# -*- coding: utf-8 -*-

"""Modulo que carga la configuracion particular del usuario ingresado"""

# Modulos externos
import re, sqlite3, time, sys, urllib2, httplib

# Modulos propios
sys.path.append('../conf')
import config
import servidores

# Clase
class Usuario:
    def __init__(self, usuario):
        self.nombre=usuario
        self.servidor=servidores.Servidor()
        conexion = sqlite3.connect(config.PATH_DB)
        self.cursor=conexion.cursor()
        self.id, self.es_admin=self.getUserIdAndAdmin(usuario)
        self.recargarDominiosDenegados()
        self.recargarDominiosPermitidos()
        self.recargarDominiosPublicamentePermitidos()
        self.recargarDominiosPublicamenteDenegados()
        self.recargarCacheAceptadas()
        self.recargarCacheDenegadas()
        self.ultimaRecargaDeDominios=0
        self.recargarPeriodoDeActualizacion()
        #conexion.close()
        #del(self.cursor)
        self.buffer_denegadas=[]
        self.buffer_aceptadas=[]

    def __str__(self):
        return self.nombre

    def __eq__(self, nombre):
        if self.nombre == nombre:
            return True
        return False

    def __getattribute__(self, attr):
        return object.__getattribute__(self, attr)

#    def __del__(self):
#        self.conexion.commit()
#        self.conexion.close()

    def getUserIdAndAdmin(self, usuario):
        """Devuelve el id del usuario, y si este es admin"""
        if usuario == "NoBody":
            id_usuario=1
            es_admin=0
            return id_usuario,  es_admin
        respuesta=self.cursor.execute('select id,admin from usuarios where username=? ', (usuario, ))
        return respuesta.fetchone()

    def recargarCacheDenegadas(self):
        """Recarga la cache de urls denegadas, con lo que esta en la base de datos"""
        self.cache_urls_denegadas=[]
        respuesta=self.cursor.execute('select url from cache_urls_denegadas').fetchall()
        for fila in respuesta:
            self.cache_urls_denegadas.append(fila[0])

    def recargarCacheAceptadas(self):
        """Recarga la cache de urls aceptadas, con lo que esta en la base de datos"""
        self.cache_urls_aceptadas=[]
        respuesta=self.cursor.execute('select url from cache_urls_aceptadas').fetchall()
        for fila in respuesta:
            self.cache_urls_aceptadas.append(fila[0])

    def recargarDominiosDenegados(self):
        """Carga desde la base de datos a memoria los dominios denegados"""
        self.dominios_denegados=[]
        respuesta=self.cursor.execute('select url from dominios_denegados where usuario=?', (self.id, )).fetchall()
        for fila in respuesta:
            self.dominios_denegados.append(fila[0])

    def recargarDominiosPermitidos(self):
        """Carga desde la base de datos a memoria los dominios permitidos"""
        self.dominios_permitidos=[]
        respuesta=self.cursor.execute('select url from dominios_permitidos where usuario=?',(self.id, )).fetchall()
        for fila in respuesta:
            self.dominios_permitidos.append(fila[0])

    def recargarDominiosPublicamentePermitidos(self):
        """Carga desde la base de datos a memoria los dominios Publicamente permitidos"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        self.dominios_publicamente_permitidos=[]
        respuesta=cursor.execute('select url from dominios_publicamente_permitidos').fetchall()
        for fila in respuesta:
            self.dominios_publicamente_permitidos.append(fila[0])
        conexion.close()

    def recargarDominiosPublicamenteDenegados(self):
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        """Carga desde la base de datos a memoria los dominios Publicamente denegados"""
        self.dominios_publicamente_denegados=[]
        respuesta=cursor.execute('select url from dominios_publicamente_denegados').fetchall()
        for fila in respuesta:
            self.dominios_publicamente_denegados.append(fila[0])
        conexion.close()

    def dominioPermitido(self, url):
        """Verifica si el dominio esta en la lista de dominios permitidos"""
        for dominio in self.dominios_permitidos:
            if re.search(dominio,url):
                return True
        return False

    def dominioDenegado(self, url):
        """Verifica si el dominio esta en la lista de dominios denegados"""
        for dominio in self.dominios_denegados:
            if re.search(str(dominio),url):
                return True
        return False

    def dominioPublicamentePermitido(self, url):
        """Verifica si el dominio esta en la lista de dominios Publicamente permitidos"""
        dominio=url.split('/')[2]
        return dominio in self.dominios_publicamente_permitidos

    def dominioPublicamenteDenegado(self, url):
        """Verifica si el dominio esta en la lista de dominios Publicamente denegados"""
        dominio=url.split('/')[2]
        return dominio in self.dominios_publicamente_denegados

    def cacheAceptadas(self, url):
        """Verifica si la url esta en la cache de aceptadas"""
        if url in self.cache_urls_aceptadas:
            return True
        else:
            return False

    def cacheDenegadas(self, url):
        """Verifica si la url esta en la cache de denegadas"""
        if url in self.cache_urls_denegadas:
            return True
        else:
            return False

    def persistirACacheAceptadas(self, url):
        """Baja de la cache en memoria, a la base de datos las urls aceptadas"""
        hora_url=time.time()
        self.buffer_aceptadas.append([url, hora_url])
        if len(self.buffer_aceptadas) > (config.MAX_CACHE_URLS_ACEPTADAS):
            conexion = sqlite3.connect(config.PATH_DB)
            cursor=conexion.cursor()
            for item in self.buffer_aceptadas:
                cursor.execute('insert into cache_urls_aceptadas values (?,?)',(item[0],item[1], ))
            conexion.commit()
            conexion.close()
            self.buffer_aceptadas=[]

    def persistirACacheDenegadas(self, url):
        """Baja de la cache en memoria, a la base de datos las urls denegadas"""
        hora_url=time.time()
        self.buffer_denegadas.append([url, hora_url])
        if len(self.buffer_denegadas) > (config.MAX_CACHE_URLS_DENEGADAS):
            conexion = sqlite3.connect(config.PATH_DB)
            cursor=conexion.cursor()
            for item in self.buffer_denegadas:
                cursor.execute('insert into cache_urls_denegadas values (?,?)',(item[0],item[1], ))
            conexion.commit()
            conexion.close()
            self.buffer_denegadas=[]

    def recargarPeriodoDeActualizacion(self):
        ip=config.SYNC_SERVER_IP
        port=config.SERVER_PORT
        # prueba con el servidor seteado en la conifg, y sino devuelve
        # uno valido
        ip, port=self.servidor.obtenerServidor(ip,port)
        conexion=httplib.HTTPConnection("%s:%s" % (ip, port))
        headers = {"UserID": "1","Peticion":"getPeriodoDeActualizacion"}
        conexion.request("GET", "/", "", headers)
        respuesta=conexion.getresponse()
        respuesta=respuesta.read()
        if not respuesta or not respuesta.isdigit():
            respuesta=10
        self.periodoDeActualizacionDB=int(respuesta)*60

    def chequearEdadCaches(self):
        tiempo_actual=time.time()
        tiempo_transcurrido=tiempo_actual - self.ultimaRecargaDeDominios
        if (tiempo_transcurrido > self.periodoDeActualizacionDB):
            self.recargarDominiosPublicamentePermitidos()
            self.recargarDominiosPublicamenteDenegados()
            self.recargarPeriodoDeActualizacion()
            self.ultimaRecargaDeDominios=tiempo_actual
            print "Recargando dominios !!!, se volveran a sincronizar en %s" % self.periodoDeActualizacionDB

    def validarRemotamente(self, url):
        """Consulta al servidor por la url, porque no pudo determinar su aptitud"""
        self.chequearEdadCaches()
        if config.USAR_PROXY:
            if self.servidor.estaOnline(config.PROXY_IP,config.PROXY_PORT):
                server="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
                proxy={'http':server, 'https': server}
                proxy_handler=urllib2.ProxyHandler(proxy)
                opener=urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
            else:
                print "El proxy no esta escuchando en %s:%s por lo que no se \
                utilizara" % (config.PROXY_IP,config.PROXY_PORT,)

        heads = {"UserID": "1","URL":url,"Peticion":"consulta"}
        ip=config.SERVER_IP
        port=config.SERVER_PORT
        ip,port=self.servidor.obtenerServidor(ip,port)
        req = urllib2.Request("http://%s:%s" %(ip, port, ),headers=heads)
        try:
            respuesta = urllib2.urlopen(req)
            if respuesta.getcode() == 204:
                return True, ""
            else:
                return False, respuesta.msg
        except urllib2.HTTPError, e:
            print "Error verificando la URL: %s , ERROR: %s" % (url, e.code)

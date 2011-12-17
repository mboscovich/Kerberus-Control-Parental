# -*- coding: utf-8 -*-

# Modulos externos
import sys, time, os, sqlite3, httplib, platform, logging, urllib2
#import logging.handlers

# Modulos propios
sys.path.append('conf')
sys.path.append('clases')

import config
import funciones
import servidores

# Logging
logger = funciones.logSetup (config.SYNC_LOG_FILENAME, config.SYNC_LOGLEVEL, config.SYNC_LOG_SIZE_MB, config.SYNC_LOG_CANT_ROTACIONES,"Sincronizador")

def obtenerRespuesta(headers):
        servidor=servidores.Servidor()
        config.SYNC_SERVER_IP,config.SYNC_SERVER_PORT = servidor.obtenerServidor(config.SYNC_SERVER_IP,config.SYNC_SERVER_PORT)
        server_sync="%s:%s" % (config.SYNC_SERVER_IP,config.SYNC_SERVER_PORT)
        if config.USAR_PROXY:
            if servidor.estaOnline(config.PROXY_IP,config.PROXY_PORT):
                url_proxy="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
                logger.log(logging.DEBUG,"Conectando a %s, por medio del proxy %s , para realizar la solicitud: %s" %(server_sync,url_proxy,headers['Peticion']))
                proxy={'http':url_proxy, 'https': url_proxy}
            else:
                logger.log(logging.ERROR,"El proxy no esta escuchando en %s:%s por lo que no se \
                utilizara" % (config.PROXY_IP,config.PROXY_PORT,))
                proxy={}
        else:
            proxy={}
        proxy_handler=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        logger.log(logging.DEBUG,"Conectando a %s para realizar la solicitud: %s" %(server_sync,headers['Peticion']))
        dormir_por=1
        while True:
            try:
                req = urllib2.Request("http://"+server_sync, headers=headers)
                respuesta = urllib2.urlopen(req).read()
                logger.log(logging.DEBUG,"Respuesta: %s" % respuesta)
                return respuesta
            except urllib2.URLError as error:
                logger.log(logging.ERROR,"Error al conectarse a %s, peticion: %s . ERROR: %s" %(server_sync,headers['Peticion'],error))
            logger.log(logging.ERROR,"Durmiendo por %s", dormir_por)
            time.sleep(dormir_por)
            #se va incrementando el tiempo de dormir para no  matar el micro
            dormir_por=dormir_por*2

def sincronizarDominiosPermitidos(ultima_actualizacion,recargar_todos_los_dominios):
        if recargar_todos_los_dominios:
            ultima_actualizacion=0
        headers = {"UserID": "1","Peticion":"obtenerDominiosPermitidos","UltimaSync":str(ultima_actualizacion)}
        dominios = obtenerRespuesta(headers)
        if len(dominios):
            if dominios[-1]=="":
                    array_dominios=dominios.rsplit("\n")[0:-1]
            else:
                array_dominios=dominios.rsplit("\n")
            if recargar_todos_los_dominios:
                cursor.execute('delete from dominios_publicamente_permitidos')
            for fila in array_dominios:
                if fila <> "":
                    logger.log(logging.DEBUG, "Se agrego el dominio permitido: %s" % fila)
                    cursor.execute('insert into dominios_publicamente_permitidos(url) values(?)', (fila, ) )
            conexion_db.commit()
        else:
           logger.log(logging.DEBUG,"No hay dominios permitidos para actualizar")

def sincronizarDominiosDenegados(ultima_actualizacion,recargar_todos_los_dominios):
        if recargar_todos_los_dominios:
            ultima_actualizacion=0
        headers = {"UserID": "1","Peticion":"obtenerDominiosDenegados","UltimaSync":str(ultima_actualizacion)}
        dominios = obtenerRespuesta(headers)
        if len(dominios):
            if dominios[-1]=="":
                array_dominios=dominios.rsplit("\n")[0:-1]
            else:
                array_dominios=dominios.rsplit("\n")
            if recargar_todos_los_dominios:
                cursor.execute('delete from dominios_publicamente_denegados')
            for fila in array_dominios:
                if fila <> "":
                    logger.log(logging.DEBUG, "Se agrego el dominio denegado: %s" % fila)
                    cursor.execute('insert into dominios_publicamente_denegados(url) values(?)',(fila, ) )
            conexion_db.commit()
        else:
           logger.log(logging.DEBUG,"No hay dominios denegados para actualizar")

def getPeriodoDeActualizacion():
        headers = {"UserID": "1","Peticion":"getPeriodoDeActualizacion"}
        respuesta = obtenerRespuesta(headers)
        return respuesta

def getPeriodoDeRecargaCompleta():
        headers = {"UserID": "1","Peticion":"getPeriodoDeRecargaCompleta"}
        respuesta = obtenerRespuesta(headers)
        return respuesta

def getHoraServidor():
        headers = {"UserID": "1","Peticion":"getHoraServidor"}
        respuesta = obtenerRespuesta(headers)
        return respuesta

def sincronizarDominiosConServer(tiempo_actual, ultima_actualizacion,recargar_todos_los_dominios):
        sincronizarDominiosPermitidos(ultima_actualizacion,recargar_todos_los_dominios)
        sincronizarDominiosDenegados(ultima_actualizacion,recargar_todos_los_dominios)
        if recargar_todos_los_dominios:
            cursor.execute('update sincronizador set ultima_actualizacion=?, ultima_recarga_completa=?', (tiempo_actual, tiempo_actual))
        else:
            cursor.execute('update sincronizador set ultima_actualizacion=%s' % tiempo_actual)
        conexion_db.commit()
        logger.log(logging.INFO, "Se ha sincronizado la base de datos de dominios publicamente aceptados/denegados")

#def borrarUrlsViejasCache(hora_actual, edad_max):
#    tiempo_expiracion=hora_actual-edad_max
#    timestring=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tiempo_expiracion))
#    respuesta=cursor.execute('delete from cache_urls_aceptadas where hora < ? ', (tiempo_expiracion, ))
#    conexion_db.commit()
#    respuesta=cursor.execute('delete from cache_urls_denegadas where hora < ? ', (tiempo_expiracion, ))
#    conexion_db.commit()
#    print "Se han borrado las urls viejas de cache"

# Inicio

while True:
    #obtiene el tiempo en minutos
    logger.log(logging.INFO, "Iniciando el demonio de sincronización")
    periodo_expiracion=getPeriodoDeActualizacion()
    periodo_recarga_completa=getPeriodoDeRecargaCompleta()
    hora_servidor=getHoraServidor()
    logger.log(logging.DEBUG, "Hora del servidor: %s" % hora_servidor)
    if not periodo_expiracion:
        periodo_expiracion=1
    logger.log(logging.DEBUG, "Periodo de actualizacion: %s minuto/s" % periodo_expiracion)
    logger.log(logging.DEBUG, "Periodo de recarga completa: %s minuto/s" % periodo_recarga_completa)
    # paso de minutos a segundos el periodo de expiracion
    periodo_expiracion=int(periodo_expiracion)*60
    periodo_recarga_completa=int(periodo_recarga_completa)*60
    conexion_db = sqlite3.connect(config.PATH_DB)
    cursor=conexion_db.cursor()
    ultima_actualizacion=cursor.execute('select ultima_actualizacion from sincronizador').fetchone()[0]
    ultima_recarga_completa=cursor.execute('select ultima_recarga_completa from sincronizador').fetchone()[0]
    tiempo_actual=float(hora_servidor)
    tiempo_transcurrido=tiempo_actual - ultima_actualizacion
    tiempo_transcurrido_ultima_recarga=tiempo_actual - ultima_recarga_completa
    recargar_todos_los_dominios = False
    if (tiempo_transcurrido_ultima_recarga > periodo_recarga_completa):
        recargar_todos_los_dominios = True
        logger.log(logging.DEBUG,"Se recargaran todos los dominios permitidos/dengados con servidor...")
    if (tiempo_transcurrido > periodo_expiracion):
        logger.log(logging.DEBUG,"Sincronizando dominios permitidos/dengados con servidor...")
        sincronizarDominiosConServer(tiempo_actual,ultima_actualizacion,recargar_todos_los_dominios)
        #borrarUrlsViejasCache(tiempo_actual, periodo_expiracion)
    else:
        tiempo_restante=ultima_actualizacion + periodo_expiracion - tiempo_actual
        tiempo_proxima_recarga_completa=ultima_recarga_completa + periodo_recarga_completa - tiempo_actual
        logger.log(logging.DEBUG, "Faltan %s minutos para que se chequee si hay dominios nuevos, y %s minutos para recargar todos los dominios" % (tiempo_restante/60,tiempo_proxima_recarga_completa/60))
        time.sleep(tiempo_restante)
    conexion_db.close()


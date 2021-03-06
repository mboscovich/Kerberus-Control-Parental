#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "1.1"

# Modulos externos
import BaseHTTPServer
import select
import socket
import SocketServer
import urlparse
import sys
import signal
import threading
from types import FrameType, CodeType
import ftplib
import base64
import os
import logging

sys.path.append('clases')
sys.path.append('conf')
sys.path.append('password')

#Modulos propios

import consultor
import manejadorUrls
import config
import funciones
import administradorDeUsuarios
import mensajesHtml
import loguear
import urllib2
import detectorDeBrowser
import peticion

# Logging
logger = loguear.logSetup(config.LOG_FILENAME, config.LOGLEVEL,
    config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES, "kerberus")

if not os.path.exists(config.PATH_DB):
    funciones.crearDBCliente(config.PATH_DB)

urls = manejadorUrls.ManejadorUrls()
adminUsers = administradorDeUsuarios.AdministradorDeUsuarios()


class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

    server_version = "Kerberus - Cliente /" + __version__
    rbufsize = 0                        # self.rfile Be unbuffered

    def mostrarPublicidad(self, url):
        msg = "<html><head><title>Navegador protegido por Kerberus</title>"\
        "<meta http-equiv=\"REFRESH\" content=\"0;"\
        "url=http://inicio.kerberus.com.ar\" ></head> <body ></body> </html>"
        self.server.logger.log(logging.DEBUG, "Primer pagina de acceso.")
        self.responderAlCliente(msg)

    def responderAlCliente(self, mensaje):
        tamano = len(mensaje)
        self.wfile.write(self.protocol_version +
            " 200 Connection established\r\n")
        self.wfile.write("Content-Type: text/html\r\n")
        self.wfile.write(" Content-Length: %s\r\n" % tamano)
        self.wfile.write("\r\n")
        self.wfile.write(mensaje)
        self.connection.close()

    def pedirPassword(self):
        mensaje = mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg = mensaje.pedirPassword()
        self.responderAlCliente(msg)

    def cambiarPassword(self):
        mensaje = mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg = mensaje.cambiarPassword('', 'password_actual')
        self.responderAlCliente(msg)

    def recargarDominios(self):
        self.server.logger.info("Recargando dominios del usuario")
        #import sincronizador
        #sync = sincronizador.Sincronizador(
                #self.server.verificador.peticionRemota)
        #sync.recargar_todos_los_dominios = True
        #sync.sincronizarDominiosUsuario()
        self.server.verificador.admDominios.recargarDominiosUsuario()

    def recordarPassword(self):
        import registrar
        registrador = registrar.Registradores()
        if registrador.checkRegistradoRemotamente():
            import peticion
            peticionRemota = peticion.Peticion()
            respuesta = peticionRemota.recordarPassword()
            id, nombre, email, version, password = \
                registrador.obtenerDatosRegistrados()
            mensaje = mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)

            if respuesta == 'Recordada':
                msj = u'Estimado usuario,<br><br>Le hemos enviado un e-mail '\
                u'a su cuenta de correo %s con la contraseña de administrador '\
                u'de Kerberus.' % (email)
            else:
                msj = u'Estimado usuario,<br><br>Ya hemos enviado un e-mail a'\
                u' su cuenta de correo %s con la contraseña de administrador '\
                u'de Kerberus.' % (email)
            msg = mensaje.recordarPassword(msj)
            self.responderAlCliente(msg)

    def redirigirDesbloqueado(self, url):
        msg = "<html><head><meta HTTP-EQUIV=\"REFRESH\" content=\"0; url=%s\""\
        "></head></html>" % url
        self.responderAlCliente(msg)

    def passwordErronea(self):
        mensaje = mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg = mensaje.pedirPassword(u'Contraseña incorrecta!')
        self.responderAlCliente(msg)

    def cambioPassPasswordErronea(self):
        mensaje = mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg = mensaje.cambiarPassword(u'Contraseña incorrecta!',
                                        'password_actual')
        self.responderAlCliente(msg)

    def passwordCambiadaCorrectamente(self):
        mensaje = mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg = mensaje.passwordCambiadaCorrectamente(
            u'Contraseña cambiada correctamente!')
        self.responderAlCliente(msg)

    def cambioPassPasswordNoCoinciden(self):
        mensaje = mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg = mensaje.cambiarPassword(u'Las contraseñas no coinciden!',
            'password_nueva1')
        self.responderAlCliente(msg)

    def denegar(self, motivo, url):
        motivo_b64 = base64.b64encode(motivo)
        url_b64 = base64.b64encode(url)
        msg = ("<html><head><title>Sitio Denegado</title>"
                "<meta http-equiv=\"REFRESH\" content=\"0;"
                "url=http://denegado.kerberus.com.ar/%(url)s/%(motivo)s"
                "\" ></head> <body ></body> </html>"
                % {'motivo': motivo_b64, 'url': url_b64})

        self.server.logger.log(
                logging.DEBUG,
                "Sitio %(url)s DENEGADO, motivo: %(motivo)s"
                % {'motivo': motivo, 'url': url})
        self.responderAlCliente(msg)

    def denegar2(self, motivo, url):
        motivo_b64 = base64.b64encode(motivo)
        url_b64 = base64.b64encode(url)
        msg = ("Denegado")

        self.server.logger.log(
                logging.DEBUG,
                "Sitio %(url)s DENEGADO, motivo: %(motivo)s"
                % {'motivo': motivo, 'url': url})
        self.responderAlCliente(msg)

    def handle(self):
        self.__base_handle()

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i + 1:])
        else:
            host_port = netloc, 80
        self.server.logger.log(logging.DEBUG,
            "connect to %s:%d", host_port[0], host_port[1])
        try:
            soc.connect(host_port)

        except socket.error, arg:
            try:
                msg = arg[1]
            except:
                msg = arg
                self.send_error(404, msg)
            return False
        return True

    # Utilizado en conexiones HTTPS
    def do_CONNECT(self):
        # Si se van a realizar busquedas en https, las redirige a http
        if self.path.startswith("www.google.") and self.path.endswith(":443"):
            self.path = "nosslsearch.google.com:443"

        # Si quieren usar encrypted, no los pelo
        if self.path.startswith("encrypted.google."):
            self.denegar("Sitio de busqueda no permitido", self.path)

        self.server.logger.log(
                logging.DEBUG,
                "Metodo do_CONNECT, path: %(url)s"
                % {'url': self.path})

        # Valido
        url = 'https://' + self.path
        self.server.logger.info(url)
        if self.server.verificador.kerberus_activado:

            permitido, motivo = self.server.verificador.validarDominio(url)
            if not permitido:
                self.denegar2(motivo, url)
                return False

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(self.path, soc):
                self.wfile.write(self.protocol_version +
                    " 200 Connection established\r\n")
                self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
                self.wfile.write("\r\n")
                self._read_write(soc, 300)
        finally:
            soc.close()
            self.connection.close()

    def validarPassword(self, password):
        return adminUsers.usuario_valido('admin', password)

    def do_KERBERUSREFRESH(self):
        self.recargarDominios()

    def do_KERBERUSESTADO(self):
        if self.server.verificador.kerberus_activado:
            respuesta = "Activo"
        else:
            respuesta = "Inactivo"
        self.wfile.write(respuesta)
        self.connection.close()

    def do_GET(self):
        modoDeConexion = self.headers.getheader('Proxy-Connection',
                                                'Transparente')
        hostDestino = self.headers.getheader('Host')
        hostDestino = "http://%s" % hostDestino
        if modoDeConexion == 'Transparente' and hostDestino not in self.path:
            url = hostDestino + self.path
        else:
            url = self.path

        if self.server.verificador.primerUrl:
            try:
                userAgent = self.headers.getheader('User-Agent')
            except:
                userAgent = False
            esbrowser = detectorDeBrowser.esBrowser(userAgent)
            self.server.verificador.primerUrl = False
            if "kerberus.com.ar" not in url and esbrowser:
                self.mostrarPublicidad(url)
                return False

        # Usuarios del sistema no remotos (para cuando tengamos multi-user)
        usuario, password = "NoBody", "NoBody"

        if "!HabilitarFiltrado!" in url:
            url = url.replace('!HabilitarFiltrado!', '')
            self.server.verificador.kerberus_activado = True
            self.redirigirDesbloqueado(url)
            return True

        if "!DeshabilitarFiltrado!" in url:
            url = url.replace('!DeshabilitarFiltrado!', '')
            if self.server.verificador.kerberus_activado:
                if self.command == 'POST':
                    try:
                        content_len = int(
                                    self.headers.getheader('content-length')
                                    )
                        post_body = self.rfile.read(content_len)
                        password = post_body.split("=")[1]
                        password = unicode(urllib2.unquote(password), 'utf-8')
                    except:
                        self.server.logger.log(logging.ERROR,
                            'Hubo un error al obtener la password de '
                            'administrador de kerberus!')
                        password = ''

                    usuario_admin = self.validarPassword(password)
                    if usuario_admin:
                        self.server.verificador.kerberus_activado = False
                        self.redirigirDesbloqueado(url)
                        return True
                    else:
                        self.passwordErronea()
                        return True
                else:
                    self.pedirPassword()
                    return True

        # Cambio de password
        if "!CambiarPassword!" in url:
            url = url.replace('!CambiarPassword!', '')
            if self.command == 'POST':
                try:
                    content_len = int(self.headers.getheader('content-length'))
                    post_body = self.rfile.read(content_len)
                    password_actual = post_body.split("&")[0].split("=")[1]
                    password_nueva1 = post_body.split("&")[1].split("=")[1]
                    password_nueva2 = post_body.split("&")[2].split("=")[1]
                    password_actual = unicode(urllib2.unquote(password_actual),
                                                'utf-8')
                    password_nueva1 = unicode(urllib2.unquote(password_nueva1),
                                                'utf-8')
                    password_nueva2 = unicode(urllib2.unquote(password_nueva2),
                                                'utf-8')
                except:
                    self.server.logger.log(logging.ERROR,
                        'Hubo un error al obtener los datos para hacer '
                        'el cambio de password de administrador de kerberus!')
                    password_actual = ''

                usuario_admin = self.validarPassword(password_actual)
                if usuario_admin:
                    if password_nueva1 != password_nueva2:
                        self.cambioPassPasswordNoCoinciden()
                        return True
                    adminUsers.cambiarPassword('admin', password_actual,
                        password_nueva1)
                    self.passwordCambiadaCorrectamente()
                    return True
                else:
                    self.cambioPassPasswordErronea()
                    return True
            else:
                self.cambiarPassword()
                return True

        if "!RecordarPassword!" in url:
            url = url.replace('!RecordarPassword!', '')
            self.recordarPassword()
            return True

        #FIXME: Esto deberia ser un header no por url
        if "http://inicio.kerberus.com.ar" in url and \
            self.server.verificador.kerberus_activado:
            url = url + "?kerberus_activado=1"

        if self.server.verificador.kerberus_activado:
            permitido, motivo = self.server.verificador.validarUrl(url)
            if not permitido:
                self.denegar(motivo, url)
                return False
            if urls.soportaSafeSearch(url):
                url = urls.agregarSafeSearch(url)
                self.server.logger.log(logging.INFO,
                    "La URL %s  soporta SafeSearch. Forzando su uso", url)

        # Si llego hasta aca es porque esta permitido
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(url,
            'http')
        if not netloc:
            netloc = self.server.ultimo_netloc

        if scm not in ('http', 'ftp') or fragment or not netloc:
            self.send_error(400, "Url erronea: %s" % url)
            return False
        else:
            self.server.ultimo_netloc = netloc
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if scm == 'http':
                if self._connect_to(netloc, soc):
                    try:
                        # Ejemplo de request http:
                        #
                        # GET /index.php?param1=value1&param2=value2 HTTP/1.1
                        #
                        # metodo_http = GET
                        # recurso_http = /index.php?param1=value1&param2=value2
                        # version_http = HTTP/1.1

                        metodo_http = self.command
                        recurso_http = urlparse.urlunparse(
                                        ('', '', path, params, query, '')
                                    )
                        version_http = self.request_version

                        self.server.logger.debug("Enviando: %s %s %s\r\n" %
                                (metodo_http, recurso_http, version_http)
                            )
                        soc.send(
                            "%s %s %s\r\n" %
                                (metodo_http, recurso_http, version_http)
                            )
                        self.headers['Connection'] = 'close'

                        del self.headers['Proxy-Connection']

                        for key_val in self.headers.items():
                            soc.send("%s: %s\r\n" % key_val)

                        soc.send("\r\n")
                        self._read_write(soc)
                    except:
                        self.server.logger.error(
                            "Hubo un error en el metodo do_GET. URL: %s", url
                            )

            elif scm == 'ftp':
                # fish out user and password information
                i = netloc.find('@')
                if i >= 0:
                    login_info, netloc = netloc[:i], netloc[i + 1:]
                    try:
                        user, passwd = login_info.split(':', 1)
                    except ValueError:
                        user, passwd = "anonymous", None
                else:
                    user, passwd = "anonymous", None
                try:
                    ftp = ftplib.FTP(netloc)
                    ftp.login(user, passwd)
                    if self.command == "GET":
                        ftp.retrbinary("RETR %s" % path, self.connection.send)
                    ftp.quit()
                except Exception, e:
                    self.server.logger.log(logging.WARNING,
                    "FTP Exception: %s", e)
        finally:
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=20, local=False):
        #FIXME: Revisar esta funcion!!!!!! tira el problema 10053 de socket
        iw = [self.connection, soc]
        local_data = ""
        ow = []
        count = 0
        timeout = 3
        while 1:
            count += 1
            # ins: sockets legibles.
            # exs: se produjo una excepcion en algun socket
            # iw: sockets desde donde se leerean datos.
            # ow: sockets donde se escribirán datos.
            (ins, _, exs) = select.select(iw, ow, iw, timeout)
            if exs:
                break
            if ins:
                for i in ins:
                    # soc: destino de la conexion.
                    # self.connection: cliente
                    if i is soc:
                        out = self.connection
                    else:
                        out = soc
                    try:
                        data = i.recv(8192)
                    except:
                        data = ''

                    if data:
                        if local:
                            local_data += data
                        else:
                            out.send(data)
                        count = 0
            if count == max_idling:
                break
        if local:
            return local_data
        return None

    # Estos son todos los metodos http que encontre (estandares o no)
    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    do_OPTIONS = do_GET
    do_TRACE = do_GET
    do_PATCH = do_GET
    do_LINK = do_GET
    do_UNLINK = do_GET
    do_PROPFIND = do_GET
    do_PROPPATCH = do_GET
    do_MKCOL = do_GET
    do_COPY = do_GET
    do_MOVE = do_GET
    do_LOCK = do_GET
    do_UNLOCK = do_GET
    do_VERSION_CONTROL = do_GET
    do_REPORT = do_GET
    do_CHECKOUT = do_GET
    do_CHECKIN = do_GET
    do_UNCHECKOUT = do_GET
    do_MKWORKSPACE = do_GET
    do_UPDATE = do_GET
    do_LABEL = do_GET
    do_MERGE = do_GET
    do_BASELINE_CONTROL = do_GET
    do_MKACTIVITY = do_GET
    do_ORDERPATCH = do_GET
    do_ACL = do_GET
    do_MKREDIRECTREF = do_GET
    do_UPDATEREDIRECTREF = do_GET
    do_MKCALENDAR = do_GET
    do_SEARCH = do_GET
    do_BIND = do_GET
    do_UNBIND = do_GET
    do_REBIND = do_GET
    do_BCOPY = do_GET
    do_BDELETE = do_GET
    do_BMOVE = do_GET
    do_BPROPFIND = do_GET
    do_BPROPPATCH = do_GET
    do_NOTIFY = do_GET
    do_POLL = do_GET
    do_SUBSCRIBE = do_GET
    do_UNSUBSCRIBE = do_GET
    do_X_MS_ENUMATTS = do_GET


class ThreadingHTTPServer(SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, logger=None):
        BaseHTTPServer.HTTPServer.__init__(self, server_address,
                                            RequestHandlerClass)
        self.logger = logger
        self.peticionRemota = peticion.Peticion()
        self.verificador = consultor.Consultor(self.peticionRemota)
        self.ultimo_netloc = ""


def handler(signo, frame):
    while frame and isinstance(frame, FrameType):
        if frame.f_code and isinstance(frame.f_code, CodeType):
            if "run_event" in frame.f_code.co_varnames:
                frame.f_locals["run_event"].set()
                return
        frame = frame.f_back


def main():
    run_event = threading.Event()
    signal.signal(signal.SIGINT, handler)
    server_address = (config.BIND_ADDRESS, config.BIND_PORT)
    ProxyHandler.protocol = "HTTP/1.1"
    httpd = ThreadingHTTPServer(server_address, ProxyHandler, logger)
    sa = httpd.socket.getsockname()
    pid = os.getpid()
    logger.info('Kerberus - Cliente atendiendo en %s:%s, pid:%s' %
                    (sa[0], sa[1], pid))

    req_count = 0
    while not run_event.isSet():
        try:
            httpd.handle_request()
            req_count += 1
            if req_count == 1000:
                logger.info("Number of active threads: %s",
                            threading.activeCount())
                req_count = 0
        except select.error, e:
            if e[0] == 4 and run_event.isSet():
                pass
            else:
                logger.critical("Errno: %d - %s", e[0], e[1])
    return 0

if __name__ == '__main__':
    sys.exit(main())

# -*- coding: utf-8 -*-

"""Modulo encargado de verificar la aptitud de una url"""

#Modulos externos
import time
import re
#import sys

#Modulos propios
import administradorDeUsuarios
#import manejadorUrls
import usuario
import config
#import servidores
import logging


modulo_logger = logging.getLogger('kerberus.' + __name__)


#Excepciones
class ConsultorError(Exception):

    def __init__(self):
        super(ConsultorError, self).__init__()
        pass


# Clase
class Consultor:
    def __init__(self):
        self.primerUrl = True
        self.kerberus_activado = True
        self.usuario = usuario.Usuario('usuario')

    def extensionValida(self, url):
        url = url.lower()
        return re.match(".*\.(gif|jpeg|jpg|png|js|css|swf|ico|json|mp3|wav|"
        "rss|rar|zip|pdf|xml)$", url)

    def urlBienFormada(self, url):
        url = url.lower()
        return re.match(".*\..*/.*", url)

    def validarUrl(self, url):
        if not self.urlBienFormada(url):
            mensaje = "URL mal formada"
            modulo_logger.log(logging.DEBUG, mensaje)
            return True, mensaje

        #TODO: No se si esto esta bien, revisar
        if "kerberus.com.ar" in url:
            mensaje = "Consulta a kerberus"
            modulo_logger.log(logging.DEBUG, mensaje)
            return True, mensaje

        self.inicio = time.time()
        if self.usuario.dominioDenegado(url):
            mensaje = "Dominio no permitido."
            if config.DEBUG_DOM_DENG:
                modulo_logger.log(logging.INFO, mensaje)
            return False, mensaje

        elif self.usuario.dominioPermitido(url):
            mensaje = "Dominio permitido"
            if config.DEBUG_DOM_PERM:
                modulo_logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif self.usuario.dominioPublicamentePermitido(url):
            mensaje = "Dominio permitido"
            if config.DEBUG_DOM_PUB_PERM:
                modulo_logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif self.usuario.dominioPublicamenteDenegado(url):
            mensaje = "Dominio denegado"
            if config.DEBUG_DOM_PUB_DENG:
                modulo_logger.log(logging.INFO, mensaje)
            return False, mensaje

        elif self.extensionValida(url):
            mensaje = "Exension valida: " + url
            if config.DEBUG_EXTENSIONES:
                modulo_logger.log(logging.INFO, mensaje)
            return True, mensaje

        else:
            valido, razon = self.usuario.validarRemotamente(url)
            if valido:
                mensaje = "Url validada remotamente : " + url
                if config.DEBUG_VALIDA_REM:
                    modulo_logger.log(logging.INFO, mensaje)
                return True, ""
            else:
                mensaje = "URL: %s <br>Motivo: %s" % (url, razon)
                if config.DEBUG_NO_VALIDA_REM:
                    modulo_logger.log(logging.INFO, mensaje)
                return False, mensaje


def main():
    pass

# Importante: los módulos no deberían ejecutar
# codigo al ser importados
if __name__ == '__main__':
    main()
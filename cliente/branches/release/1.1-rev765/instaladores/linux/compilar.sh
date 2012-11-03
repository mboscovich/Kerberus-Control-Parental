#!/bin/bash
echo "   - Limpiando directorios..."
[ -d ../cliente/build ] && rm -r ../cliente/build
[ -d ../cliente/dist ] && rm -r ../cliente/dist
[ -d ../sincronizadorCliente/build ] && rm -r ../sincronizadorCliente/build
[ -d ../sincronizadorCliente/dist ] && rm -r ../sincronizadorCliente/dist
[ -d ../desinstalador/build ] && rm -r ../desinstalador/build
[ -d ../desinstalador/dist ] && rm -r ../desinstalador/dist

grep ENTORNO_DE_DESARROLLO=True ../../conf/config.py > /dev/null
if [ ${?} -eq 0 ];then
	echo "   - Seteando entorno en produccion..."
	sed -i s/ENTORNO_DE_DESARROLLO=True/ENTORNO_DE_DESARROLLO=False/g ../../conf/config.py
	SETEADO_ENTORNO=true 
fi
echo "   - compilando cliente..."
python ../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR ./cliente/cliente.spec
echo "   - compilando sincronizador..."
python ../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR ./sincronizadorCliente/sincronizadorCliente.spec
echo "   - compilando desinstalador..."
python ../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR ./desinstalador/desinstalador.spec

if [ ${SETEADO_ENTORNO} ]; then
          echo "   - Volviendo al entorno de desarrollo..."
          sed -i s/ENTORNO_DE_DESARROLLO=False/ENTORNO_DE_DESARROLLO=True/g  ../../conf/config.py
fi

echo "   - Generando archivo payload..."
cd cliente/dist/
tar cvfz ../../payload/cliente.tar.gz cliente > /dev/null
cd ../../
cd sincronizadorCliente/dist/
tar cvfz ../../payload/sincronizador.tar.gz sincronizadorCliente > /dev/null
cd ../../
cd desinstalador/dist/
tar cvfz ../../payload/desinstalador.tar.gz desinstalador > /dev/null
cd ../../


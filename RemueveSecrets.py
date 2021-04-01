#!/usr/bin/python
from progress.bar import Bar, ChargingBar
import ManejadorDeArchivos
import Secrets
def IniciaFlujoSecretos(Secretos):
    lista = []
    lista = ManejadorDeArchivos.ls(lista,Secretos.rutaRepositorio)
    barra = ChargingBar('Escaneando: ', max=len(lista))
    resultado = []
    for file in lista:
        contenido = ManejadorDeArchivos.readFile(file)
        Cambios = False
        Mensaje = ''
        for secret in Secretos.listaSecretos:
            if contenido.find(secret['Valor']) != -1:
                val = secret['Valor']
                Mensaje += f'\t{file} - Secreto encontrado: {val}\n'
                contenido = contenido.replace(secret['Valor'], secret['Llave'])
                Cambios = True
        if Cambios:
            ManejadorDeArchivos.writeFile(file, contenido)
            Mensaje += f'\tSecretos guardados en {file}'
        if Mensaje != '':
            resultado.append(Mensaje)
            Mensaje = ''
        barra.next()
    barra.finish()
    for msg in resultado:
        print(msg)
print('1. - Verifica si existen secretos configurados')
secretos = ManejadorDeArchivos.readFile('secrets.dll')
if len(secretos) == 0:
    print('No hay secretos configurados')
    Secretos = Secrets.ClsSecrets('')
    if not Secretos.ValidaRuta():
        Secretos.leeRuta()
    if not Secretos.ValidaListas():
        Secretos.leeSecretos()
    Secretos.SaveSecrets()
    print('2. - Inicia flujo para ocultar secretos')
    IniciaFlujoSecretos(Secretos)
    print('3. - Fin de secretos')
else:
    print('2. - Valida si existe ruta para el repositorio y secretos')
    Secretos = Secrets.ClsSecrets(secretos)
    if Secretos.rutaRepositorio == '':
        print('2.1. - Inserta Ruta')
        if not Secretos.ValidaRuta():
            Secretos.leeRuta()
    if Secretos.listaSecretos == []:
        print('2.2. - Inserta Secretos')
        if not Secretos.ValidaListas():
            Secretos.leeSecretos()
    Secretos.SaveSecrets()
    print('3. - Inicia flujo para ocultar secretos')
    IniciaFlujoSecretos(Secretos)
    print('4. - Fin de secretos')

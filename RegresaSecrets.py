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
            if contenido.find(secret['Llave']) != -1:
                val = secret['Llave']
                Mensaje += f'\t{file} - Secreto encontrado: {val}\n'
                contenido = contenido.replace(secret['Llave'], secret['Valor'])
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
    print('No cuenta con los secretos requeridos para este proyecto')
else:
    Secretos = Secrets.ClsSecrets(secretos)
    if Secretos.listaSecretos != []:
        print('2. - Inicia flujo de obtencion de secretos')
        IniciaFlujoSecretos(Secretos)
        print('3. - Fin de secretos')
    else:
        print('El archivo de secretos no cuenta con secretos a obtener')

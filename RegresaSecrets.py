#!/usr/bin/python
from progress.bar import Bar, ChargingBar
from colorama import Fore, init, Style
init(autoreset = True)
import ManejadorDeArchivos
import Secrets
def IniciaFlujoSecretos(Secretos):
    lista = []
    lista = ManejadorDeArchivos.ls(lista,Secretos.rutaRepositorio)
    barra = ChargingBar(Fore.GREEN + 'Escaneando: ', max=len(lista))
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
        print(Fore.YELLOW + msg)
print(Style.BRIGHT + Fore.CYAN + '1. - Verifica si existen secretos configurados')
secretos = ManejadorDeArchivos.readFile('secrets.dll')
if len(secretos) == 0:
    print(Fore.RED + 'No cuenta con los secretos requeridos para este proyecto')
else:
    Secretos = Secrets.ClsSecrets(secretos)
    if Secretos.listaSecretos != []:
        print(Style.BRIGHT + Fore.CYAN + '2. - Inicia flujo de obtencion de secretos')
        IniciaFlujoSecretos(Secretos)
        print(Style.BRIGHT + Fore.CYAN + '3. - Fin de secretos')
    else:
        print(Fore.RED + 'El archivo de secretos no cuenta con secretos a obtener')

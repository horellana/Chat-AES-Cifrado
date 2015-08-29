#!/usr/bin/env python

import sys
import asyncio
import os

from Cifrado import Enigma


class Cliente:
    def __init__(self, servidor, enigma):
        self.servidor = servidor
        self.enigma = enigma

    # Este metodo  es llamada cuando el usuario ingresa un mensaje
    # recibe el mensaje y un socket conectado al servidor
    # su trabajo es enviar el mensaje
    def enviar_mensaje(self, mensaje):
        os.system('clear')
        epic_buho()
        mostrar_historial()
        self.servidor.write(self.enigma.cifrar(mensaje))

    # Este metodo recibe un mensaje desde el servidor
    # Es su trabajo decidir que hacer con el
    # Idealmente lo muestra al usuario de alguna manera
    def recibir_mensaje(self, mensaje):
        mensaje = self.enigma.decifrar(mensaje)
        guardar_historial(mensaje.decode())
        print(mensaje.decode())


def guardar_historial(mensaje):
    ObjArchivo = open(os.getcwd()+'/historial.txt', mode='a', encoding='utf-8')
    ObjArchivo.write(mensaje)  # escribe cadena1 añadiendo salto de línea
    ObjArchivo.close  # cierra archivo


def mostrar_historial():
    archivo = open(os.getcwd()+'/historial.txt','r')  # abre archivo en modo lectura
    lista = archivo.readlines()  # lee todas la líneas a una lista
    for linea in lista[limite_inferior(lista):len(lista)]:
        print(linea, end='')
    archivo.close


def limite_inferior(lista):
    limite_inferior = (len(lista) - 10)

    if (limite_inferior <= 0):
        limite_inferior = 0
    elif (limite_inferior > 0):
        limite_inferior = limite_inferior
    else:
        print ("esto no pasa :)")
    return limite_inferior


def epic_buho():
    print ("""
    ,___,
    [O.o]   Welcome to Búho chat
    /)__)       Have fun!
    -”–”- 
    """)


@asyncio.coroutine
def tcp_echo_client(loop, servidor, puerto, key):
    # Nos conectamos al servidor
    r, w = yield from asyncio.open_connection(servidor, puerto, loop=loop)

    cliente = Cliente(w, Enigma(key))

    # Escuchamos stdin por mensajes enviados por nosotros
    # (El cliente)
    loop.add_reader(sys.stdin,
                    lambda: cliente.enviar_mensaje(sys.stdin.readline()))

    while True:
        data = yield from r.read(100)
        cliente.recibir_mensaje(data)
        
if __name__ == '__main__':
    epic_buho()

    ObjArchivo = open(os.getcwd()+'/historial.txt', mode='a', encoding='utf-8')
    ObjArchivo.close

    servidor = sys.argv[1]
    puerto = sys.argv[2]
    key = sys.argv[3]
    
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(tcp_echo_client(loop, servidor, puerto, key))
    loop.close()

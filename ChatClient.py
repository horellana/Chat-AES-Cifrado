#!/usr/bin/env python

import os
import sys
import json
import asyncio
import Cifrado
from Crypto.Util.number import getRandomInteger


class Cliente:
    def __init__(self, main_loop, servidor, puerto):
        self.historial = []
        self.main_loop = main_loop
        main_loop.add_reader(sys.stdin,
                             lambda: self.enviar_mensaje(sys.stdin.readline()))

    @asyncio.coroutine
    def loop(self):
        self.socket_r, self.socket_w = yield from asyncio.open_connection(servidor,
                                                                          puerto,
                                                                          loop=self.main_loop)

        secreto = getRandomInteger(10)
        generado = pow(Cifrado.generador, secreto) % Cifrado.modulo

        self.socket_w.write(json.dumps({'gen-key': True,
                                        'key': generado}).encode())

        respuesta_servidor = yield from self.socket_r.read(100)
        generado_servidor = json.loads(respuesta_servidor.decode())['gen']

        key = str(pow(generado_servidor, secreto) % Cifrado.modulo)

        if len(key) > 16:
            key -= key * (len(key) - 16)
        if len(key) < 16:
            key += key * int(16 - len(key))

        self.enigma = Cifrado.Enigma(key)

        while True:
            data = yield from self.socket_r.read(100)
            mensaje = self.enigma.decifrar(data)
            self.recibir_mensaje(mensaje)

    # Este metodo  es llamada cuando el usuario ingresa un mensaje
    # recibe el mensaje y un socket conectado al servidor
    # su trabajo es enviar el mensaje
    def enviar_mensaje(self, mensaje):
        os.system('clear')
        epic_buho()
        self.mostrar_historial()
        self.socket_w.write(self.enigma.cifrar(mensaje))

    # Este metodo recibe un mensaje desde el servidor
    # Es su trabajo decidir que hacer con el
    # Idealmente lo muestra al usuario de alguna manera
    def recibir_mensaje(self, mensaje):
        self.guardar_historial(mensaje)
        print(mensaje + '\n')

    def guardar_historial(self, mensaje):
        self.historial.append(mensaje)

    def mostrar_historial(self):
        h = self.historial
        lineas = h[limite_inferior(h):len(h)]
        for linea in lineas:
            print(linea)


def limite_inferior(lista):
    limite_inferior = (len(lista) - 10)

    if (limite_inferior <= 0):
        limite_inferior = 0
    elif (limite_inferior > 0):
        limite_inferior = limite_inferior
    else:
        print("esto no pasa :)")
    return limite_inferior


def epic_buho():
    print("""
    ,___,
    [O.o]   Welcome to Búho chat
    /)__)       Have fun!
    -”–”- 
    """)


if __name__ == '__main__':
    epic_buho()

    servidor = sys.argv[1]
    puerto = sys.argv[2]

    loop = asyncio.get_event_loop()
    cliente = Cliente(loop, servidor, puerto)

    loop.run_until_complete(cliente.loop())
    loop.close()

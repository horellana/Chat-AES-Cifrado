#!/usr/bin/env python

import sys
import asyncio

### Esta funcion es llamada cuando el usuario ingresa un mensaje
### recibe el mensaje y un socket conectado al servidor
### su trabajo es enviar el mensaje
def enviar_mensaje(mensaje, servidor):
    servidor.write(mensaje.encode())


def recibir_mensaje(mensaje):
    print(mensaje.decode())
    
@asyncio.coroutine
def tcp_echo_client(loop, servidor, puerto):
    ### Nos conectamos al servidor
    r, w = yield from asyncio.open_connection(servidor, puerto, loop=loop)

    ### Escuchamos stdin por mensajes enviados por nosotros
    ### (El cliente)
    loop.add_reader(sys.stdin, lambda: enviar_mensaje(sys.stdin.readline(), w))

    while True:
        data = yield from r.read(100)
        recibir_mensaje(data)
        
if __name__ == '__main__':
    print ("""
    ,___,
    [O.o]   Welcome to Búho chat
    /)__)       Have fun!
    -”–”- 
    """)

    servidor = sys.argv[1]
    puerto = sys.argv[2]
    
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(tcp_echo_client(loop, servidor, puerto))
    loop.close()

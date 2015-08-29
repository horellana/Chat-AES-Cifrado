#!/usr/bin/env python

import sys
import random
import asyncio

from Cifrado import Enigma

clientes = []
contador_usuarios = 0

key = sys.argv[1]
enigma = Enigma(key)


# Esta clase la saque de
# https://docs.python.org/dev/library/asyncio-protocol.html#tcp-echo-server-protocol
# Solo la modifique para que guarde a los clientes en la lista `clientes`
class EchoServerClientProtocol(asyncio.Protocol):
    # Esta funcion es llamada cada vez que un nuevo cliente se conecta
    # Aqui creamos un diccionario con los datos (nombre y socket)
    # y lo guardamos en la lista de clientes.
    # me imagino que transport es el socket, pero no estoy seguro.
    def connection_made(self, transport):
        global contador_usuarios
        cliente = {'nombre': 'user{}'.format(contador_usuarios),
                   'transport': transport}
        clientes.append(cliente)
        contador_usuarios = contador_usuarios + 1
        self.cliente = cliente
        self.propagar('{} se a conectado'.format(cliente['nombre']))
    
    def propagar(self, mensaje):
        mensaje = enigma.cifrar(mensaje)
        for cliente in clientes:
            cliente['transport'].write(mensaje)

    # Esta funcion es llamada cuando el cliente envia un mensaje al servidor
    def data_received(self, data):
        data = enigma.decifrar(data).decode()
        # Aqui enviamos el mensaje a todos los clientes conectados
        self.propagar('{}: {}'.format(self.cliente['nombre'], data))

    def connection_lost(self, exc):
        global clientes
        msj = enigma.cifrar('{} Se desconecto'.format(self.cliente['nombre']))
        # Saca al cliente desconectado de la lista ...
        clientes = [c for c in clientes
                    if c['nombre'] != self.cliente['nombre']]
        self.propagar(msj)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    coro = loop.create_server(EchoServerClientProtocol, '', 8888)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

#!/usr/bin/env python

import sys
import asyncio

from Cifrado import Enigma


# Esta clase la saque de
# https://docs.python.org/dev/library/asyncio-protocol.html#tcp-echo-server-protocol
# Solo la modifique para que guarde a los clientes en la lista `clientes`
class ChatServer(asyncio.Protocol):
    # Estas variables son compartidas por todas las instancias
    # de la clase `ChatServer`
    enigma = None
    clientes = []
    contador_usuarios = 0

    def __init__(self, key):
        ChatServer.enigma = Enigma(key)

    # Esta funcion es llamada cada vez que un nuevo cliente se conecta
    # Aqui creamos un diccionario con los datos (nombre y socket)
    # y lo guardamos en la lista de clientes.
    # me imagino que transport es el socket, pero no estoy seguro.
    def connection_made(self, transport):
        cliente = {'nombre': 'user{}'.format(ChatServer.contador_usuarios),
                   'transport': transport}
        ChatServer.clientes.append(cliente)
        ChatServer.contador_usuarios += 1
        self.cliente = cliente
        self.propagar('{} se conecto'.format(cliente['nombre']))

    def propagar(self, mensaje):
        mensaje = self.enigma.cifrar(mensaje)
        for cliente in ChatServer.clientes:
            cliente['transport'].write(mensaje)

    # Esta funcion es llamada cuando el cliente envia un mensaje al servidor
    def data_received(self, data):
        # Aqui enviamos el mensaje a todos los clientes conectados
        self.propagar('{}: {}'.format(self.cliente['nombre'],
                                      self.enigma.decifrar(data)))

    def connection_lost(self, exc):
        # Saca al cliente desconectado de la lista ...
        ChatServer.clientes = [c for c in ChatServer.clientes
                               if c['nombre'] != self.cliente['nombre']]
        self.propagar('{} se desconecto'.format(self.cliente['nombre']))


if __name__ == '__main__':
    key = sys.argv[1]

    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: ChatServer(key), '', 8888)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

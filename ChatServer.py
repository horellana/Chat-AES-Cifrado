#!/usr/bin/env python

import sys
import json
import asyncio
import Cifrado
from Crypto.Util.number import getRandomInteger


# Esta clase la saque de
# https://docs.python.org/dev/library/asyncio-protocol.html#tcp-echo-server-protocol
# Solo la modifique para que guarde a los clientes en la lista `clientes`
class ChatServer(asyncio.Protocol):
    # Estas variables son compartidas por todas las instancias
    # de la clase `ChatServer`
    clientes = []
    contador_usuarios = 0

    def __init__(self):
        self.estado = 'no-key'
        self.cliente = None

    # Esta funcion es llamada cada vez que un nuevo cliente se conecta
    # Aqui creamos un diccionario con los datos (nombre y socket)
    # y lo guardamos en la lista de clientes.
    # me imagino que transport es el socket, pero no estoy seguro.
    def connection_made(self, transport):
        self.nombre_cliente = 'user{}'.format(ChatServer.contador_usuarios)
        self.transport = transport
        ChatServer.clientes.append(self)
        ChatServer.contador_usuarios += 1
        self.propagar('{} se conecto'.format(self.nombre_cliente))

    def propagar(self, mensaje):
        if self.estado == 'key-ready':
            mensaje = self.enigma.cifrar(mensaje)
            for cliente in ChatServer.clientes:
                cliente.transport.write(mensaje)

    # Esta funcion es llamada cuando el cliente envia un mensaje al servidor
    def data_received(self, data):
        if self.estado == 'no-key':
            mensaje = json.loads(data.decode())
            if mensaje['gen-key']:
                generado_cliente = mensaje['key']
                if generado_cliente:
                    secreto = getRandomInteger(10)
                    key = str(pow(generado_cliente, secreto) % Cifrado.modulo)
                    generado = pow(Cifrado.generador, secreto) % Cifrado.modulo

                    if len(key) > 16:
                        key -= key * (len(key) - 16)
                    if len(key) < 16:
                        key += key * int(16 - len(key))

                    self.estado = 'key-ready'
                    self.enigma = Cifrado.Enigma(key)
                    self.transport.write(json.dumps({'gen': generado}).encode())
        
        elif self.estado == 'key-ready':
            # Aqui enviamos el mensaje a todos los clientes conectados
            self.propagar('{}: {}'.format(self.nombre_cliente,
                                          self.enigma.decifrar(data)))

    def connection_lost(self, exc):
        # Saca al cliente desconectado de la lista ...
        ChatServer.clientes = [c for c in ChatServer.clientes if c != self]
        self.propagar('{} se desconecto'.format(self.nombre_cliente))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ChatServer, '', 8888)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

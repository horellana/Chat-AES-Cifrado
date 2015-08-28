#!/usr/bin/env python

import random
import asyncio

clientes = []
contador_usuarios = 0

### Esta clase la saque de 
### https://docs.python.org/dev/library/asyncio-protocol.html#tcp-echo-server-protocol
### Solo la modifique para que guarde a los clientes en la lista `clientes`


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        global contador_usuarios
        cliente = {'nombre': 'user{}'.format(contador_usuarios),
                   'transport': transport}
        clientes.append(cliente)
        contador_usuarios = contador_usuarios + 1
        self.cliente = cliente
    
    def data_received(self, data):
        message = data.decode()

        for cliente in clientes:
            m = '{}: {}'.format(self.cliente['nombre'], message).encode()
            cliente['transport'].write(m)

loop = asyncio.get_event_loop()

coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

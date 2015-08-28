#!/usr/bin/env python

import asyncio

clientes = []

### Esta clase la saque de 
### https://docs.python.org/dev/library/asyncio-protocol.html#tcp-echo-server-protocol
### Solo la modifique para que guarde a los clientes en la lista `clientes`


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('Conexion desde {}'.format(self.peername))
        clientes.append(transport)
        self.transport = transport
    
    def data_received(self, data):
        message = data.decode()

        for cliente in clientes:
            if cliente is self.transport:
                next
            cliente.write('{}: {}'.format(self.peername, message).encode())

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

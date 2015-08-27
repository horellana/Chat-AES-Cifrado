#!/usr/bin/env python

import asyncio

clientes = []


### Esta clase la saque de 
### https://docs.python.org/dev/library/asyncio-protocol.html#tcp-echo-server-protocol
### Solo la modifique para que guarde a los clientes en la lista `clientes`

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        clientes.append(transport)

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        for cliente in clientes:
            cliente.write(data)
        # self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


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

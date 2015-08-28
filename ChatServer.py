#!/usr/bin/env python

import random
import asyncio

clientes = []
contador_usuarios = 0

### Esta clase la saque de 
### https://docs.python.org/dev/library/asyncio-protocol.html#tcp-echo-server-protocol
### Solo la modifique para que guarde a los clientes en la lista `clientes`


class EchoServerClientProtocol(asyncio.Protocol):
    ### Esta funcion es llamada cada vez que un nuevo cliente se conecta
    ### Aqui creamos un diccionario con los datos (nombre y socket)
    ### y lo guardamos en la lista de clientes.
    ### me imagino que transport es el socket, pero no estoy seguro.
    def connection_made(self, transport):
        global contador_usuarios
        cliente = {'nombre': 'user{}'.format(contador_usuarios),
                   'transport': transport}
        clientes.append(cliente)
        contador_usuarios = contador_usuarios + 1
        self.cliente = cliente
    
    ### Esta funcion es llamada cuando el cliente envia un mensaje al servidor
    def data_received(self, data):
        message = data.decode()

        ### Aqui enviamos el mensaje a todos los clientes conectados
        for cliente in clientes:
            m = '{}: {}'.format(self.cliente['nombre'], message).encode()
            cliente['transport'].write(m)


if __name__ == '__main__':
    
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

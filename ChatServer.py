#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

from Crypto.Cipher import AES
from Crypto import Random

key = sys.argv[1]
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)


def cifrar(mensaje):
    global cipher
    return iv + cipher.encrypt(mensaje)

# instanciamos un objeto para trabajar con el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

s.bind(("", 9898)) # escucha los clientes que se dirijan al puerto

s.listen(1)
 
#Instanciamos un objeto sc (socket cliente) para recibir datos, al recibir datos este
#devolvera tambien un objeto que representa una tupla con los datos de conexion: IP y puerto
sc, addr = s.accept()
 
while True:
 
    # Recibe mensaje
    recibido = sc.recv(1024)
 
    # Muestra la IP y el mensaje recibido
    print str(addr[0]) + " dice: ", recibido
 
    # Retorna el mansaje al cliente
    sc.send(recibido)

sc.close() # Cierra socket cliente
s.close() # Cierra socket servidor

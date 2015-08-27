#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import socket

def chat(Host, Port, username):
    s = socket() # Asignamos el socket
    s.connect((Host, Port)) # Conectamos con el servidor
    while True:
        output_data = raw_input("> ")
        if output_data != "":
            try:
                s.send(output_data) 
            except TypeError:
                s.send(bytes(output_data, "utf-8"))

            # Mensaje enviado por el usuario.
            input_data = s.recv(1024)
            if input_data != "":
                print(username+": "+input_data.decode("utf-8") if
                      isinstance(input_data, bytes) else username+": "+input_data)
        if input_data == "salir":
            s.close()
            break
    s.close() # Cierra el socket

def main():
    print """
    ,___,
    [O.o]   Welcome to Búho chat
    /)__)       Have fun!
    -”–”- 

    * Escriba "salir" para finalizar sesión
    """
    username = raw_input("Ingrese su nombre de usuario: ")

    Host = "45.55.180.132"
    Port = 9898
    chat(Host, Port, username)
    print "Chat finalizado."


if __name__ == "__main__":
    main()

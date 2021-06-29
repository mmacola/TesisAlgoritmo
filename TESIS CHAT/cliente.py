# Python program to implement client side of chat room.
import socket
import select
import sys


class Cliente:

    def __init__(self, host='localhost', port=4000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP_address = input('Ingresar ip del servidor (default: localhost): ') or host
        Port = 4000
        self.server.connect((IP_address, Port))
        self.name=input('Ingresá tu email o tu nick: ')
        self.enviar_login()
        self.empezar_chat()

    def enviar_login(self):
        self.send_msg(self.name + "&login")

    def enviar_logoff(self):
        self.send_msg(self.name + "&logoff")

    def send_msg(self, mensaje):
        self.server.send(mensaje.encode('utf-8'))

    def empezar_chat(self):
        while True:
            # maintains a list of possible input streams
            sockets_list = [sys.stdin, self.server]

            """ There are two possible input situations. Either the
            user wants to give manual input to send to other people,
            or the server is sending a message to be printed on the
            screen. Select returns from sockets_list, the stream that
            is reader for input. So for example, if the server wants
            to send a message, then the if condition will hold true
            below.If the user wants to send a message, the else
            condition will evaluate as true"""
            read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

            for socks in read_sockets:
                if socks == self.server:
                    message = socks.recv(2048)
                    print(message.decode('utf-8'))
                    sys.stdout.write("-> ")
                    sys.stdout.flush()

                else:
                    message = sys.stdin.readline()
                    self.procesar_mensaje(message)
                    sys.stdout.write("-> ")
                    sys.stdout.flush()
        self.server.close()

    def procesar_mensaje(self, mensaje):
        if mensaje == 'exit\n':
            self.enviar_logoff()
            self.server.close()
            sys.exit()
        else:
            self.send_msg(mensaje)

if __name__ == "__main__":
    print("************INFORMACION*****************")
    print("'match': Trae el alumno asignado.")
    print("'list': Lista de los alumnos conectados.")
    print("'exit': Sale de la aplicacion.")
    print("****************************************")
    Cliente()
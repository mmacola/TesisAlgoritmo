import socket
import select
import sys
import os
import time
from _thread import start_new_thread
import match
import signal


class Servidor:

    list_of_clients = []
    list_of_nicks = []

    def __init__(self): #El hilo principal ejecuta los siguientes metodos.
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #El indicador SO_REUSEADDR indica al kernel que reutilice un socket local en estado TIME_WAIT, sin esperar a que expire su tiempo de espera natural.
        IP_address = 'localhost'
        Port = 4000

        server.bind((IP_address, Port))
        server.listen(100)
        print('Escuchando conexiones...')

        while True: #Crea un nuevo hilo por cada nuevo cliente que se conecta.
            conn, addr = server.accept()
            Servidor.list_of_clients.append(conn) #Siempre vivo.
            print (addr[0] + " connected")
            start_new_thread(ClienteHilo, (conn,)) #Se inicia un nuevo hilo , que invoca a la clase ClienteHilo. Siempre que While sea True se va a ejecutar.
            #ClienteHilo (conn) esto haria el mismo trabajo que el start new thread, sin hilos, sería de forma secuencial. (MONOHILO)
        conn.close()
        server.close()

    @classmethod
    def broadcast(cls, message, connection):
        for client in cls.list_of_clients:
            if client != connection:
                try:
                    client.send(message)
                except:
                    client.close()
                    remove(client)
                    print('SE ELIMINO A UN CLIENTE!')

    @classmethod
    def remove(cls, connection):
        if connection in cls.list_of_clients:
            cls.list_of_clients.remove(connection)

    @classmethod
    def get_match_info(cls, name):
        mensaje_entero = ''
        pipein, pipeout = os.pipe()
        if os.fork() == 0:
            os.close(pipein)
            cls.match_proccess_invoker(pipeout, name)
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            os.close(pipeout)
            pipein_fd = os.fdopen(pipein)
            messages_read = 0
            mensaje_entero = ''
            contador_exit = 0
            while messages_read < 2:
                msg = pipein_fd.readline()[:-1]
                if msg:
                    mensaje_entero += '\n' + msg
                    messages_read += 1
                contador_exit += 1
                if contador_exit == 5:
                    mensaje_entero = 'No se encontro su match intente mañana'
                    break
            os.close(pipein)

            return mensaje_entero

    @classmethod
    def match_proccess_invoker(cls, pipeout, name):
        msg = match.match(name)  #* Llamo a la funcion match.
        if msg:
            os.write(pipeout, msg.encode('utf-8'))  #* Envio al padre el mensaje en bytes.
        os.close(pipeout)


class ClienteHilo:
    def __init__(self, conn): #El nuevo hilo ejecuta las siguientes instrucciones.
        self.vivo = True
        self.conn = conn
        self.conn.send('Welcome to this chatroom!'.encode('utf-8'))
        self._procesar_hilo() # Se invoca el método "_procesar_hilo"

    def _procesar_hilo(self):
        while self.vivo: #Siempre activo, hasta self.vivo = False. 115
            try:
                message = self.conn.recv(2048) #Se encarga de estar escuchando permanentemente al Socket (Conexion)
                if message:
                    # print(message)
                    self._procesar_mensaje(message.decode('utf-8')) #Se fija que tipo de mensaje es (login/logoff/list/match)
                else:
                    Servidor.remove(conn)
                    self.vivo = False
            except:
                continue

    def _procesar_mensaje(self, mensaje):
        if mensaje.endswith('&login'):
            self.usuario = mensaje.split('&')[0]
            Servidor.list_of_nicks.append(self.usuario)
        elif mensaje.endswith('&logoff'):
            Servidor.remove(self.conn)
            Servidor.list_of_nicks.remove(self.usuario)
            self.vivo = False #Equivalente a "exit" y se finaliza el hilo que comenzo en la linea 96, while self.vivo
            return
        elif mensaje == 'list\n':
            self.conn.send(str(Servidor.list_of_nicks).encode('utf-8'))
        elif mensaje == 'match\n':
            message_to_send = Servidor.get_match_info(self.usuario)
            self.conn.send(message_to_send.encode('utf-8'))
        else:
            message_to_send = "<" + self.usuario + "> " + mensaje
            Servidor.broadcast(message_to_send.encode('utf-8'), self.conn)

if __name__ == "__main__": #1)"Main" Proceso principal con un Hilo principal, este ejecuta varias cosas.
    Servidor()
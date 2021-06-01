import datetime
import os
import pickle
import socket
import sys
import threading

from numpy import mat

import match

#Los sockets funcionan en modo Bloqueante, quiere decir que se queda enchufado a la primer 
#conexion que recibe al momento de conectarse al servidor, el servidor se queda enchufado 
#al primer cliente y el segundo queda a la espera la forma de que esto no suceda es:

print("************INFORMACION*****************")
print("'match': Trae el alumno asignado.")
print("'list': Lista de los alumnos conectados.")
print("'exit': Sale de la aplicacion.")
print("****************************************")

def get_match_info(name):
    	#* Este es el proceso padre el cual invoca al hijo.
    pipein, pipeout = os.pipe()
    if os.fork() == 0:
        os.close(pipein)
        match_proccess_invoker(pipeout, name) 
        #* Si fork == 0 entonces quiere decir que soy el hijo y como soy el hijo ejecuto 
    	#el proceso de buscar el match.
    else:
        os.close(pipeout)
        pipein = os.fdopen(pipein)
        msg = pipein.readline()[:-1]  
		#* Como soy el padre me quedo escuchando el pipe a ver que cuenta mi hijo.
        print(f'{msg}')
        #os.close(pipein)

        #* Como soy el padre me quedo escuchando el pipe a ver que cuenta mi hijo.


def match_proccess_invoker(pipeout, name):
    msg = match.match(name)  #* Llamo a la funcion match.
    print(msg)
    if msg:
        os.write(pipeout, msg.encode('utf-8'))  #* Envio al padre el mensaje en bytes.
    os.close(pipeout)


class Cliente(): #El cliente no hereda de ninguna otra clase.
    """docstring for Cliente"""

    def __init__(self, host="localhost", port=4000): 
		#Inicializamos la clase, con sus valores necesarios Self si mismo, puerto y nombre de cliente.
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        print("Ingresar mail: ")
        self.name=input()  
		#Lo guardo en una variable.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
		#Inicializamos los Sockets y le pasamos la familia del Socket.
        self.sock.connect((str(host), int(port)))  
		#Nos conectamos con el servidor, recibe una tupla, el Host que es un string y un entero 
		#que es el puerto. Acá ya esta establecida la conexión.

        #Este es el hilo, una variable que seran los mensajes recibidos, que tiene como target 
		#una funcion del mismo nombre.
        msg_recv = threading.Thread(target=self.msg_recv)
		#Definimos los metodos, es un hilo que recibe los mensajes y metodo que envia los mensajes.
        msg_recv.daemon = True 
		#Lo inicializamos con un daemon, para que este ligado al hilo principal del programa y 
		#cuando se cierre el programa, el hilo se muera y no que quede como un proceso andando.
        msg_recv.start()

        self.usuarios = []

        self.send_msg(self.name + "&login")

        while True:
			#Mantiene vivo el hilo principal.

            msg = input('->')
            if msg == 'list':
				#Listamos los usuarios.
                print(self.usuarios)
				#Imprimimos la lista de usuarios.
            elif msg == 'match':
                get_match_info(self.name)  
				#*Este proceso a la vez dispara un hijo con el cual se comunica con pipe.
            else:
                if msg == 'exit':
                    self.send_msg(self.name + "&logoff")
                    self.sock.close() 
					#Cerramos la conexión.
                    sys.exit()
					#Salimos.
                else:
                    msg = self.name + ": " + msg
                    self.send_msg(msg) 
					#Enviamos el mensaje.

    def msg_recv(self): 
		#Ahora vamos con la funcion, que va a estar pendiente cuando llegue el mensaje.
        nick = "@" + self.name
        while True:
			#Esta funcion va a estar pendiente de cuando llegue un mensaje.
            try:
                data = self.sock.recv(1024)
				# Aca obtenemos los datos del SOCKET cuando reciba Un mensaje de maximo 1024.
                if data:
					#Si el mensaje, existe, lo imprime. Viene serializado por el mismo socket. 
					#Serializado por el mismo cliente.
                    #El cliente le envia un mensaje serializado al servidor y el servidor lo 
					#devuelve tal cual.
                    new_msg = pickle.loads(data) 
					#Deserializamos el mensaje para poder mostrarlo.

                    self.controlUsuarios(new_msg)

                    if ((new_msg.find('&') == -1) and (new_msg.find('@') == -1)) : 
						#Muestro el mensaje solo si no es un mensaje interno o dirigido a un usuario
						#especifico.
                        print(new_msg)
                    else:
                        if(new_msg.find(nick) != -1):
                            print(new_msg)
            except:
                pass

    def send_msg(self, msg):
		#Definimos la funcion para enviar el mensaje
            self.sock.send(pickle.dumps(msg))
			#Recibe de parametros, el mensaje y le dice al socket  que va a enviar, hay que 
			#serializar el mensaje.

    def controlUsuarios(self, msg):
        if (msg.find('&') != -1): 
			#Busco mensajes internos.
            nombre = msg.split("&")
            if nombre[1] == "login":
                print(nombre[0] + " ha iniciado sesion")
                self.usuarios.append(nombre[0])
                self.sock.send(pickle.dumps(self.name + "&online"))
            if nombre[1] == "logoff":
                print(nombre[0] + " se ha ido")
                self.usuarios.remove(nombre[0])
            if nombre[1] == "online":
                print(nombre[0] + " esta online")
                self.usuarios.append(nombre[0])

c = Cliente()
#Inicializamos o instanciamos en cliente.
import socket
import threading
import sys
import pickle
import datetime

#Python cuando trabaja con sockets, esta en modo Bloqueante, quiere decir que se queda enchufado a la primer conexion que recibe
#al momento de conectarse al servidor, el servidor se queda enchufado al primer cliente y el segundo queda a la espera
#la forma de que esto no suceda es: 

class Cliente(): #el cliente no hereda de ninguna otra clase
	"""docstring for Cliente"""
	print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
	print("Ingresar usuario y legajo: ")
	client_name=input()#Lo guardo en una variable

	def __init__(self, host="localhost", port=4000,name=client_name): #inicializamos la clase, con sus valores necesarios Self si mismo, puerto y nombre de cliente
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Inicializamos los Sockets Le pasamos la familia del Socket y el tipo. TCP o UDP??
		self.sock.connect((str(host), int(port)))#nos conectamos con el servidor, recibe una tupla, el Host que es un string y un entero que es el puerto.
		#aca ya esta establecida la conexion

		#este es el hilo, Una variable que seran los mensajes recibidos, que tiene como target una funcion del mismo nombre
		msg_recv = threading.Thread(target=self.msg_recv) #Definimos los metodos, es un hilo que recibe los mensajes y metodo que envia los mensajes.
		#con que sentido usamos un hilo acá?
		msg_recv.daemon = True #Lo inicializamos con un daemon, para que este ligado al hilo principal del programa y cuando se cierre el programa, el hilo se muera y no que quede como un proceso andando. 
		msg_recv.start()  #aca lo corremos

		self.usuarios = []

		self.send_msg(name + "&login")
		
		while True:#Mantiene vivo el hilo principal.

			msg = input('->')
			if msg == 'list':#listamos los usuarios
				print(self.usuarios)#Imprimimos la lista de Usuarios
			else:
				if msg == 'exit':
					self.send_msg(name + "&logoff")
					self.sock.close() #Cerramos la conexion
					sys.exit()#Salimos
				else:
					msg = name + ": " + msg
					self.send_msg(msg) #Enviamos el mensaje

	def msg_recv(self): #ahora vamos con la funcion, que va a estar pendiente cuando llegue el mensaje.
		nick = "@" + self.client_name
		while True:#Esta funcion va a estar pendiente de cuando llegue un mensaje.
			try:
				data = self.sock.recv(1024)# Aca obtenemos los datos del SOCKET cuando reciba Un mensaje de maximo 1024
				if data:#Si el mensaje, existe, lo imprime. Viene serializado por el mismo socket. Serializado por el mismo cliente. 
					#El cliente le envia un mensaje serializado al servidor y el servidor lo devuelve tal cual
					new_msg = pickle.loads(data) #deserializamos el mensaje para poder mostrarlo

					self.controlUsuarios(new_msg)

					if ((new_msg.find('&') == -1) and (new_msg.find('@') == -1)) : #muestro el mensaje solo si no es un mensaje interno o dirigido a un usuario especifico
						print(new_msg)
					else:
						if(new_msg.find(nick) != -1):
							print(new_msg)

			except:
				pass

	def send_msg(self, msg):#Definimos la funcion para enviar el mensaje
			self.sock.send(pickle.dumps(msg))#Recibe de parametros, el mensaje y le dice al socket  que va a enviar, hay que serializar el mensaje.
#por qué necesitaba serializarlo?
#PROFUNDIZAR UN POCO MAS
	def controlUsuarios(self, msg):
		if (msg.find('&') != -1): #busco mensajes internos
			nombre = msg.split("&")
			if nombre[1] == "login":
				print(nombre[0] + " ha iniciado sesion")
				self.usuarios.append(nombre[0])
				self.sock.send(pickle.dumps(self.client_name + "&online"))
			if nombre[1] == "logoff":
				print(nombre[0] + " se ha ido")
				self.usuarios.remove(nombre[0])
			if nombre[1] == "online":
				print(nombre[0] + " esta online")
				self.usuarios.append(nombre[0])

c = Cliente()#Inicializamos o instanciamos en cliente.
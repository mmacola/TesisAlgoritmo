import socket
import threading
import sys
import pickle
import datetime

#print(datetime.date.today())


class Cliente():
	"""docstring for Cliente"""
	print(datetime.date.today())
	print("ingresar ip del servidor: ")
	srv_host=input()
	print("ingresar usuario")
	client_name=input()

	def __init__(self, host=srv_host, port=4000,name=client_name):
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Le pasamos la familia del Socket y el tipo.
		self.sock.connect((str(host), int(port)))#nos conectamos con el servidor, recibe una tupla, el Host que es un string y un entero que es el puerto.

		msg_recv = threading.Thread(target=self.msg_recv) #Definimos los metodos, es un hilo que recibe los mensajes y metodo que envia los mensajes.

		msg_recv.daemon = True #Lo inicializamos con un daemon, para que este ligado al hilo principal del programa y cuando se cierre el programa, se cierre solo.
		msg_recv.start()
#class person :
	
	#def __init__(self,name,ID,path):
		#self.name = name
		#self.ID = ID
		#self.path = path	
		
		while True:#Mantiene vivo el hilo principal.

			msg = input('->')
			if msg != 'exit':#hay que validar que este mensaje es diferente al de salir.
				msg = name + ": " + msg
				self.send_msg(msg)
				
			else:#De lo contrario cerramos la conexion y salimos.
				self.sock.close()
				sys.exit()

	def msg_recv(self):
		while True:#Esta funcion va a estar pendiente de cuando llegue un mensaje.
			try:
				data = self.sock.recv(1024)#Un mensaje de maximo 1024
				if data:#Si el mensaje, existe, lo imprime. Viene serializado por el mismo cliente o socket.
					
					print(pickle.loads(data))#Al momento de imprimir el mensaje tenemos que deserializarlo.
			except:
				pass

	def send_msg(self, msg):#Definimos la funcion para enviar el mensaje
			self.sock.send(pickle.dumps(msg))#Recibe de parametros, el mensaje y le dice al socket lo que va a enviar, hay que codificar o serializar el mensaje.
		

c = Cliente()#Inicializamos o instanciamos en cliente.
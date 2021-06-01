import socket
import threading
import sys
import pickle
import multiprocessing
import pandas as pd
from multiprocessing import Process
import numpy as np

class Servidor():
	"""docstring for Servidor"""
	def __init__(self, host="localhost", port=4000):
		self.clientes = []
		self.usuarios = []

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#Se instancia de la misma manera.
		self.sock.bind((str(host), int(port))) 
		#Ligamos el puerto al Host, el cliente lo conectamos y en el servidor lo enlazamos, 
		#reciben la misma tupla, con un string que es un string que es el host y un int que es 
		#el numero del puertoaca es donde utiliza el parametro del init del servidor.
		self.sock.listen(10) 
		#Para motivo de demostracion 10 es suficiente.
		self.sock.setblocking(False) 
		#Le decimos que es un socket no bloqueante, le quitamos el bloqueo que trae por defecto.

		aceptar = threading.Thread(target=self.aceptarCon) 
		#Servidor multihilo.
		procesar = threading.Thread(target=self.procesarCon) 
		#Cada vez que esta fc se ejecute crea un nuevo hilo.

		aceptar.daemon = True
		aceptar.start()

		procesar.daemon = True
		procesar.start()

		while True:
			#El ciclo que mantiene vivo el hilo principal.
			msg = input('->')
			if msg == 'exit':
				self.sock.close()
				#Cerramos la conexion al socket y salimos.
				sys.exit()
			if msg == 'list':
				print(self.usuarios)
			elif msg == 'match':
				print("Tu match es: ")
			else:
				pass

	def msg_to_all(self, msg, cliente):
		#Este método lo que hace es que recorre todos los clientes y que el cliente al que le vamos a
		#mandar el mensaje sea distinto al que envía el mensaje.
		for c in self.clientes:
			#Recorremos nuestro arreglo de clientes y por cada cliente validamos que el que
			#envía el msg sea distinto al que lo envía.
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)
				#Si no me puedo comunicar elimino el cliente del arreglo.

	def aceptarCon(self): # ACEPTA CONEXIONES
		print("aceptarCon iniciado")
		while True:
			#Siempre vamos a estar preguntandose cuando un socket se conecte.
			try:
				conn, addr = self.sock.accept()
				#Tenemos la conexion y la direccion , que acepta la conexion.
				conn.setblocking(False) 
				#Le decimos a la conexion que no se bloquee.
				self.clientes.append(conn)
				#Le pasamos la conexion, APPEND añade un dato a la lista.
			except:
				pass

	def procesarCon(self):
		#Es un ciclo infinito.
		print("ProcesarCon iniciado")
		while True:
			if len(self.clientes) > 0:
				#Que a partir de que la cantidad de clientes sea mayor que 0, empieza un For.
				for c in self.clientes:
					#Por cada cliente dentro de nuestro arreglo de clientes, verificamos que haya 
					#recibido un mensaje.
					try: 
						#En self.clientes se guardan los clientes, es una lista.
						data = c.recv(1024)
						if data:
							#Si lo recibió, llamamos a un método que envíe ese mensaje a todos los 
							#demas clientes.
							self.msg_to_all(data,c)
							#Recorrer el arreglo de clientes, y por cada cliente validar que le 
							#haya llegado un mensaje, si le llegó se lo envía a todos los demás.
							self.controlUsuarios(pickle.loads(data)) 
							#Deserializo el mensaje para parsearlo.
					except:
						pass

	def controlUsuarios(self, msg):
		if (msg.find('&') != -1):
			#Busco mensajes internos.
			nombre = msg.split("&")
			if nombre[1] == "login":
				print(nombre[0] + " ha iniciado sesion")
				self.usuarios.append(nombre[0])
			if nombre[1] == "logoff":
				print(nombre[0] + " se ha ido")
				self.usuarios.remove(nombre[0])

s = Servidor()
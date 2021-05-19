import socket
import threading
import sys
import pickle

class Servidor():
	"""docstring for Servidor"""
	def __init__(self, host="0.0.0.0", port=4000):#si le dejo el localhost queda "bloqueado" a recibir solo conexiones que provienen de localhost
												#con el 0.0.0.0 queda abierto a cualquier IP interno o externo
		
		self.clientes = []

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((str(host), int(port))) #aca es donde utiliza el parametro del init del servidor
		self.sock.listen(10)
		self.sock.setblocking(False)

		aceptar = threading.Thread(target=self.aceptarCon)
		procesar = threading.Thread(target=self.procesarCon)
		
		aceptar.daemon = True
		aceptar.start()

		procesar.daemon = True
		procesar.start()

		while True:
			msg = input('->')
			if msg == 'exit':
				self.sock.close()
				sys.exit()
			else:
				pass


	def msg_to_all(self, msg, cliente):
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)

	def aceptarCon(self):
		print("aceptarCon iniciado")
		while True:
			try:
				conn, addr = self.sock.accept()
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass

	def procesarCon(self):
		print("ProcesarCon iniciado")
		while True:
			if len(self.clientes) > 0: #en self.clientes se guardan los clientes, es una lista
				for c in self.clientes:
					try:
						data = c.recv(1024)
						if data:
							self.msg_to_all(data,c)
					except:
						pass
print ("IP DEL SERVIDOR: ")
print (socket.gethostbyname(socket.gethostname()))

s = Servidor()
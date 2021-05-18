import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host,port))#Pasa los datos de conexion
server.listen() #El servidor esta a la escucha de los clientes
print(f"Server running on {host}:{port}")

clients = [] 
usernames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)
def handle_messages(client):
 #Funcion que maneja mensajes de cada cliente

    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def recive_connection():
    while True:
        client, addres = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(addres)}")

        message = f"Servidor: {username} joined the chat! ".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))
        
        #Por cada cliente que se conecte, el servidor va a crear un hilo para que cada cliente tenga una funcion Handdle dedicada a ese cliente
        #Corren al mismo tiempo y manejan los mensajes de c/cliete por separado

        thread = threading.Thread(target=handle_messages, args=(client,))#como es una Tupla se agrega la ","
        thread.start

    recive_connection()
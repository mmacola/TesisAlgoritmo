# um_Trabajo_Final
**Projecto final.**


Se presenta la arquitectura del proyecto.

![ArquitecturaServidor](https://user-images.githubusercontent.com/10929077/115784852-0ab4ae80-a395-11eb-932d-336c8fa7b1e7.png)


******
**MATCH Y CHAT**
******


🛑 **Login** (Autentificación).🛑 <span style="color: red"> Mejorar, esta muy básico.</span>

*************************

🆗 **ALGORITMO DE MATCH**🆗 <span style="color: green"> HECHO!!! ;)!</span>

Lo resolvi utilizando PANDAS.
Abrir respuestasExtranjeros.csv y respuestasAlumnos.csv.
Abro estos archivos .csv y le realizo distintas operaciones. 
El algoritmo del MATCH ya lo programé y se llama MATCH20.py

* Debería resolver como agregarlo a la parte del servidor como funciones o ver de crear un nuevo servidor para que realice estas operaciones.
¿Qué opinan?

*************************

💡 **CHAT** 💡 <span style="color: yellow"> Tengo algo programado, pero habría que retocarlo.</span>

* **SERVIDOR**

Servidor utilizando SOCKET.
server.bind((host,port))#Pasa los datos de conexion
server.listen() #El servidor esta a la escucha de los clientes
Por cada cliente que se conecte, el servidor va a crear un hilo para que cada cliente tenga una funcion "Handdle" dedicada a ese cliente.
Funcion Handdle maneja mensajes de cada cliente
Los hilos corren al mismo tiempo y manejan los mensajes de c/cliete por separado.

* **CLIENTE**

Creamos 2 hilos.
Un hilo para la funcion "Recibir mensajes".
Un hilo para la funcion "Escribir mensajes".
Para que esten corriendo al mismo tiempo

No serian salas, sino MATCH uno a uno. ¿QUE OPINAN? (O hacemos salas y ademas chat uno a uno).


**************************************************************
MAKE?? 

Agregar comandos para compilar.


**************************************************************

<span style="color: blue"> **COMENTARIOS DEL PROFE**</span>

🇯🇵 🇰🇷 🇩🇪 🇨🇳 🇺🇸 🇫🇷 🇪🇸 🇮🇹 🇷🇺 🇬🇧 🇯🇵 🇰🇷 🇩🇪 🇨🇳 🇺🇸 🇫🇷 🇪🇸 🇮🇹 🇷🇺 🇬🇧🇯🇵 🇰🇷 🇩🇪 🇨🇳 🇺🇸 🇫🇷 🇪🇸 🇮🇹 🇷🇺 🇬🇧

Herramientas para usar, Justificar IPC (si uso Multi hilo o multiproceso decir el xq)
Chat, como armarlo (arquitectura con diagrama).

(Creo que como lo programé, puede ser la arquitectura completa, CONFIRMENME)
Solo la izquierda de la arquitectura del diagrama presentado.

Se puede usar las bibliotecas que queramos, pero entender los metodos que tiene y como usarla.



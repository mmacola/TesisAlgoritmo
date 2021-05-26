# um_Trabajo_Final
**Projecto final.**


Se presenta la arquitectura del proyecto.

![ArquitecturaServidor](https://user-images.githubusercontent.com/10929077/115784852-0ab4ae80-a395-11eb-932d-336c8fa7b1e7.png)


******
**MATCH Y CHAT**
******



*************************

🆗 **ALGORITMO DE MATCH**🆗 <span style="color: green"> HECHO!!! ;)!</span>

Utilicé la biblioteca PANDAS,me pareció una buena alternativa para trabajar con los archivos .csv que traía las respuestas del formulario. 

Trabajé los distintos archivos a través de Dataframe (parseo y analizo).

Realicé los cálculos, de las métricas que explicaremos en detalle a continuación, con procesos y cree un nuevo Dataframe por cada dimensión. 

Y con las respuestas obtenidas, las pude cruzar en un Macth, entre la lista de estudiantes extranjeros y estudiantes locales.

Detalle:
https://docs.google.com/document/d/e/2PACX-1vQEeJ-riwPwUHPxhOjtcLMin_WpuUZVRqguq4UTJ_RtQbiKH97mNJ4JtUhfe6mw_ZLeSLBqB9CY20ou/pub

Observación:

Abrir respuestasExtranjeros.csv y respuestasAlumnos.csv (que se encuentran en drive), a traves de url.

Abro estos archivos .csv y le realizo distintas operaciones. 

El algoritmo del MATCH ya lo programé y se llama MATCH20.py.

*************************

💡 **CHAT** 💡 <span style="color: yellow"> </span>

El servidor se queda conectado a una sola conexión y pone en espera las demás. 
Una buena solución que encontré fue llamar al método setblocking (que tiene un booleano, en este caso “False”).

* Socket bloqueante/nobloqueante es un modo. 
* Cuando uso un socket bloqueante, al hacer una llamada a recv() el proceso queda bloqueado hasta que llegan datos. Es algo parecido a leer del teclado (que también puede ser bloqueante o no).
* nda bien cuando sólo manejo un dispositivo asíncrono (socket). El problema se puede resolver con hilos.
* select() permite manejar en un solo punto varios descriptores asíncronos, de modo que cuando lees o escribes en un dispositivo (incluye a los sockets) ya sabes de antemano que hay algo para leer o escribir, de modo que evitas que te bloquee el proceso.
* Si uso select() no hay mucha diferencia entre usar bloqueantes o no. Y puestos a elegir, son preferibles los bloqueantes.

* **SERVIDOR**

Servidor utilizando SOCKET, MULTIHILO.

* server.bind((host,port))#Pasa los datos de conexion
* server.listen() #El servidor esta a la escucha de los clientes
Por cada cliente que se conecte, el servidor va a crear un hilo para que cada cliente tenga una funcion "Handdle" dedicada a ese cliente.
* Funcion Handdle maneja mensajes de cada cliente
* Los hilos corren al mismo tiempo y manejan los mensajes de c/cliete por separado.

* **CLIENTE**

Utilizamos hilos. Dejamos vivo el hilo principal para manejar los mensajes.

Creamos 2 hilos.
Un hilo para la funcion "Recibir mensajes".
Un hilo para la funcion "Escribir mensajes".
Para que esten corriendo al mismo tiempo

Seria una sala de chat, y cuando el cliente pide informacion sobre su Macth, a este le devuelven la información pedida(mail).

**************************************************************

🇯🇵 🇰🇷 🇩🇪 🇨🇳 🇺🇸 🇫🇷 🇪🇸 🇮🇹 🇷🇺 🇬🇧 🇯🇵 🇰🇷 🇩🇪 🇨🇳 🇺🇸 🇫🇷 🇪🇸 🇮🇹 🇷🇺 🇬🇧🇯🇵 🇰🇷 🇩🇪 🇨🇳 🇺🇸 🇫🇷 🇪🇸 🇮🇹 🇷🇺 🇬🇧

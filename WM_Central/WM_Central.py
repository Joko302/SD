import socket 
import threading
import time
import tkinter as tk
import psycopg
import sys
from confluent_kafka import Consumer, KafkaException, KafkaError, Producer


HEADER = 64
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = socket.gethostbyname("0.0.0.0")

FORMAT = 'utf-8'
FIN = "FIN"
MAX_CONEXIONES = 2
listaRiegos={}

def bloquearWS(id_WS,diccionario):
	if diccionario[id_WS]==False:
		diccionario[id_WS]=True
	else:
		diccionario[id_WS]=False
	
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
def recibir_mensaje(cadena,socket):
	prueba=socket.recv(3).decode(FORMAT)
	if prueba==cadena:
	#if socket.recv(3).decode(FORMAT)==cadena:
		socket.recv(1).decode(FORMAT)
		length=int(socket.recv(4).decode(FORMAT))
		socket.recv(1).decode(FORMAT)
		mensaje=socket.recv(length).decode(FORMAT)
		return mensaje
	else:
		return "ERROR"

def escucharMonitor(botones,id_monitor,monitor,ventana,bloqueo,pararCliente):
	global switch
	
	while True:
		mensaje=recibir_mensaje("WSA",monitor)
		if mensaje == "KO":
			bloqueo[id_monitor]=True
			ventana.after(
				0, lambda: botones[id_monitor].config(fg="red")
			)
			
			switch=True
		if mensaje == "OK":
			bloqueo[id_monitor]=False
			ventana.after(
				0, lambda: botones[id_monitor].config(fg="green")
			)
			switch=False
		if mensaje=="ERROR":
			pararCliente.set()
			print("Se ha escuchado incorrectamente al monitor")
			return 
	

def handle_client(monitor, addr,botones,estacionesRegistradas,onOffs,ventana,bloqueo,producer,conexion,cursor):  

	id_monitor=recibir_mensaje("WID",monitor)
	if id_monitor=="ERROR":
		print("Mensaje mal formado")
		monitor.close()
		return
	print(f"WS con la ID {id_monitor} se ha conectado")
	switch=True
	i=0
	for estacion in estacionesRegistradas:
		if estacion[0] == id_monitor:
			switch=False
	
	if switch:
		lista=[]
		lista.append(id_monitor)
		estacionesRegistradas.append(lista)
		ventana.after(
				0, añadirElemento(ventana,id_monitor,onOffs,botones,bloqueo,producer,conexion,cursor)
			)
		#añadirElemento(ventana,id_monitor,onOffs,botones)
		switch=False
	else:
		botones[id_monitor].config(fg="green")
	#botones[id_monitor].config(fg="green")
	pararCliente = threading.Event()
	hilo = threading.Thread(target=escucharMonitor, args=(botones,id_monitor,monitor,ventana,bloqueo,pararCliente),daemon=True)
	hilo.start()
	while True:
		if pararCliente.is_set():
			print(f"Cliente {id_monitor} parado")
			botones[id_monitor].config(fg="gray")
			monitor.close()
			return
		while switch==True:
			if pararCliente.is_set():
				print(f"Cliente {id_monitor} parado")
				botones[id_monitor].config(fg="gray")
				monitor.close()
				return
			time.sleep(0.1)
		if onOffs[id_monitor] and not bloqueo[id_monitor]:
			monitor.send("STP/0004/stop".encode(FORMAT))
			ventana.after(
				0, lambda: botones[id_monitor].config(fg="orange")
			)
			#botones[id_monitor].config(fg="red")

			
			while onOffs[id_monitor]==True:
				if pararCliente.is_set():
					print(f"Cliente {id_monitor} parado")
					botones[id_monitor].config(fg="gray")
					monitor.close()
					return
				time.sleep(0.1)
			monitor.send("STP/0008/continue".encode(FORMAT))

			botones[id_monitor].config(fg="green")

	
	
	
	'''
    print(f"[NUEVA CONEXION] {addr} connected.")
    
	
    connected = True
    while connected:
        opcion = conn.recv(1).decode(FORMAT)
        print(opcion)
        try:
            opcion=int(opcion)
        except:
            print(f"Ha habido un error en la conexión del cliente {addr}")
            conn.close()
            return
        if opcion == 0:
            break
        
        print(f" He recibido del cliente [{addr}] el número: {opcion}")
        conn.send(f"HOLA CLIENTE: Has elegido la opción {opcion}, envíame una cadena de texto.".encode(FORMAT))
           
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == FIN:
                connected = False
            print(f" He recibido del cliente [{addr}] el mensaje: {msg}")
            if opcion == 1:
                print("Enviando el mensaje directamente")
                conn.send(msg.encode(FORMAT))
            if opcion == 2:
                print("Enviando el mensaje al revés")
                conn.send(msg[::-1].encode(FORMAT))
    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()
    '''
'''def presentacion():
	global estacionesRegistradas
	while True:
		 print("Estado de la ")
		time.sleep(0.5)'''
 
def pedirRiego(producer,id_WS,listaRiegos,boton):
	if not listaRiegos[id_WS] and not boton.cget("fg")=="gray":
		print(boton.cget("fg"))
		print(f"Enviando petición de riego de parte de {id_WS}")
		producer.produce(id_WS, value="REGAR", callback=delivery_report)
		listaRiegos[id_WS]=True
	else:
		producer.produce(id_WS, value="PARA", callback=delivery_report)
		listaRiegos[id_WS]=False


def pantallaNueva(ventana,estacionesRegistradas,onOffs,bloqueo,producer):
	global listaRiegos
	botones={}
	for lista in estacionesRegistradas:
		print(f"{lista[0]} se ha conectado anteriormente")
		onOffs[lista[0]] = False
		bloqueo[lista[0]]= False
		listaRiegos[lista[0]]=False
		botones[lista[0]] = tk.Label(
			ventana, 
			text=lista[0], 
			font=("Arial", 8, "underline"), 
			cursor="hand2"  # Hace que el cursor cambie a una mano interactiva
		)
		botones[lista[0]].config(fg="gray")
		botones[lista[0]].pack(pady=5)
		botones[lista[0]].bind("<Button-1>", lambda event, est=lista[0]: bloquearWS(est,onOffs))
		botones[lista[0]].bind("<Button-3>",  lambda event, est=lista[0]: pedirRiego(producer,est,listaRiegos,botones[est]))
	return botones;
		
	#ventana.mainloop()
	#todo
	'''
def recargarPantalla(ventana,estacionesRegistradas,onOffs)
	diccionario.clear()
	for widget in ventana.winfo_children():
        widget.destroy()
	for lista in estacionesRegistradas:
		onOffs.setdefault(lista[0], False) 
		botones[lista[0]]= tk.Label(
			ventana, 
			text=lista[0], 
			font=("Arial", 8, "underline"), 
			cursor="hand2"  # Hace que el cursor cambie a una mano interactiva
		)
		etiqueta_boton.config(fg="gray")
		etiqueta_boton.pack(pady=5)
		etiqueta_boton.bind("<Button-1>",  lambda event: bloquearWS(lista[0],onOffs))
   '''  

def parpadear(label):
    # Obtenemos el color de fondo actual del Label
	color_actual = label.cget("fg")
    
    # Alternamos entre verde y gris
	nuevo_color = "black" if color_actual == "green" else "green"
    
    # Aplicamos el nuevo color
	label.config(fg=nuevo_color)
    
    # Programamos la función para que se vuelva a ejecutar en 500 milisegundos (0.5 segundos)
	return 

def detener_parpadeo(label):
		color_actual = label.cget("fg")
		if color_actual == "black":
			label.config(fg="green")

def riego(peticionesRiego,botones):
	cantidad_regada={}
	while True:
		msg = peticionesRiego.poll(timeout=1.0)
		if msg is None:
			continue
		else:
			message_values = msg.value().decode('utf-8').split(":") #decode?
			
			if message_values[0]==FIN:
				botones[message_values[1]].config(text=message_values[1])
				detener_parpadeo(botones[message_values[1]])
				cantidad_regada[message_values[1]]=0
			else:
				if message_values[1] not in botones:
					continue
				if message_values[1] not in cantidad_regada:
					cantidad_regada[message_values[1]]=0
				cantidad_regada[message_values[1]]=cantidad_regada[message_values[1]]+10
				
				while message_values[1] not in botones:
					time.sleep(1)
				botones[message_values[1]].config(text=f"{message_values[1]} Regando... (Cantidad Regada={cantidad_regada[message_values[1]]})")
				parpadear(botones[message_values[1]])
				
				

def añadirElemento(ventana,elemento,onOffs,botones,bloqueo,producer,conexion,cursor):
	global listaRiegos
	onOffs[elemento] = False
	bloqueo[elemento] = False
	listaRiegos[elemento] = False
	botones[elemento] = tk.Label(
		ventana, 
		text=elemento, 
		font=("Arial", 8, "underline"), 
		cursor="hand2"  # Hace que el cursor cambie a una mano interactiva
	)
	botones[elemento].config(fg="green")
	botones[elemento].pack(pady=5)
	botones[elemento].bind("<Button-1>",  lambda event, est=elemento: bloquearWS(est,onOffs))
	botones[elemento].bind("<Button-3>",  lambda event, est=elemento: pedirRiego(producer,est,listaRiegos,botones[est]))
	cursor.execute(
		"INSERT INTO IDs (id) VALUES (%s);",
		(elemento,)
	)
	conexion.commit()

def start():
	ventana = tk.Tk()
	ventana.title("WM_Central")
	ventana.geometry("1000x500")
	estacionesRegistradas = []
	onOffs={}
	bloqueo={}
	cursor.execute("SELECT id FROM IDs;")
	estacionesRegistradas = cursor.fetchall()
	botones=pantallaNueva(ventana,estacionesRegistradas,onOffs,bloqueo,producer)
	peticionesRiegoHilo=threading.Thread(target=riego,args=(peticionesRiego,botones),daemon=True)
	peticionesRiegoHilo.start()
	hilo = threading.Thread(target=start2,args=(estacionesRegistradas,onOffs,botones,ventana,bloqueo,producer,conexion,cursor),daemon=True)
	hilo.start()
	ventana.mainloop()
	'''
	#hilo = threading.Thread(target=presentacion)
	server.listen()
    #print(f"[LISTENING] Servidor a la escucha en {SERVER}")
	CONEX_ACTIVAS = threading.active_count()-1
	print(CONEX_ACTIVAS)
	while True:
		try:
			conn, addr = server.accept()
		except:
			exit()
		CONEX_ACTIVAS = threading.active_count()
		if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
			thread = threading.Thread(target=handle_client, args=(conn, addr))
			thread.start()
			#print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
			#print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
		else:
			#print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
			conn.send("OOppsss... DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
			conn.close()
			CONEX_ACTUALES = threading.active_count()-1
        '''
def start2(estacionesRegistradas,onOffs,botones,ventana,bloqueo,producer,conexion,cursor):
	
	#hilo = threading.Thread(target=presentacion)
	
	
	server.listen()
	#print(f"[LISTENING] Servidor a la escucha en {SERVER}")

	while True:
		try:
			conn, addr = server.accept()	
	
			

		except:
			exit()

		thread = threading.Thread(target=handle_client, args=(conn, addr,botones,estacionesRegistradas,onOffs,ventana,bloqueo,producer,conexion,cursor),daemon=True)
		thread.start()
			#print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
			#print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
######################### MAIN ##########################

if  (len(sys.argv) == 4 ):
    PORT = sys.argv[1]
    IP_KAFKA = sys.argv[2]
    PORT_KAFKA = sys.argv[3]
else:
	print("Parámetros incorrectos")
	sys.exit()
consumer_config = {
    'bootstrap.servers': f'{IP_KAFKA}:{PORT_KAFKA}',   # Kafka broker
    'group.id': 'my-group',                   # Consumer group id
    'auto.offset.reset': 'earliest',          # Start reading at the earliest offset
    'enable.auto.commit': True                # Enable auto-commit of offsets
}
producer = Producer({
		'bootstrap.servers': f'{IP_KAFKA}:{PORT_KAFKA}'
	})

peticionesRiego = Consumer(consumer_config)
peticionesRiego.subscribe(['peticionesRiego'])
#peticionesRiego.subscribe(['FO'])
ADDR = (SERVER, int(PORT))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
conexion = psycopg.connect(
	host="localhost",
	dbname="mis_ids",
	user="admin",
	password="password",
	port="5432"
)
cursor = conexion.cursor()
cursor.execute("""
	CREATE TABLE IF NOT EXISTS IDs (
		id VARCHAR(8) PRIMARY KEY
	);
""")
conexion.commit()



print("[STARTING] Servidor inicializándose...")


start()

if 'cursor' in locals() and cursor:
    cursor.close()
if 'conexion' in locals() and conexion:
    conexion.close()
    print("\nConexión cerrada correctamente.")


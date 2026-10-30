import socket 
import threading
import tkinter as tk
import sys

HEADER = 64
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = socket.gethostbyname("0.0.0.0")

FORMAT = 'utf-8'
FIN = "FIN"
MAX_CONEXIONES = 2

def bloquearWS(id_WS,diccionario):
	if diccionario[id_WS]==False:
		diccionario[id_WS]=True
	else:
		diccionario[id_WS]=False
	

def recibir_mensaje(cadena,socket):
	prueba=socket.recv(3).decode(FORMAT)
	print(prueba)
	if prueba==cadena:
	#if socket.recv(3).decode(FORMAT)==cadena:
		socket.recv(1).decode(FORMAT)
		length=int(socket.recv(4).decode(FORMAT))
		socket.recv(1).decode(FORMAT)
		mensaje=socket.recv(length).decode(FORMAT)
		return mensaje
	else:
		return "ERROR"

def escucharMonitor(botones,id_monitor,monitor,ventana):
	global switch
	
	while True:
		mensaje=recibir_mensaje("WSA",monitor)
		if mensaje == "KO":
			print("rojo")
			ventana.after(
				0, lambda: botones[id_monitor].config(fg="red")
			)
			
			switch=True
		if mensaje == "OK":
			print("verde")
			ventana.after(
				0, lambda: botones[id_monitor].config(fg="green")
			)
			switch=False
		if mensaje=="ERROR":
			print("Se ha escuchado incorrectamente al monitor")
	

def handle_client(monitor, addr,botones,estacionesRegistradas,onOffs,ventana):  
	id_monitor=recibir_mensaje("WID",monitor)
	if id_monitor=="ERROR":
		print("Mensaje mal formado")
		monitor.close()
		return
	

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
				0, añadirElemento(ventana,id_monitor,onOffs,botones)
			)
		#añadirElemento(ventana,id_monitor,onOffs,botones)
		switch=False
		#todo mas tarde
	#botones[id_monitor].config(fg="green")
	hilo = threading.Thread(target=escucharMonitor, args=(botones,id_monitor,monitor,ventana))
	hilo.start()
	while True:
		
		while switch==True:
			sleep(0.1)
		if onOffs[id_monitor]:
			monitor.send("STP/0004/stop".encode(FORMAT))
			ventana.after(
				0, lambda: botones[id_monitor].config(fg="orange")
			)
			#botones[id_monitor].config(fg="red")

			onOffs[id_monitor]=False
			
			while onOffs[id_monitor]==True:
				sleep(0.1)
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

def pantallaNueva(ventana,estacionesRegistradas,onOffs):
	botones={}
	
	for lista in estacionesRegistradas:
		onOffs[lista[0]] = False
		botones[lista[0]] = tk.Label(
			ventana, 
			text=lista[0], 
			font=("Arial", 8, "underline"), 
			cursor="hand2"  # Hace que el cursor cambie a una mano interactiva
		)
		botones[lista[0]].config(fg="gray")
		botones[lista[0]].pack(pady=5)
		botones[lista[0]].bind("<Button-1>",  lambda event: bloquearWS(lista[0],onOffs))
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

def riego(peticionesRiego,botones):
	while True:
		msg = peticionesRiego.poll(timeout=1.0)
		message_values = loads(msg.value().decode('utf-8')).split(":")
		if message_value[0]==FIN:
			#todo
		else:
			#todo

def añadirElemento(ventana,elemento,onOffs,botones):
	onOffs[elemento] = False
	botones[elemento] = tk.Label(
		ventana, 
		text=elemento, 
		font=("Arial", 8, "underline"), 
		cursor="hand2"  # Hace que el cursor cambie a una mano interactiva
	)
	botones[elemento].config(fg="green")
	botones[elemento].pack(pady=5)
	botones[elemento].bind("<Button-1>",  lambda event: bloquearWS(elemento,onOffs))

def start():
	ventana = tk.Tk()
	ventana.title("WM_Central")
	ventana.geometry("1000x500")
	estacionesRegistradas = []
	onOffs={}
	botones=pantallaNueva(ventana,estacionesRegistradas,onOffs)
	peticionesRiegoHilo=threading.Thread(target=riego,args=(peticionesRiego,botones),daemon=True)
	hilo = threading.Thread(target=start2,args=(estacionesRegistradas,onOffs,botones,ventana))
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
def start2(estacionesRegistradas,onOffs,botones,ventana):
	
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
			thread = threading.Thread(target=handle_client, args=(conn, addr,botones,estacionesRegistradas,onOffs,ventana))
			thread.start()
			#print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
			#print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
		else:
			#print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
			conn.send("OOppsss... DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
			conn.close()
			CONEX_ACTUALES = threading.active_count()-1

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
peticionesRiego = Consumer(consumer_config)
peticionesRiego.subscribe(['peticionesRiego'])
ADDR = (SERVER, int(PORT))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] Servidor inicializándose...")

start()


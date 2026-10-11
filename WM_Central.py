import socket 
import threading
import tkinter as tk

HEADER = 64
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = socket.gethostbyname("0.0.0.0")

FORMAT = 'utf-8'
FIN = "FIN"
MAX_CONEXIONES = 2

def recibir_mensaje(cadena,socket):
	if socket.recv(3)==cadena:
		socket.recv(1)
		length=int(conn.recv(4))
		socket.recv(1)
		mensaje=socket.recv(length)
		return mensaje
	else:
		return "ERROR"

def handle_client(monitor, addr):
	global estacionesRegistradas
	global ventana
	id_monitor=recibir_mensaje("WID",engine)
	if id_monitor=="ERROR":
		print("Mensaje mal formado")
		monitor.close()
		return
	switch=True
	for estacion in estacionesRegistradas:
		if estacion[0] == id_monitor:
			switch=False
	if switch:
		lista=[]
		lista.append(id_engine)
		estacionesRegistradas.append(lista)
		switch=False
		#todo mas tarde
	
	while True:
		#todo
		if False:
			monitor.send("STP/0004/stop")
			#todo
		if False:
			monitor.send("STP/0008/continue")
	
	
	
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

def pantallaNueva(ventana,estacionesRegistradas):
	for widget in ventana.winfo_children():
        widget.destroy()
	for lista in estacionesRegistradas:
		etiqueta_boton = tk.Label(
			ventana, 
			text=lista[0], 
			font=("Arial", 8, "underline"), 
			cursor="hand2"  # Hace que el cursor cambie a una mano interactiva
		)
		etiqueta_boton.pack(pady=5)
	ventana.mainloop()
	#todo

def start():
	ventana = tk.Tk()
	ventana.title("WM_Central")
	ventana.geometry("1000x500")
	estacionesRegistradas = [[]]
	pantallaNueva(ventana,estacionesRegistradas)
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
        

######################### MAIN ##########################

if  (len(sys.argv) == 4 ):
    PORT = sys.argv[1]
else:
	return
    
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] Servidor inicializándose...")

start()


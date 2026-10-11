import socket 
import threading


HEADER = 64
FORMAT = 'utf-8'
MAX_CONEXIONES = 2
IP=socket.gethostbyname("0.0.0.0")

'''
def handle_client(conn, addr):
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
    
'''def comprobarAvería(engine,central):
	global estado
	if conn.recv(3)!="WSA":
		print("Mensaje del engine incorrecto")
		conn.close()
		return
	conn.recv(1)
	length=int(conn.recv(4))
	conn.recv(1)
	mensaje=conn.recv(length)
	if mensaje!=estado:
		#todo
		estado=mensaje
	else:
		
	'''#idea
def recibir_mensaje(cadena,socket):
	if socket.recv(3)==cadena:
		socket.recv(1)
		length=int(conn.recv(4))
		socket.recv(1)
		mensaje=socket.recv(length)
		return mensaje
	else:
		return "ERROR
def escucharCentral(central,engine):
	if recibir_mensaje("STP",central)=="stop":
		engine.send("STP/0004/stop")
	if recibir_mensaje("STP",central)=="continue":
		engine.send("STP/0008/continue")

def start():
	central.send(f"WID/0008/{ID}")
	estado="OK"
	engine.listen()
	print("Comprobando estado de la máquina")
	thread = threading.Thread(target=escucharCentral, args=(central,engine))
    thread.start()
	while True:
	if engine.recv(3)=="WSA":
		engine.recv(1)
		length=int(conn.recv(4))
		engine.recv(1)
		mensaje=conn.recv(length)
		print(f"Recibido mensaje: {mensaje}")
		if mensaje!=estado:
			central.send("WSA/0002/{estado}")
			print("Mandando mendaje a central...")
			estado=mensaje
		
	#thread = threading.Thread(target=comprobarAvería, args=(engine,central))
    #thread.start()
	'''
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
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
            print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        else:
            print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
            conn.send("OOppsss... DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
            conn.close()
            CONEX_ACTUALES = threading.active_count()-1
        '''

######################### MAIN ##########################

#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = socket.gethostbyname("0.0.0.0")

if  (len(sys.argv) == 5):
	PORT_MON = sys.argv[1]
	
    IP_Central = sys.argv[2]
    PORT_Central = int(sys.argv[3])
    ID=sys.argv[4]
    ADDR_Central = (IP_Central, PORT_Central)
    if len(ID) != 8:
		print("La ID se debe componer de 8 números")
		return
    central = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    central.connect(ADDR_Central)
else:
	return
ADDR_Monitor = (IP, PORT_MON)
engine = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
engine.bind(ADDR_Monitor)


print("[STARTING] Servidor inicializándose...")

start()


import socket
import threading
import time
import sys

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
FIN = "FIN"


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
########## MAIN ##########

def OKorKO(client):
	global estado
	while True:
		client.send(f"WSA/0002/{estado}".encode(FORMAT))
		time.sleep(1)

def recibir_mensaje(cadena,socket):
	if socket.recv(3).decode(FORMAT)==cadena:
		socket.recv(1).decode(FORMAT)
		length=int(socket.recv(4).decode(FORMAT))
		socket.recv(1).decode(FORMAT)
		mensaje=socket.recv(length).decode(FORMAT)
		return mensaje
	else:
		return "ERROR"

def blockEngine(client):
	global block
	if recibir_mensaje("STP",client)=="stop":
		print("Recibiendo mensaje para parar la WS")
		block=True
	if recibir_mensaje("STP",client)=="continue":
		print("Recibiendo mensaje para continuar la WS")
		block=False
		


print("****** WELCOME TO OUR BRILLIANT SD UA CURSO 2020/2021 SOCKET CLIENT ****")

def regar(encender_evento):
	while True:
		if encender_evento.is_set():
			#todo
			encender_evento.clear()
		

if  (len(sys.argv) == 5):
	SERVER = sys.argv[3]
	PORT = int(sys.argv[4])
	ADDR = (SERVER, PORT)
    
	block=False
    
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
	print (f"Establecida conexión en [{ADDR}]")

	option=1
	estado="OK"
	thread = threading.Thread(target=OKorKO, args=(client,))
	thread.daemon=True
	thread.start()
	thread2=threading.Thread(target=blockEngine, args=(client,))
	thread2.daemon=True
	thread2.start()
	encender_riego=threading.Event()
	threadRegar=threading.Thread(target=Regar, args=(encender_riego,),daemon=True)
	threadRegar.start()
	while True :
		if option=="r":
			encender_riego.set()
		while option!="a":
			print("Pulse A para averiar la WS")
			try:
				option=input()
			except:
				break;

			if option=="a":
				print("Enviando KO")
				estado="KO"
				option="b"
				break
		while option!="a":
			encender_riego.clear()
			print("Pulse A para arreglar la WS")
			try:
				option=input()
			except:
				break;

		if option=="a":
			print("Enviando OK")
			estado="OK"
			option="b"
	print("Desconectandose del monitor")
	#print("Envio al servidor: ", FIN)
	#send(FIN)
	client.close()
else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos: <ServerIP> <Puerto> <Texto Bienvenida>")

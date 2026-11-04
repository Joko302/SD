import socket
import threading
import time
import sys
from confluent_kafka import Producer, Consumer
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
FIN = "FIN"

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
        
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
	while True:
		if recibir_mensaje("STP",client)=="stop":
			print("Recibiendo mensaje para parar la WS")
			block=True
		if recibir_mensaje("STP",client)=="continue":
			print("Recibiendo mensaje para continuar la WS")
			block=False
		


print("****** WELCOME TO OUR BRILLIANT SD UA CURSO 2020/2021 SOCKET CLIENT ****")

def regar(encender_evento,producer,id_monitor):
	regado=0;
	while True:
		if encender_evento.is_set():
			
			print("Regando 10ml")
			regado=regado+10
			print(f"Cantidad regada: {regado}")
			producer.produce('peticionesRiego', value=f"REGAR:{id_monitor}", callback=delivery_report)
			time.sleep(0.5)
			#todo
			#encender_evento.clear()
			if not encender_evento.is_set():
				producer.produce('peticionesRiego',value=f"FIN:{id_monitor}",)
		else:
			regado=0
			time.sleep(0.5)

def PeticionRiego(peticionesRiego,encender_riego):
	global block
	global estado
	while True:
		msg = peticionesRiego.poll(timeout=1.0)
		if msg is None:
			continue
		else:
			
			message_value = msg.value().decode('utf-8')
			print(f"Se ha recibido {message_value}")
			if message_value=="REGAR":
				if not block and estado=="OK":
					encender_riego.set()
			if message_value=="PARA":
				encender_riego.clear()

if  (len(sys.argv) == 5):
	KAFKA_IP=sys.argv[1]
	KAFKA_PORT=sys.argv[2]	
	producer = Producer({
		'bootstrap.servers': f'{KAFKA_IP}:{KAFKA_PORT}'
	})
	consumer_config = {
		'bootstrap.servers': f'{KAFKA_IP}:{KAFKA_PORT}',   # Kafka broker
		'group.id': 'my-group',                   # Consumer group id
		'auto.offset.reset': 'earliest',          # Start reading at the earliest offset
		'enable.auto.commit': True                # Enable auto-commit of offsets
	}
	peticionesRiego = Consumer(consumer_config)
	SERVER = sys.argv[3]
	PORT = int(sys.argv[4])
	ADDR = (SERVER, PORT)
    
	block=False
    
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
	
	id_monitor=recibir_mensaje("WID",client)
	peticionesRiego.subscribe([id_monitor])
	
	print (f"Establecida conexión en [{ADDR}] con la ID {id}")

	option=1
	estado="OK"
	thread = threading.Thread(target=OKorKO, args=(client,),daemon=True)
	thread.daemon=True
	thread.start()
	thread2=threading.Thread(target=blockEngine, args=(client,),daemon=True)
	thread2.daemon=True
	thread2.start()
	encender_riego=threading.Event()
	threadRegar=threading.Thread(target=regar, args=(encender_riego,producer,id_monitor),daemon=True)
	threadRegar.start()
	threadPeticionRiego=threading.Thread(target=PeticionRiego, args=(peticionesRiego,encender_riego),daemon=True)
	threadPeticionRiego.start()
	while True :
		print("Pulse A para averiar la WS o R para regar")
		while option!="a":
			try:
				option=input()
			except:	

				break;
			if block:
				while block:
					print("Central ha bloqueado la WS")
					time.sleep(1)
			elif option=="a":
				print("Enviando KO")
				estado="KO"
				option="b"
				break
			elif option=="r" and not block:
				encender_riego.set()
			elif option=="s":
				encender_riego.clear()
		while option!="a":
			if block:
				while block:
					print("Central ha bloqueado la WS")
					time.sleep(1)
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
    print ("Oops!. Parece que algo falló. Necesito otros argumentos")

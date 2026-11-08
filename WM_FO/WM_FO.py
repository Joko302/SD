import socket 
import threading
import sys
import time
from confluent_kafka import Producer

def Regar(riega):
	cantidad_regada=0
	while True:
		if riega.is_set():
			producer.produce("peticionesRiego", value=f"REGAR:{ID_WS}")
			cantidad_regada=cantidad_regada+10
			print(f"Se ha regado un total de {cantidad_regada}ml")
			time.sleep(0.5)
		else:
			cantidad_regada=0
			continue

def start():
	riega=threading.Event()
	thread = threading.Thread(target=Regar, args=(riega,),daemon=True)
	thread.start()
	cantidad_regada=0
	while True:
		print("Presiona r para regar o l para leer el archivo instrucciones.txt")
		option=input()
		if option=="l":
			with open("mi_archivo.txt", "r", encoding="utf-8") as archivo:
				for linea in archivo:
					numPeticiones=round(int(linea.strip())/10)
					while numPeticiones>=0:
						producer.produce("peticionesRiego", value=f"FIN:{ID_WS}")
						numPeticiones=numPeticiones-1
					
		if option=="r":

			print("Presiona s para parar")
			riega.set()
			while option!="s":
				option=input()
				if option=="s":
					riega.clear()
					producer.produce("peticionesRiego", value=f"FIN:{ID_WS}")

if  (len(sys.argv) == 4):
	IP_KAFKA = sys.argv[1]
	PORT_KAFKA = sys.argv[2]
	ID_WS = sys.argv[3]
	
	if len(ID_WS) != 8:
		print("La ID se debe componer de 8 números")
		sys.exit()
else:
	sys.exit()

producer = Producer({
	'bootstrap.servers': f'{IP_KAFKA}:{PORT_KAFKA}'
})

print("[STARTING] Servidor inicializándose...")

start()


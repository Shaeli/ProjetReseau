#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, sys

TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 50



def client(): #Fonction client
	print("Connexion sur le port " + str(TCP_PORT) + "\n") 
	print("Adresse IP : " + str(TCP_IP) + "\n")

	while True: #Boucle communication simple
		#print('<client>')
		data = input("<client>")
		if data == "quit":
			break
		send(sock, data)
		data = sock.recv(BUFFER_SIZE).decode("Utf-8")
		print('<server>',str(data))

	sock.close()

#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))

if __name__ == '__main__': #Connexion et appel à la fonction client
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((TCP_IP, TCP_PORT))
	except:
		sys.exit()
	client()
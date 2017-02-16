#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, sys

TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 50

def commandes_client():
	sock.send("commandes")
	mess=raw_input("Tapez la commande que vous voulez effectuer.\nSont actuellement supportés les commandes ls et cd")
	mess=mess.rstrip()
	if mess == "cd":
		sock.send(mess)
	elif mess == "ls":
		sock.send(mess)
	else:
		print("Cette commande n'est pas supporte pour le moment! Revenez plus tard.")



def client(): #Fonction client
	print("Connexion sur le port " + str(TCP_PORT) + "\n") 
	print("Adresse IP : " + str(TCP_IP) + "\n")

	while True: #Boucle communication simple
		sys.stdout.write('<client>')
		data = sys.stdin.readline()
		if data == "quit\n":
			break
		elif data == "commandes":
			commandes_client()
		sock.send(data)
		data = sock.recv(BUFFER_SIZE)
		sys.stdout.write('<server>')
		sys.stdout.write(data)

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
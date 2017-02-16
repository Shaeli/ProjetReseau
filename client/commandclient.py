#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, sys

TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 2048

def commandes_client(sock):
	sock.send("commandes")
	mess=raw_input("Tapez la commande que vous voulez effectuer.\nSont actuellement supportés les commandes ls et cd\n")
	mess=mess.rstrip()
	if mess[0] == "cd":
		print 'ouii'
		send(sock,mess)
	elif mess == "ls":
		send(sock,mess)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		sys.stdout.write('<server>')
		sys.stdout.write(data)
	else:
		print("Cette commande n'est pas supporte pour le moment! Revenez plus tard.")



#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))
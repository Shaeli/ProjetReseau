#!/usr/bin/python
# -*-coding:Utf8 -*
from getpass import getpass
import socket, sys
import md5

TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 2048

def commandes_client(sock,mess):


	#Listes des fonctions implémentées
	if mess[0] == "cd":
		chn = " ".join(mess)
		send(sock,chn)
	elif mess[0] == "ls":
		chn = " ".join(mess)
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		sys.stdout.write('<server>')
		sys.stdout.write(data)
	elif mess[0] == "cat":
		chn = " ".join(mess)
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		sys.stdout.write('<server>')
		sys.stdout.write(data)
	elif mess[0] == "mv":
		chn = " ".join(mess)
		send(sock,chn)
	
#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))
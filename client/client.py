#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, sys
import commandclient
import md5
from getpass import getpass

TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 4024

def client(): #Fonction client
	print("Connexion sur le port " + str(TCP_PORT) + "\n") 
	print("Adresse IP : " + str(TCP_IP) + "\n")

	id_cli = raw_input("ID : ")
	send(sock,id_cli)
	mdp_cli = getpass("mdp : ")
	mdp_hash = md5.new(mdp_cli).hexdigest()
	send(sock,str(mdp_hash))

	if sock.recv(BUFFER_SIZE) == "access granted":
		print "acces autorisé"
		while True: #Boucle communication simple
			sys.stdout.write('<client>')
			data = sys.stdin.readline()
			data=data.rstrip()
			if data == "quit":
				break
			elif data == "commandes":
				commandclient.commandes_client(sock)
			elif data == "ajout utilisateur":
				commandclient.utilisateur(sock)
			else:	
				send(sock,data)

	else:
		print "mauvais mot de passe connexion annulee"
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

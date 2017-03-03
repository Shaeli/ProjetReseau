#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, sys
import commandclient
import md5, ssl
from getpass import getpass
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 8099
BUFFER_SIZE = 1024

def client(): #Fonction client
	print("Connexion sur le port " + str(TCP_PORT) + "\n") 
	print("Adresse IP : " + str(TCP_IP) + "\n")

	ssl_sock.getpeername()
	ssl_sock.cipher()

	#Connexion via id et mdp
	id_cli = raw_input("ID : ")
	send(ssl_sock, id_cli)
	mdp_cli = getpass("mdp : ")
	mdp_hash = md5.new(mdp_cli).hexdigest()
	send(ssl_sock,str(mdp_hash))

	#Si on accepte l'accès au serveur
	if sock.recv(BUFFER_SIZE) == "access granted":
		print "acces autorisé"

		#Boucle communication simple finie
	while True: 
		#Récupération des données
		data = input("<serveur>")
		data=data.rstrip()
		data=data.split(" ")
		#Si quit, on quitte le prgramme en fermant la socket
		if data == "quit":
			break
		#Si commandes, on lance l'état commande chez le client
		elif data[0] == "ls" or data[0] == "cd" or data[0] == "mv" or data[0] == "cat":
			send(ssl_sock,"commandes")
			time.sleep(0.1)
			commandclient.commandes_client(ssl_sock,data)
		#Sinon on envoit les données écrites au serveur
		else:

			send(ssl_sock,"reponse serveur")

	else:
		print "mauvais mot de passe connexion annulee"

	#Fermeture de la socket
	sock.close()

#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))

if __name__ == '__main__': #Connexion et appel à la fonction client
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssl_sock = ssl.wrap_socket(sock, 
								ca_certs = "server/sslcertif/server.crt",
								cert_reqs = ssl.CERT_REQUIRED)
	ssl_sock.connect((TCP_IP, TCP_PORT))
	client()
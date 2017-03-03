#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, sys
import commandclient
import md5
from getpass import getpass
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 2048

def client(): #Fonction client
	print("Connexion sur le port " + str(TCP_PORT) + "\n") 
	print("Adresse IP : " + str(TCP_IP) + "\n")
	acces = "access denied"
	while acces == "access denied" :
	#Connection via id et mdp
		id_cli = raw_input("ID : ")
		send(sock,id_cli)
		mdp_cli = getpass("mdp : ")
		mdp_hash = md5.new(mdp_cli).hexdigest()
		send(sock,str(mdp_hash))

	#Si on accepte l'accès au serveur
		acces = sock.recv(BUFFER_SIZE)
		if acces == "stop" :
			print "mauvais mot de passe consécutifs, connexion annulee"
			sock.close()
		if acces == "access granted" :
			en_route()


def en_route():
	while True : 
		sys.stdout.write('<client>')
	#Récupération des données
		data = sys.stdin.readline()
		data = data.rstrip()
		data = data.split(" ")
	#Si quit, on quitte le prgramme en fermant la socket
		if data == "quit":
			break
	#Si commandes, on lance l'état commande chez le client
		elif data[0] == "ls" or data[0] == "cd" or data[0] == "mv" or data[0] == "cat":
			send(sock,"commandes")
			time.sleep(0.1)
			commandclient.commandes_client(sock,data)
	#Sinon on envoit les données écrites au serveur
		else:	
			send(sock,data)

	#Fermeture de la socket

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

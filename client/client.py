#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, sys
import commandclient
import md5, ssl
from getpass import getpass
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 8099
BUFFER_SIZE = 2048

id_cli=""

def client(): #Fonction client
	global id_cli
	print("Connexion sur le port " + str(TCP_PORT) + "\n") 
	print("Adresse IP : " + str(TCP_IP) + "\n")
	acces = "access denied"
	while acces == "access denied" :
	#Connection via id et mdp
		id_cli = raw_input("ID : ")
		send(ssl_sock,id_cli)
		mdp_cli = getpass("mdp : ")
		mdp_hash = md5.new(mdp_cli).hexdigest()
		send(ssl_sock,str(mdp_hash))

		acces = ssl_sock.recv(BUFFER_SIZE)
		if acces == "stop" : #trop de tentatives de connexions echoues, on coupe la connexion
			print "mauvais mot de passe consécutifs, connexion annulee"
			sock.close()
			break
		if acces == "access granted" : 	#Si on accepte l'accès au serveur

			en_route()
			break
		print "mauvaise combinaison ID/MdP, veuillez reessayer"


def en_route():
	while True : 
		if id_cli != "root" :
			sys.stdout.write(id_cli + ":~" + commandclient.path + "$" + " ")
		else :
			sys.stdout.write(id_cli + ":~" + commandclient.path + "#" + " ")
	#Récupération des données
		data = sys.stdin.readline()
		data = data.rstrip()
		data = data.split(" ")
	#Si quit, on quitte le prgramme en fermant la socket
		if data[0] == "quit":
			print("\nFermeture de la socket client\n")
			break
	#Si commandes, on lance l'état commande chez le client
		elif data[0] == "ls" or data[0] == "cd" or data[0] == "mv" or data[0] == "cat" or data[0] == "rm" or data[0] == "touch" or data[0] == "add" or data[0] == "mkdir" or data[0] == "vim" :
			send(ssl_sock,"commandes")
			time.sleep(0.1)
			commandclient.commandes_client(ssl_sock,data)

	#Fermeture de la socket
	sock.close()
	ssl_sock.close()

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
#!/usr/bin/python
# -*-coding:Utf8 -*

import socket
from threading import Thread
from socket import error as SocketError
import errno
import Command
import md5

BUFFER_SIZE = 2048

#Classe de thread d'un client
class ClientThread(Thread):

	def __init__(self, ip, port, clientsocket):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.clientsocket = clientsocket
		passages = 0
		#Tentative de connection du client via id et mdp 
		while passages < 4 : #apres 4 tentatives echouees, la connexion est refusée
			id_cli = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			mdp_cli = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			self.path = "./data"
			user_base = open("server/ressources/users.bdd","r")

			accepted = False
			for line in user_base.read().split("\n"):
				(id_base, mdp_base) = line.split(';')
				if (id_base == id_cli and mdp_base == mdp_cli):
					accepted = True
			user_base.close()
			if accepted:	
				self.send("access granted") #acces accorde au client
				passages = 8

			else:
				if passages == 3 :
					self.send("stop") #trop de tentatives echoues : on coupe la connexion
				else:
					self.send("access denied") #tentative echoue : on donne la chance au client de retenter

			print("Nouveau client : "+ id_cli + " sur : " + ip + " " + str(port))
			passages=passages+1
	#Fonction de boucle infinie
	def run(self):
		while 1:
			data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8") #recupération de la connection
			if data == "commandes" :
				Command.commandes_server(self,self.clientsocket)
			if not data: 
				print("Plus de données, on sort !")
				break

	#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
	def send(self, message):
		self.clientsocket.send(message.encode("Utf8"))
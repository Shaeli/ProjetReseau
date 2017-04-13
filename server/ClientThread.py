#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, os, errno, Command, md5, ssl
from threading import Thread
from socket import error as SocketError

BUFFER_SIZE = 2048

#Classe de thread d'un client
class ClientThread(Thread):
	Thread_name = ""
	def __init__(self, ip, port, clientsocket):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.clientsocket = clientsocket

		rights = ""
		passages = 0
		#Tentative de connection du client via id et mdp 
		while passages < 4 : #apres 4 tentatives echouees, la connexion est refusée
			self.id_cli = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			self.id_cli=self.id_cli[1:]
			mdp_cli = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			self.mdp = mdp_cli
			self.path = "./data"
			user_base = open("server/ressources/users.bdd","r")

			accepted = False
			for line in user_base.read().split("\n"):
				(id_base, mdp_base, rghts) = line.split(';')
				if (id_base == self.id_cli and mdp_base == mdp_cli):
					accepted = True
					rights = rghts
			user_base.close()
			if accepted:	
				self.send("access granted") #acces accorde au client
				print("Nouveau client : "+ self.id_cli + " sur : " + ip + " " + str(port) + ", droits de type " + str(rights))
				self.Thread_name = self.id_cli
				self.rights = str(rights)
				passages = 8

			else:
				if passages == 3 :
					self.send("stop") #trop de tentatives echoues : on coupe la connexion
					clientsocket.close()

				else:
					self.send("access denied") #tentative echoue : on donne la chance au client de retenter

			passages+=1


	#Fonction de boucle infinie
	def run(self):
		while self.Thread_name!="":
			liste = []
			for (repertoire, sousRepertoires, fichiers) in os.walk(self.path):
 				liste.extend(fichiers)
 				liste.extend(sousRepertoires)
 			completion= " ".join(liste)
 			self.send(completion)
			data = self.clientsocket.recv(BUFFER_SIZE) #recupération de la connection

			if data == "commandes" :
				Command.commandes_server(self,self.clientsocket)
			if not data: 
				print self.Thread_name + " s'est deconnecte"
				break


	#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
	def send(self, message):
		self.clientsocket.send(message.encode("Utf8"))
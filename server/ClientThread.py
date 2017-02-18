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

	def __init__(self, ip, port, clientsocket,user_list):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.clientsocket = clientsocket
		id_cli=self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
		mdp_cli=self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
		#mdp_hash=md5.new(mdp_cli).hexdigest()
		#print "mot de passe recu : " + mdp_cli
		#print "mot de passe BDD : " + user_list[id_cli]
		#print "mot de passe hache " + str(md5.new("azerty").hexdigest())
		if (user_list.has_key(id_cli) and str(md5.new(user_list[id_cli]).hexdigest())==mdp_cli):
			self.send("access granted")
		else:
			self.send("access denied")
		print("Nouveau client : "+ id_cli + " sur : " + ip + " " + str(port))

	#Fonction de boucle infinie
	def run(self):
		while 1:
			data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8") #recupération de la connection
			if data == "commandes" :
				Command.commandes_server(self,self.clientsocket)
			if not data: 
				print("Plus de données, on sort !")
				break

			#self.send(data) #Echo

	#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
	def send(self, message):
		self.clientsocket.send(message.encode("Utf8"))
#!/usr/bin/python
# -*-coding:Utf8 -*

import socket
from threading import Thread
from socket import error as SocketError
import errno

BUFFER_SIZE = 1024

#Classe de thread d'un client
class ClientThread(Thread):

	def __init__(self, ip, port, clientsocket):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.clientsocket = clientsocket
		print("Nouveau client " + ip + " " + str(port))

	#Fonction de boucle infinie
	def run(self):
		while 1:
			data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8") #recupération de la connection
			print(data)
			if not data: 
				print("Plus de données, on sort !")
				break

			self.send(data) #Echo

	#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
	def send(self, message):
		self.clientsocket.send(message.encode("Utf8"))
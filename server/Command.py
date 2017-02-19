#!/usr/bin/python
# -*-coding:Utf8 -*

import socket
from socket import error as SocketError
import errno
from os import chdir
from os import system
import os
from getpass import getpass
BUFFER_SIZE = 2048

def commandes_server(self,clientsocket):
	tampon = " "
	data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
	if data == "ls":
		res = os.popen("/bin/ls").readlines()
		for mot in res :
			tampon = tampon + mot
		send(self,tampon,clientsocket)
		send(self,"\n",clientsocket)
		del tampon
	if data[0] == "cd" :
		print 'cd en cours'
		os.system(data)
def gestion_base(self,clientsocket):
	print "yolo"
	id_new=clientsocket.recv(BUFFER_SIZE).decode("Utf8")
	base=open("user_base.txt","a")
	base.write("\n"+id_new)
	print "ajout de "+id_new.split(";")[0]+" a la base de donnee"
	base.close()

#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
def send(self, message,clientsocket):
	self.clientsocket.send(message.encode("Utf8"))
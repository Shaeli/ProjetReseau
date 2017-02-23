#!/usr/bin/python
# -*-coding:Utf8 -*

import socket
from socket import error as SocketError
import errno
from os import chdir
from os import system
import os
from getpass import getpass

BUFFER_SIZE = 4024

def commandes_server(self,clientsocket):
	tampon = " "
	data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
	data=data.split(" ")
	if data[0] == "ls":
		chn = " ".join(data)
		res = os.popen(chn).readlines()
		for mot in res :
			tampon = tampon + mot
		send(self,tampon,clientsocket)
		send(self,"\n",clientsocket)
		del tampon
	if data[0] == "cd" :
		os.chdir(data[1])
	if data[0] == "cat" :
		chn = " ".join(data)
		res = os.popen(chn).readlines()
		for mot in res :
			tampon = tampon + mot
		send(self,tampon,clientsocket)
		send(self,"\n",clientsocket)
		del tampon
	if data[0] == "mv" :
		chn = " ".join(data)
		os.system(chn)


def gestion_base(self,clientsocket):
	id_new=clientsocket.recv(BUFFER_SIZE).decode("Utf8")
	base=open("user_base.txt","a")
	base.write("\n"+id_new)
	print "ajout de "+id_new.split(";")[0]+" a la base de donnee"
	base.close()

#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
def send(self, message,clientsocket):
	self.clientsocket.send(message.encode("Utf8"))
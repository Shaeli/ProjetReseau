#!/usr/bin/python
# -*-coding:Utf8 -*

import socket
from socket import error as SocketError
import errno
from os import chdir
from os import system
import os
from getpass import getpass

BUFFER_SIZE = 1024

def commandes_server(self,clientsocket):
	tampon = ""
	data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
	data=data.split(" ")
	if data[0] == "ls":
		chn = " ".join(data)
		chn = chn + " " + self.path
		res = os.popen(chn).readlines()
		for mot in res :
			tampon = tampon + mot
		send(self,tampon,clientsocket)
		send(self,"\n",clientsocket)
		del tampon

	elif data[0] == "cd" :
		ls ="ls" + " " + self.path
		lst = os.popen(ls).readlines()
		for i, item in enumerate(lst) :
			lst[i] = item.rstrip()
		if (data[1] in lst) or (data[1] == "..") :
			if data[1] == ".." :
				if self.path != "./data" :
					path=self.path.split("/")
					self.path=""
					for i in range(0,len(path)-1):
						self.path=self.path+path[i]
						self.path=self.path+"/"
			else :
				self.path = self.path + "/" + data[1]
		else :
			print("pas de changement de path car cd pas bon")
	elif data[0] == "cat" :
		ls ="ls" + " " + self.path
		lst = os.popen(ls).readlines()
		for i, item in enumerate(lst) :
			lst[i] = item.rstrip()
		if (data[1] in lst) :
			data[1] = self.path+"/"+data[1]
			chn = " ".join(data)
			res = os.popen(chn).readlines()
			for mot in res :
				tampon = tampon + mot
			taille = len(tampon)/4024
			tampon = str(taille) + tampon
			send(self,tampon,clientsocket)
			send(self,"\n",clientsocket)
			del tampon
		else :
			send(self,"le fichier n'existe pas il n'est pas possible de cat\n",clientsocket)
	elif data[0] == "mv" :
		ls ="ls" + " " + self.path
		lst = os.popen(ls).readlines()
		for i, item in enumerate(lst) :
			lst[i] = item.rstrip()
		if (data[1] in lst) :
			data[1]=self.path+"/"+data[1]
			data[2]=self.path+"/"+data[2]
			chn = " ".join(data)
			os.system(chn)
		else :
			print("fichier inconnu")
	else:
		print "connais pas"

#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
def send(self, message,clientsocket):
	self.clientsocket.send(message.encode("Utf8"))
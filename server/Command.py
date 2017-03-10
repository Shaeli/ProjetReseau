#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, Rights
from socket import error as SocketError
import errno, shutil
from os import chdir
from os import system
import os
from getpass import getpass
import time

BUFFER_SIZE = 2048

def commandes_server(self, clientsocket):
	tampon = ""
	data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
	data=data.split(" ")

	#Partie gestion des droits
	rights = Rights.Rights(self.path)


	if data[0] == "ls":
		chn = " ".join(data)
		chn = chn + " " + self.path
		res = os.popen(chn).readlines()
		for mot in res :
			tampon = tampon + mot
		taille = len(tampon)/BUFFER_SIZE
		tampon = str(taille) + tampon + "\n"
		send(self,tampon,clientsocket)
		del tampon

	elif data[0] == "cd" :
		ls = "ls" + " " + self.path
		lst = os.popen(ls).readlines()
		for i, item in enumerate(lst) :
			lst[i] = item.rstrip()
		if (data[1] in lst) or (data[1] == "..") :
			if data[1] == ".." :
				if self.path != "./data" :
					path = self.path.split("/")
					self.path = ""
					for i in range(0,len(path)-1):
						self.path = self.path+path[i]
						self.path = self.path+"/"
			else :
				self.path = self.path + "/" + data[1]
		else :
			print("pas de changement de path car cd pas bon")
		send(self,self.path,clientsocket)
	elif data[0] == "cat" :
		if rights.isReadable(self.rights):
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
				taille = len(tampon)/BUFFER_SIZE
				tampon = str(taille) + tampon
				send(self,tampon,clientsocket)
				del tampon
			else :
				send(self,"le fichier n'existe pas il n'est pas possible de cat\n",clientsocket)
		else:
			send(self,"0Droits de lectures insuffisants.\n",clientsocket)

	elif data[0] == "mv" :
		if rights.isWritable(self.rights):
			ls ="ls" + " " + self.path
			lst = os.popen(ls).readlines()
			for i, item in enumerate(lst) :
				lst[i] = item.rstrip()
			if (data[1] in lst) :
				data[1] = self.path+"/"+data[1]
				data[2] = self.path+"/"+data[2]
				chn = " ".join(data)
				os.system(chn)
			else :
				print("fichier inconnu")

	elif data[0] == "rm" :
		if rights.isWritable(self.rights):
			if data[1] == "-R":
				try:
					shutil.rmtree(self.path+"/"+data[2])
					send(self,"Suppression effectuée.\n", clientsocket)
				except Exception as e:
					send(self,"Impossible de supprimer le dossier, erreur.\n", clientsocket)
			else:
				try:
					os.remove(self.path+"/"+data[1])
					send(self,"Suppression effectuée.\n", clientsocket)
				except Exception as e:
					send(self,"Impossible de supprimer le fichier, erreur.\n", clientsocket)
		else:
			send(self,"Droits d'écriture insuffisants.\n", clientsocket)

	elif data[0] == "mkdir" :
		if rights.isWritable(self.rights):
			data[1] = self.path+"/"+data[1]
			chn = " ".join(data)
			os.system(chn)
			config = open(data[1] + "/.config", "w")
			config.write("[read]\nall\n[write]\nall\n")

	elif data[0] == "touch" :
		if rights.isWritable(self.rights):
			data[1] = self.path+"/"+data[1]
			chn = " ".join(data)
			os.system(chn)

	elif data[0] == "add" :
		etat=False
		ls ="ls" + " " + self.path
		lst = os.popen(ls).readlines()
		for i, item in enumerate(lst) :
			lst[i] = item.rstrip()
		if (data[1] in lst) :
			data[1] = self.path+"/"+data[1]
			fichier = data[1]
			chn = "cat " + fichier
			res = os.popen(chn).readlines()
			for mot in res :
				tampon = tampon + mot
			taille = len(tampon)/BUFFER_SIZE
			tampon = str(taille) + tampon
			tampon = tampon + "\n"
			send(self,tampon,clientsocket)
			del tampon
			etat=True
		else :
			send(self,"0Le fichier n'existe pas, creez le avant d'ajouter du texte\n",clientsocket)
		if etat == True :
			ajout = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			commande = 'echo "' + ajout + '" ' + ">>" + " " + fichier
			os.system(commande)
	elif data[0] == "vim":
		print "edition"
	else:
		print "commande non reconnue"

#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
def send(self, message,clientsocket):
	self.clientsocket.send(message.encode("Utf8"))
#!/usr/bin/python
# -*-coding:Utf8 -*

from socket import error as SocketError
from os import chdir
from os import system
import os, base64, time, tempfile, errno, shutil, socket, Rights
from getpass import getpass
from xml.sax.saxutils import escape as xml
from Crypto.Cipher import AES
import time
import tempfile
import sys
import threading
import subprocess


BUFFER_SIZE = 4096

if os.name=="nt":
	separateur="\\"
else:
	separateur="/"
	
def commandes_server(self, clientsocket):
	self.path=self.path.replace("/",separateur)
	tampon = ""
	data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
	data=data.split(" ")

	#Partie gestion des droits
	rights = Rights.Rights(self.path)


	if data[0] == "ls": #commande ls
		chn = " ".join(data)
		chn = chn + " " + self.path #on recupere le path
		for mot in os.listdir(self.path) : #on le remet sous la forme chaine de caractere
			if mot[0]!=".":
				tampon = tampon +" "+ mot
		taille = len(tampon)/BUFFER_SIZE
		tampon = str(taille) + tampon + " "+ "\n"
		send(self,tampon,clientsocket) #on envoie le resultat
		del tampon

	elif data[0] == "cd" : #commande cd
		if len(data) != 1 :
			if (data[1] in os.listdir(self.path) )  : #si c'est dans la liste, ou "..", on peut changer le path
				if(os.path.isdir(self.path+separateur+data[1])):
					self.path = self.path+separateur+data[1]
					send(self,self.path,clientsocket)
				else: 
					send(self,"error,cd impossible: C'est un fichier",clientsocket)
			elif data[1] == ".." :
				if (self.path != "./data" and self.path!=".\\data"): #si le path est "./data" et l'on souhaite faire "cd ..", on ne le change pas, ce n'est pas possible
					path = self.path.split(separateur)
					self.path = ""
					for i in range(0,len(path)-1): #mise a jour du nouveau path
						self.path = self.path+path[i]
						self.path = self.path+separateur
					nb=len(self.path)
					self.path=self.path[0:nb-1]
					send(self,self.path,clientsocket)
			else :
				send(self,"error,cd impossible: Le dossier n'existe pas",clientsocket)
		
	elif data[0] == "cat" : #commande cat
		if rights.isReadable(self.rights) and data[1] != ".config": #verification si l'on possede les droits
			if (data[1] in os.listdir(self.path)) :
				data[1] = self.path+separateur+data[1] #on met a jour le chemin
				if os.name=="nt":
					chn="type "+data[1]
				else:
					chn = " ".join(data)
				res = os.popen(chn).readlines() #on recupere la sortie du cat
				for mot in res :
					tampon = tampon + mot
				taille = len(tampon)/BUFFER_SIZE #on regarde le nombre de message qu'il faut pour envoyer entierement le fichier
				tampon = str(taille) + tampon
				send(self,tampon,clientsocket) #on envoie le message
				del tampon
			else :
				send(self,"0le fichier n'existe pas il n'est pas possible de cat\n",clientsocket)
		else:
			send(self,"0Droits de lectures insuffisants.\n",clientsocket)

	elif data[0] == "mv" : #commande mv
		if rights.isWritable(self.rights) and data[1] != ".config":
			if (data[1] in os.listdir(self.path)):
				data[1] = self.path+separateur+data[1]
				data[2] = self.path+separateur+data[2]
				if os.name=="nt":
					chn="move "+data[1]+ " " +data[2]
				else:
					chn = " ".join(data)
				os.system(chn)
			else :
				print("fichier inconnu")

	elif data[0] == "rm" :
		if rights.isWritable(self.rights):
			if data[1] == "-R":
				if data[2] == ".config":
					send(self,"Fichier de configuration vérouillé.\n", clientsocket)
				else :
					try:
						shutil.rmtree(self.path+separateur+data[2])
						send(self,"Suppression effectuée.\n", clientsocket)
					except Exception as e:
						send(self,"Impossible de supprimer le dossier, erreur.\n", clientsocket)
			else:
				if data[1] == ".config":
					send(self,"Fichier de configuration vérouillé.\n", clientsocket)
				else :
					try:
						os.remove(self.path+separateur+data[1])
						send(self,"Suppression effectuée.\n", clientsocket)
					except Exception as e:
						send(self,"Impossible de supprimer le fichier, erreur.\n", clientsocket)
		else:
			send(self,"Droits d'écriture insuffisants.\n", clientsocket)

	elif data[0] == "mkdir" :
		if rights.isWritable(self.rights):
			data[1] = self.path+separateur+data[1]
			chn = " ".join(data)
			os.system(chn)
			config = open(data[1] + separateur+".config", "w")
			config.write("[read]\n")
			line = ""
			for l in rights.read :
				line = line + l + ";"
			line = line[:-1]
			config.write(line + "\n[write]\n")
			line = ""
			for l in rights.write :
				line = line + l + ";"
			line = line[:-1]
			config.write(line + "\n[owners]\n")
			line = ""
			for l in rights.owners :
				line = line + l + ";"
			line = line +self.Thread_name
			config.write(line)

	elif data[0] == "touch" :
		if rights.isWritable(self.rights):
			if os.name=="nt":
				os.system("type nul>"+self.path+separateur+data[1])
			else:
				data[1] = self.path+separateur+data[1]
				chn = " ".join(data)
				os.system(chn)

	elif data[0] == "rights":
		config = open(self.path +separateur+".config", "r")
		config.readline()
		line = "Lecture : " + config.readline().replace(";", ", ") + "Ecriture : "
		config.readline()
		line = line + config.readline().replace(";", ", ") +"\n"
		send(self, line, clientsocket)

	elif data[0] == "admin":
		if rights.isOwner(self.Thread_name):
			#Envoie des données à l'application graphique
			send(self, "yes", clientsocket)			
			config = open(self.path +separateur+".config", "r")
			config.readline()
			line = config.readline().replace(";", ",").replace(" ", "").rstrip()
			send(self, line, clientsocket)
			config.readline()
			line = config.readline().replace(";", ",").replace(" ", "").rstrip()
			send(self, line, clientsocket)
			config.close()
			#Retour des données
			read = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			write = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			if read.rstrip() == "abort" or write.rstrip() == "abort":
				send(self, "no", clientsocket)
			else:
				read = read.rstrip().replace(" ", "").replace(",", ";")
				write = write.rstrip().replace(" ", "").replace(",", ";")
				#Ecriture des informations
				os.remove(self.path + separateur+".config")
				config = open(self.path + separateur+".config", "w")
				config.write("[read]\n")
				print read
				print write
				config.write(read + "\n[write]\n")
				config.write(write + "\n[owners]\n")
				line = ""
				for l in rights.owners :
					line = line + l + ";"
				line = line[:-1]
				config.write(line)
				#Mise à jour des droits
				rights = Rights.Rights(self.path)
				#Réponse du serveur
				send(self, "ok", clientsocket)
		else:
			send(self, "no", clientsocket)


	elif data[0] == "vim":
		IP = "127.0.0.1"
		port = 6300
		droit = False
		file = self.path +"/" + data[1]
		print file
		if rights.isWritable(self.rights):
			send(self,"ok",clientsocket)
			droit=True
		else :
			send(self,"no",clientsocket)

		if droit :
			sock_serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock_serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sock_serv.bind((IP, port))
			sock_serv.listen(10)
			(conn, (ip, port)) = sock_serv.accept()
			subprocess.call(["rvim", file], bufsize=0, stdin=conn, stdout=conn)
			conn.send("FIN");




	elif data[0] == 'upload' : #test si fich existe a faire
		if rights.isWritable(self.rights):
			send(self, "ok",clientsocket)
			nbretour = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			nbretour = int(nbretour)
			fich = self.path + separateur + data[1]
			fp = open(fich, "wb")
			if nbretour > BUFFER_SIZE :
				for i in range((nbretour / BUFFER_SIZE) +1) :
					data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
					fp.write(data)
			else :
				data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
				fp.write(data)
			fp.close()
		else:
			send(self,"no",clientsocket)

	elif data[0] == 'uploadx' :
		path = data[1].rstrip().split('/')
		path = path[0:len(path) - 1]
		path = "/".join(path)
		rights = Rights.Rights(path)
		if rights.isWritable(self.rights):
			send(self, "ok",clientsocket)
			nbretour = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
			nbretour = int(nbretour)
			fich = data[1]
			fp = open(fich, "wb")
			if nbretour > BUFFER_SIZE :
				for i in range((nbretour / BUFFER_SIZE) +1) :
					data = self.clientsocket.recv(BUFFER_SIZE)
					fp.write(data)
			else :
				data = self.clientsocket.recv(BUFFER_SIZE)
				fp.write(data)
			fp.close()
		else:
			send(self,"no",clientsocket)

	elif data[0] == "dlx" :
		path = data[1].rstrip().split('/')
		path = path[0:len(path) - 1]
		path = "/".join(path)
		rights = Rights.Rights(path)
		fich = data[1] 
		droits = True
		exist = False
		if rights.isWritable(self.rights) :
			send(self,"ok",clientsocket)
		elif rights.isReadable(self.rights) and not rights.isWritable(self.rights):
			send(self,"RO",clientsocket)
		else:
			send(self,"no",clientsocket)
			droits = False
		if droits :
			try:
				fp=open(fich,"rb") #ici nous testons l'exitence du fichier
				fp.close()
				exist = True
			except:
				send(self,"Ce fichier n'existe pas!\n",clientsocket)
			if exist :
				cle = self.mdp
				cle += '\0' *(-len(cle)%16)
				codeur = AES.new(cle,AES.MODE_ECB)
				fp = open(fich,'rb')
				nboctets=os.path.getsize(fich)
				send(self,str(nboctets),clientsocket)
				num = 0
				if nboctets > BUFFER_SIZE : #si il y a plus d'octets que la taille du buffer, on envoie en plusieurs fois
					for i in range((nboctets/BUFFER_SIZE)+1) :
						fp.seek(num,0)
						data = fp.read(BUFFER_SIZE)
						data += '\0' *(-len(data)%16)
						datacryptes = codeur.encrypt(data.encode("utf8"))
						self.clientsocket.send(datacryptes)
						num = num + BUFFER_SIZE
				elif nboctets == 0 :
					pass
				else : #si il est possible d'envoyer en une fois
					data = fp.read() 
					data += '\0' *(-len(data)%16)
					datacryptes = codeur.encrypt(data.encode("utf8"))
					self.clientsocket.send(datacryptes)
					#send(self,datacryptes,clientsocket)
				fp.close()

	elif data[0] == "rmx":
		if rights.isWritable(self.rights):
			send(self, "ok", clientsocket)
			try:
				os.remove(data[1])
				send(self,"ok", clientsocket)
			except Exception as e:
				send(self,"no", clientsocket)
		else:
			send(self,"no", clientsocket)

	elif data[0] == "ask":
		if rights.isReadable(self.rights):
			send(self, "ok", clientsocket)
			fp=open(data[1],"rb")
			nboctets = os.path.getsize(data[1])
			send(self,str(nboctets),clientsocket)
			if nboctets > BUFFER_SIZE :
				for i in range((nboctets/BUFFER_SIZE)+1) :
					fp.seek(num,0)
					data = fp.read(BUFFER_SIZE)
					send(self,data,clientsocket)
					num = num + BUFFER_SIZE
			else :
				data = fp.read()
				if data == "":
					send(self, "empty file", clientsocket)
				else:
					send(self,data,clientsocket)
			fp.close()
		else:
			send(self,"no", clientsocket)

	elif data[0] == "touchx":
		if rights.isWritable(self.rights):
			send(self, "ok", clientsocket)
			try:
				chn = "touch " + data[2] + "/" + data[1]
				os.system(chn)
				send(self,"ok", clientsocket)
			except Exception as e:
				send(self,"no", clientsocket)
		else:
			send(self,"no", clientsocket)

	elif data[0] == "startx" : #commande startx
		pass

	elif data[0] == "init_arbo":
		def initialisationXML(path):
		    arborescence = '<dir>\n<name>%s</name>\n' % xml(os.path.basename(path))
		    dirs = []
		    files = []
		    for item in os.listdir(path):
		        itempath = os.path.join(path, item)
		        if os.path.isdir(itempath):
		            dirs.append(item)
		        elif os.path.isfile(itempath):
		            files.append(item)
		    if files:
		        arborescence += '  <files>\n' + '\n'.join('    <file>\n      <name>%s</name>\n    </file>' % xml(f) for f in files) + '\n  </files>\n'
		    if dirs:
		        for d in dirs:
		            x = initialisationXML(os.path.join(path, d))
		            arborescence += '\n'.join('  ' + line for line in x.split('\n'))
		    arborescence += '</dir>'
		    return arborescence
		arbostring =initialisationXML("data")
		str(arbostring)
		send(self, arbostring ,clientsocket)
		
	elif data[0] == "getpass":
		send(self,self.path,clientsocket)

	elif data[0] == "nothing" :
		print("Commande incomplete")

	elif data[0] == "dl" :
		fich = self.path + separateur + data[1] 
		droits = True
		exist = False
		if rights.isWritable(self.rights) :
			send(self,"ok",clientsocket)
		elif rights.isReadable(self.rights) and not rights.isWritable(self.rights):
			send(self,"RO",clientsocket)
		else:
			send(self,"no",clientsocket)
			droits = False
		if droits :
			try:
				fp=open(fich,"rb") #ici nous testons l'exitence du fichier
				fp.close()
				exist = True
			except:
				send(self,"Ce fichier n'existe pas!\n",clientsocket)
			if exist :
				cle = self.id_cli
				cle += '\0' *(-len(cle)%16)
				codeur = AES.new(cle,AES.MODE_ECB)
				fp = open(fich,'rb')
				nboctets=os.path.getsize(fich)
				send(self,str(nboctets),clientsocket)
				num = 0
				if nboctets > BUFFER_SIZE : #si il y a plus d'octets que la taille du buffer, on envoie en plusieurs fois
					for i in range((nboctets/BUFFER_SIZE)+1) :
						fp.seek(num,0)
						data = fp.read(BUFFER_SIZE)
						data += '\0' *(-len(data)%16)
						datacryptes = codeur.encrypt(data)
						self.clientsocket.send(datacryptes)
						num = num + BUFFER_SIZE
				elif nboctets == 0 :
					pass
				else : #si il est possible d'envoyer en une fois
					data = fp.read() 
					data += '\0' *(-len(data)%16)
					datacryptes = codeur.encrypt(data)
					self.clientsocket.send(datacryptes)
					#send(self,datacryptes,clientsocket)
				fp.close()
	else:
		print "commande non reconnue"

#Fonction à utiliser pour envoyer un message en texte (utilise un encodage défini)
def send(self, message,clientsocket):

	self.clientsocket.send(message.encode("Utf8"))
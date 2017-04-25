#!/usr/bin/python
# -*-coding:Utf8 -*

import Tkconstants, tkFileDialog, tkMessageBox
import socket, sys, md5, ssl, time, readline, os, commandclient, base64
import Treeview as TV
import Tkinter as tk
from Crypto.Cipher import AES

BUFFER_SIZE = 2048

def getPass(self, socket):
	send("commandes", socket)
	send("getpass", socket)
	socket.recv(BUFFER_SIZE).decode("Utf8")
	self.path = socket.recv(BUFFER_SIZE).decode("Utf8")

def sendFileToServer(socket, gui):
	#On récupère le nom du fichier à envoyer
	filename = tkFileDialog.askopenfilename(title = "Fichier à envoyer")

	#Si il y a un nom de fichier
	if filename:
		if gui.ptype == "directory":
			send("commandes", socket)
			#On récupère le nom final du fichier
			file = filename.rstrip().split("/")
			file = file[len(file) - 1]
			#On lance la procédure d'upload
			send("uploadx " +  gui.path + "/" + str(file), socket)
			data = socket.recv(BUFFER_SIZE).decode("Utf8")
			data = socket.recv(BUFFER_SIZE).decode("Utf8")
			if data == "ok":
				pourcent = 0
				num = 0
				fich = filename #fichier a upload : il doit se situer dans le dossier client/dataclient
				fp = open(fich,"rb") #on ouvre le fichier
				nboctets = os.path.getsize(fich)
				send(str(nboctets), socket) #on envoie le nombre d'octets presents dans le fichier
				if nboctets > BUFFER_SIZE : #si il y a plus d'octets que la taille du buffer, on envoie en plusieurs fois
					for i in range((nboctets/BUFFER_SIZE)+1) :
						fp.seek(num,0)
						data = fp.read(BUFFER_SIZE)
						socket.send(data)
				else : #si il est possible d'envoyer en une fois
					data = fp.read() 
					if data == "":
						send(" ", socket)
					else:
						socket.send(data)
				fp.close()
			else:
				print "Droit d'écriture insuffisants."
		else:
			tkMessageBox.showinfo("GUI", "L'élement de destination n'est pas un dossier.")

def getFileFromServer(socket, gui):
	send("commandes", socket)
	if gui.ptype_client == "directory":
		send("dlx " + gui.path, socket)
		file = gui.path
		obj = file.rstrip().split("/")
		obj = obj[len(obj) - 1]
		socket.recv(BUFFER_SIZE).decode("Utf8")
		droits = socket.recv(BUFFER_SIZE).decode("Utf8")
		fich = gui.path_client + "/" + obj
		if droits != "no" :
			existe = socket.recv(BUFFER_SIZE).decode("Utf8")
			if existe == "Ce fichier n'existe pas!\n" :
				print existe
			else :
				fp = open(fich,"wb")
				nbretour = int(existe)
				if nbretour > BUFFER_SIZE :
					for i in range((nbretour / BUFFER_SIZE) +1) :
						data=socket.recv(BUFFER_SIZE)
						fp.write(data)
				elif nbretour == 0 :
					pass
				else :
					data=socket.recv(BUFFER_SIZE)
					fp.write(data)
				fp.close()
	else:
		tkMessageBox.showinfo("GUI", "L'élement de destination n'est pas un dossier.")

def delFileOnServer(socket, gui):
	send("commandes", socket)
	if gui.ptype != "directory":
		send("rmx " + gui.path, socket)
		#socket.recv(BUFFER_SIZE).decode("Utf8")
		droits = socket.recv(BUFFER_SIZE).decode("Utf8")
		if droits != "no" :
			socket.recv(BUFFER_SIZE).decode("Utf8")
			recept = socket.recv(BUFFER_SIZE).decode("Utf8")
			if recept == "ok":
				tkMessageBox.showinfo("GUI", "Fichier supprimé.")
			else:
				tkMessageBox.showinfo("GUI", "Erreur lors de la suppression.")
		else:
			tkMessageBox.showinfo("GUI", "Droits d'écriture insuffisants.")
	else:
		tkMessageBox.showinfo("GUI", "L'élément à supprimer est un dossier : erreur.")

def addFileToServer(socket, gui):
	subwindow = tk.Toplevel()
	text = tk.StringVar()
	entry = tk.Entry(subwindow, textvariable = text)
	button = tk.Button(subwindow, text = "Ajouter", command = lambda y = socket, x = gui , z = text: touchServer(y, x, z))
	entry.pack()
	button.pack()

	
def touchServer(socket, gui, text):
	if text.get() != "":
		if gui.ptype == "directory":
				send("commandes", socket)
				time.sleep(0.1)
				send("touchx " + text.get() + " " + gui.path, socket)
				#socket.recv(BUFFER_SIZE).decode("Utf8")
				droits = socket.recv(BUFFER_SIZE).decode("Utf8")
				if droits != "no" :
					recept = socket.recv(BUFFER_SIZE).decode("Utf8")
					if recept == "ok":
						tkMessageBox.showinfo("GUI", "Fichier ajouté.")
					else:
						tkMessageBox.showinfo("GUI", "Erreur lors de l'ajout.")
				else:
					tkMessageBox.showinfo("GUI", "Droits d'écriture insuffisants.")
		else:
			tkMessageBox.showinfo("GUI", "Vous n'êtes pas dans un dossier.")
	else:
		tkMessageBox.showinfo("GUI", "fichier vide")
	socket.recv(BUFFER_SIZE).decode("Utf8")

def send(message,clientsocket):
	clientsocket.send(message.encode("Utf8"))

#Fonction pour flush un message reçu par le client (virer l'autocomplétion)
def flushRecv(sock):
	data = sock.recv(BUFFER_SIZE).decode("Utf8")
	test = data.split(" ")
	if test[0] == ".config":
		return sock.recv(BUFFER_SIZE).decode("Utf8")
	else:
		return data

#Fonction pour mettre à jour le fichier (coté serveur ou client)
def majFile(gui, zoneTexte):
	socket = gui.socket
	if gui.side == "server":
		file = gui.current.rstrip().split("/")
		file = file[len(file) - 1]
		fd = open("./client/dataclient/tmp/" + file, "wb")
		fd.write(zoneTexte.get("1.0",tk.END))
		fd.close()
		send("commandes", socket)
		#On lance la procédure d'upload
		send("uploadx " +  gui.current, socket)
		data = socket.recv(BUFFER_SIZE).decode("Utf8")
		data = socket.recv(BUFFER_SIZE).decode("Utf8")
		if data == "ok":
			pourcent = 0
			num = 0
			#fichier a upload : il doit se situer dans le dossier client/dataclient
			fp = open("./client/dataclient/tmp/" + file,"rb") #on ouvre le fichier
			nboctets = os.path.getsize("./client/dataclient/tmp/" + file)
			send(str(nboctets), socket) #on envoie le nombre d'octets presents dans le fichier
			if nboctets > BUFFER_SIZE : #si il y a plus d'octets que la taille du buffer, on envoie en plusieurs fois
				for i in range((nboctets/BUFFER_SIZE)+1) :
					fp.seek(num,0)
					data = fp.read(BUFFER_SIZE)
					socket.send(data)
			else : #si il est possible d'envoyer en une fois
				data = fp.read() 
				if data == "":
					send(" ", socket)
				else:
					socket.send(data)
			fp.close()
			os.remove("./client/dataclient/tmp/" + file)
		else:
			print "Droit d'écriture insuffisants."
	elif gui.side == "client":
		subwindow = tk.Toplevel()
		text = tk.StringVar()
		label = tk.Label(subwindow, text="Mot de passe :")
		entry = tk.Entry(subwindow, textvariable = text, show = "*")
		button = tk.Button(subwindow, text = "Encoder", command = lambda x = text, y = subwindow, z = zoneTexte, a = gui.current: hashing(x, y, z, a))
		label.pack()
		entry.pack()
		button.pack()

def hashing(text, window, zoneTexte, path):
	textstr = text.get()
	text.set(md5.new(textstr).hexdigest())
	window.destroy()
	cle = text.get()
	cle += '\0' *(-len(cle)%16)
	coder = AES.new(cle, AES.MODE_ECB)
	fd = open(path, 'wb')
	data = zoneTexte.get("1.0",tk.END)
	data += '\0' *(-len(data)%16)
	datacryptes = coder.encrypt(data.encode("utf8"))
	fd.write(datacryptes)
	fd.close()
#!/usr/bin/python
# -*-coding:Utf8 -*
from getpass import getpass
import socket, sys , os
import md5
import subprocess



TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 2048

path = ""

def commandes_client(sock,mess):


	#Liste des commandes implémentées : cd, ls, cat, mv
	if mess[0] == "cd":
		global path
		chn = " ".join(mess)
		send(sock,chn)
		tmp = sock.recv(BUFFER_SIZE).decode("Utf8")
		taille=len(tmp)
		path=tmp[6:taille]

	elif mess[0] == "ls":
		chn = " ".join(mess)
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		message = ""
		nb = data[0]
		taille = len(data) 
		for i in range(taille-1) :
			message = message+data[i+1]
		#sys.stdout.write('<server>')
		sys.stdout.write(message)
		if int(nb) > 0 :
			a = int(nb) 
			for i in range(a):
				data = sock.recv(BUFFER_SIZE).decode("Utf8")
				sys.stdout.write(data)
	elif mess[0] == "cat":
		chn = " ".join(mess)
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		message = ""
		nb = data[0]
		taille = len(data) 
		for i in range(taille-1) :
			message = message+data[i+1]
		sys.stdout.write('<server>')
		sys.stdout.write(message)
		if int(nb) > 0 :
			a=int(nb) 
			for i in range(a):
				data = sock.recv(BUFFER_SIZE).decode("Utf8")
				sys.stdout.write(data)
	elif mess[0] == "mv":
		chn = " ".join(mess)
		send(sock,chn)
	elif mess[0] == "rm":
		chn = " ".join(mess)
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		sys.stdout.write('<server>')
		sys.stdout.write(data)
	elif mess[0] == "mkdir" :
		chn = " ".join(mess)
		send(sock,chn)
	elif mess[0] == "touch" :
		chn = " ".join(mess)
		send(sock,chn)
	elif mess[0] == "add" :
		chn = " ".join(mess) 
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		message = ""
		nb = int(data[0])
		taille = len(data) 
		for i in range(taille-1) :
			message = message+data[i+1]
		sys.stdout.write('<server>')
		sys.stdout.write(message)
		if nb > 0 :
			for i in range(nb):
				data = sock.recv(BUFFER_SIZE).decode("Utf8")
				sys.stdout.write(data)
		if data != "0Le fichier n'existe pas, creez le avant d'ajouter du texte\n" :
			print("\n \n Que voulez vous rajouter a ce fichier ?\n")
			ajout = sys.stdin.readline()
			ajout = ajout.rstrip()
			send(sock,ajout)
	elif mess[0]==envoie:

		host = TCP_IP                    #hard-coded
		port = TCP_PORT
		transport = paramiko.Transport((host, port))

		password = "THEPASSWORD"                #hard-coded
		username = "THEUSERNAME"                #hard-coded
		transport.connect(username = username, password = password)

		sftp = paramiko.SFTPClient.from_transport(transport)

		path = '/home/yabda/ProjetReseau/data' + sys.argv[1]    #hard-coded
		localpath = sys.argv[1]
		sftp.put(localpath, path)

		sftp.close()
		transport.close()
		print 'Upload done.'
	elif mess[0] == "vim" :
		chn = " ".join(mess) 
		send(sock,chn)
		myfile = "/tmp/" + mess[1]
		print myfile 
		os.system("vim "+ myfile)

	
#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))
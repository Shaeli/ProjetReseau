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
	elif mess[0] == "rights":
		chn = " ".join(mess)
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		sys.stdout.write(data)

	elif mess[0]=="envoie":

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
		modif = False
		chn = " ".join(mess) 
		send(sock,chn)
###########################  Partie reception du fichier  ################################ 
		infos = sock.recv(BUFFER_SIZE).decode("Utf8")
		if infos == "Ce fichier n'existe pas!\n" :
			print "Le fichier n'existe pas"
		else :
			infos = int(infos)
			fich = "/home/elounette/tempo/client/dataclient" + "/" + mess[1]
			fp = open(fich, "wb")
			if infos > BUFFER_SIZE :
				for i in range((infos / BUFFER_SIZE) +1) :
					data = sock.recv(BUFFER_SIZE).decode("Utf8")
					fp.write(data)
			else :
				data = sock.recv(BUFFER_SIZE).decode("Utf8")
				fp.write(data)
###########################  Partie edition du fichier  ################################ 				
			os.system("vim " + fich)
			modif=True
###########################  Partie renvoie du fichier  ################################ 
		if modif == True :
			num = 0
			fp=open(fich,"rb")
			nboctets = os.path.getsize(fich)
			send(sock,str(nboctets))
			print nboctets
			if nboctets > BUFFER_SIZE :
				for i in range((nboctets/BUFFER_SIZE)+1) :
					fp.seek(num,0)
					data = fp.read(BUFFER_SIZE)
					print data
					send(sock,data)
					num = num + BUFFER_SIZE
			else :
				data = fp.read()
				send(sock,data)
			fp.close()
	elif mess[0] == "upload" :
		chn = " ".join(mess)
		send(sock,chn)
		pourcent = 0
		num = 0
		fich = "./client/dataclient/" + mess[1]
		fp=open(fich,"rb")
		nboctets = os.path.getsize(fich)
		send(sock,str(nboctets))
		if nboctets > BUFFER_SIZE :
			for i in range((nboctets/BUFFER_SIZE)+1) :
				fp.seek(num,0)
				data = fp.read(BUFFER_SIZE)
				send(sock,data)
				num = num + BUFFER_SIZE
				if pourcent == 0 and num > nboctets / 100 * 10 and num < nboctets / 100 * 20:
					print " >> 10%",
					pourcent = 1
				elif pourcent == 1 and num > nboctets / 100 * 20 and num < nboctets / 100 * 30:
					print " >> 20%",
					pourcent = 2
				elif pourcent < 3 and num > nboctets / 100 * 30 and num < nboctets / 100 * 40:
					print " >> 30%",
					pourcent = 3
 				elif pourcent < 4 and num > nboctets / 100 * 40 and num < nboctets / 100 * 50:
					print " >> 40%",
					pourcent = 4
				elif pourcent < 5 and num > nboctets / 100 * 50 and num < nboctets / 100 * 60:
					print " >> 50%",
					pourcent = 5
				elif pourcent < 6 and num > nboctets / 100 * 60 and num < nboctets / 100 * 70:
					print " >> 60%",
					pourcent = 6
				elif pourcent < 7 and num > nboctets / 100 * 70 and num < nboctets / 100 * 80:
					print " >> 70%",
					pourcent = 7
				elif pourcent < 8 and num > nboctets / 100 * 80 and num < nboctets / 100 * 90:
					print " >> 80%",
					pourcent = 8
				elif pourcent < 9 and num > nboctets / 100 * 90 and num < nboctets / 100 * 100:
					print " >> 90%"                    
					pourcent = 9

		else :
			data = fp.read()
			send(sock,data)
		fp.close()
	else :
		print("Commande non reconnue")

#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))
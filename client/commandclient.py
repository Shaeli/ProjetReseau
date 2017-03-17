#!/usr/bin/python
# -*-coding:Utf8 -*
from getpass import getpass
import socket, sys , os
import md5
import subprocess
import time



TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 2048

path = ""

def commandes_client(sock,mess):


	#Liste des commandes implémentées : cd, ls, cat, mv , rm, mkdir, touch, add, vim, upload
	if mess[0] == "cd": #commande cd
			global path
			chn = " ".join(mess)
			send(sock,chn) #envoie du changement de chemin
			tmp = sock.recv(BUFFER_SIZE).decode("Utf8")
			taille=len(tmp)
			path=tmp[6:taille] #mise a jour du nouveau chemin coté client

	elif mess[0] == "ls": #commande ls
		chn = " ".join(mess)
		send(sock,chn) #envoie de la commande
		data = sock.recv(BUFFER_SIZE).decode("Utf8") #recuperation de la reponse
		message = ""
		nb = data[0] #récuperation du chiffre indiquant combien de message vont arriver
		taille = len(data) 
		for i in range(taille-1) : #affichage du premier message sans le premier octet (le chiffre indiquant le nombre de message)
			message = message+data[i+1]
		sys.stdout.write(message) #on imprime a l'ecran le resultat
		if int(nb) > 0 : #si il y a plusieurs messages, on recommence avec les autres
			a = int(nb) 
			for i in range(a):
				data = sock.recv(BUFFER_SIZE).decode("Utf8")
				sys.stdout.write(data)
	elif mess[0] == "cat": #commande cat
		chn = " ".join(mess)
		send(sock,chn) #envoie du message
		data = sock.recv(BUFFER_SIZE).decode("Utf8") #reception des donnees
		message = ""
		nb = data[0] #recuperation du nombre de message arrivant
		taille = len(data) 
		for i in range(taille-1) : #affichage du premier message sans le premier caractere
			message = message+data[i+1]
		sys.stdout.write(message)
		if int(nb) > 0 : #si il y a plusieurs messages, recuperation et affichage des autre messages
			a=int(nb) 
			for i in range(a):
				data = sock.recv(BUFFER_SIZE).decode("Utf8")
				sys.stdout.write(data)
	elif mess[0] == "mv": #commande mv
		chn = " ".join(mess) 
		send(sock,chn)
	elif mess[0] == "rm": #commande rm
		chn = " ".join(mess)
		send(sock,chn) #envoie du fichier a supprimer
		data = sock.recv(BUFFER_SIZE).decode("Utf8") 
		sys.stdout.write(data)
	elif mess[0] == "mkdir" : #commande mkdir
		chn = " ".join(mess)
		send(sock,chn)
	elif mess[0] == "touch" : #commande touch
		chn = " ".join(mess)
		send(sock,chn)
	elif mess[0] == "rights": #commande rights
		chn = " ".join(mess)
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		sys.stdout.write(data)
	elif mess[0] == "admin": #commande admin
		#Demande d'administration des drots au serveur
		chn = " ".join(mess)
		send(sock,chn)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		#Si les droits sont insuffisants
		if data == "no":
			print "Droits insuffisants"
		#Sinon on lance l'édition
		else:
			#On récupère les droits
			read = sock.recv(BUFFER_SIZE).decode("Utf8")
			write = sock.recv(BUFFER_SIZE).decode("Utf8")
			#On lance le programme d'édition
			os.system("python2.7 client/RightsAdministrator.py " + read + " " + write + " " + str(os.getpid()))
			#On lit des information de retour
			fd = open("client/tmp", 'r')
			line = fd.readline()
			send(sock, line)
			line = fd.readline()
			send(sock, line)
			fd.close()
			os.remove("client/tmp")
			#Accusé de reception
			data = sock.recv(BUFFER_SIZE).decode("Utf8")
			if data == "ok":
				print "Les droits ont bien été modifiés."
			else:
				print "Problème dans l'édition des droits."
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
			fich = "client/dataclient" + "/" + mess[1]
			fp = open(fich, "wb")
			if infos > BUFFER_SIZE :
				for i in range((infos / BUFFER_SIZE) +1) :
					data = sock.recv(BUFFER_SIZE).decode("Utf8")
					fp.write(data)
			else :
				data = sock.recv(BUFFER_SIZE).decode("Utf8")
				fp.write(data)
			fp.close()
###########################  Partie edition du fichier  ################################ 				
			time.sleep(1)
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
		fich = "./client/dataclient/" + mess[1] #fichier a upload : il doit se situer dans le dossier client/dataclient
		fp=open(fich,"rb") #on ouvre le fichier
		nboctets = os.path.getsize(fich)
		send(sock,str(nboctets)) #on envoie le nombre d'octets presents dans le fichier
		if nboctets > BUFFER_SIZE : #si il y a plus d'octets que la taille du buffer, on envoie en plusieurs fois
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
		else : #si il est possible d'envoyer en une fois
			data = fp.read() 
			send(sock,data)
		fp.close()
	elif mess[0] == "download" :
		print "coucou"
	else :
		print("Commande non reconnue")

#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))

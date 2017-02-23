#!/usr/bin/python
# -*-coding:Utf8 -*
from getpass import getpass
import socket, sys
import md5

TCP_IP = "127.0.0.1"
TCP_PORT = 8888
BUFFER_SIZE = 2048

def commandes_client(sock):
	sock.send("commandes")
	mess=raw_input("Tapez la commande que vous voulez effectuer.\nSont actuellement supportés les commandes ls et cd\n")
	mess=mess.rstrip()
	if mess[0] == "cd":
		print 'ouii'
		send(sock,mess)
	elif mess == "ls":
		send(sock,mess)
		data = sock.recv(BUFFER_SIZE).decode("Utf8")
		sys.stdout.write('<server>')
		sys.stdout.write(data)
	else:
		print("Cette commande n'est pas supporte pour le moment! Revenez plus tard.")


def utilisateur(sock):
	send(sock,"ajout utilisateur")
	print("ajout d'un utilisateur : \n")
	id_new=raw_input("nom d'utilisateur : ")
	mdp_new2="a"
	mdp_new1="b"
	while mdp_new1!=mdp_new2:
		mdp_new1=getpass("mot de passe utilisateur :")
		mdp_new2=getpass("retaper le mot de passe")
		if mdp_new1!=mdp_new2:
			print "Les mots de passe ne correspondent pas, veuillez le rentrer a nouveau"
	send(sock,id_new+";"+md5.new(mdp_new2).hexdigest())
	print "personnel ajoute a la base de donnee"
	
#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))
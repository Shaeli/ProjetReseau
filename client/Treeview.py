#!/usr/bin/python
# -*-coding:Utf8 -*

BUFFER_SIZE = 2048

#Méthode pour initialiser l'arborescence
def initialisation_arbre_racine(arbre, socket):
	send(socket, "commandes")
	send(socket, "init_arbo")
	data = socket.recv(BUFFER_SIZE)
	data = data.split()
	node = arbre.insert('','end', text=data[0], values=[data[0],"directory"])

	

#def update_arbre(arbre, node, socket):



#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))
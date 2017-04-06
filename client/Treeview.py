#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, os, time
import xml.etree.ElementTree as ET

BUFFER_SIZE = 4096

def parcours_XML(treeview, root, treeview_root, treeview_node):
	for child in root:
		if (child.tag == "name" and child.text == "data"):
			continue
		elif (root.text == "data") and child.tag != "files" and child.tag != "dir":
			treeview_node = treeview.insert(treeview_root, 'end', text = child.text, values = [child.text, "directory"])
		elif child.tag != "files" and child.tag != "dir":
			treeview_node = treeview.insert(treeview_node,'end', text = child.text, values = [child.text, "directory"])
		if (child.tag == "files"):
			for f in child:
				liste = f.findall("name")
				for l in liste:
					if l.text != ".config":
						if (root.text == "data"):
							treeview.insert(treeview_root,'end', text = l.text, values = [l.text,"file"])
						else:
							treeview.insert(treeview_node, 'end' , text = l.text, values = [l.text, "file"])
		elif child.tag == "dir":
			parcours_XML(treeview,child,treeview_root, treeview_node)			

#Méthode pour initialiser l'arborescence
def initialisation_arbre_racine(arbre, socket):
	send(socket, "commandes")
	send(socket, "init_arbo")
	socket.recv(BUFFER_SIZE)
	data = socket.recv(BUFFER_SIZE)
	fd = open("client/dataclient/tree.xml", "w")
	fd.write(data)
	fd.close()
	tree = ET.parse('client/dataclient/tree.xml')
	os.remove('client/dataclient/tree.xml')
	root = tree.getroot()
	treeview_root = arbre.insert('','end', text="data", values = ["data", "directory"])
	parcours_XML(arbre,root,treeview_root,"")

#Méthode de mise à jour de l'arborescence	
#def update_arbre(arbre, node, socket):


#Méthode pour mettre à jour le path lorsque l'on clique sur un item de l'arbre
def eventOnCLick(event, arbre, self):
	item = arbre.selection()[0]
	path = ""
	parent = arbre.parent(item)
	while arbre.item(parent, "text") != "":
		path = arbre.item(parent, "text") + "/" + path
		parent = arbre.parent(parent)
	path = "./data/" + path + arbre.item(item, "text")
	self.path = path
	self.ptype = arbre.item(item,"values")[1]
	return self.path + "::" + self.ptype 



#Fonction pour envoyer un message string sur une socket
def send(sock, message):
	sock.send(message.encode("Utf8"))


##################################################
#################PARTIE CLIENT####################
##################################################

#Méthode de récupération de l'arborescence client
def init_arbo_client(tree):
	node = tree.insert('', 'end', text="dataclient", values=["client/dataclient", "directory"])
	for i in os.listdir("client/dataclient"):
		ptype = None
		if os.path.isdir(i):
			ptype = "directory"
		elif os.path.isfile(i):
			ptype = "file"
		tree.insert(node, "end", text=i, values=[i, ptype])



def eventOnClickClient(event, arbre, self):
	item = arbre.selection()[0]
	path = ""
	parent = arbre.parent(item)
	while arbre.item(parent, "text") != "":
		path = arbre.item(parent, "text") + "/" + path
		parent = arbre.parent(parent)
	path = "./client/" + path + arbre.item(item, "text")
	print path
	self.path_client = path
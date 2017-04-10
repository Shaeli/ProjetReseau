#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, os, time, md5, base64
import xml.etree.ElementTree as ET
from Tkinter import *
from Crypto.Cipher import AES

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



def eventOnClickClient(event, arbre, self, zoneTexte):
	item = arbre.selection()[0]
	path = ""
	parent = arbre.parent(item)
	while arbre.item(parent, "text") != "":
		path = arbre.item(parent, "text") + "/" + path
		parent = arbre.parent(parent)
	path = "./client/" + path + arbre.item(item, "text")
	#Affichage du fichier dans la zone de texte
	if os.path.isdir(path) == False:
		getHashMdp(zoneTexte, path)
	self.path_client = path

def getHashMdp(zoneTexte, path):
	subwindow = Toplevel()
	text = StringVar()
	label = Label(subwindow, text="Mot de passe :")
	entry = Entry(subwindow, textvariable = text, show = "*")
	button = Button(subwindow, text = "Decoder", command = lambda x = text, y = subwindow, z = zoneTexte, a = path: hashing(x, y, z, a))
	label.pack()
	entry.pack()
	button.pack()

def hashing(text, window, zoneTexte, path):
	textstr = text.get()
	text.set(md5.new(textstr).hexdigest())
	window.destroy()
	cle = text.get()
	cle += '\0' *(-len(cle)%16)
	decoder = AES.new(cle, AES.MODE_ECB)
	zoneTexte.delete(1.0, END)
	fd = open(path, 'rb')
	content = fd.read()
	zoneTexte.insert(END, decoder.decrypt(content))
	fd.close()
#!/usr/bin/python
# -*-coding:Utf8 -*

import socket
import sys, os
from Tkinter import *
import tkMessageBox

os.chdir(".")

#fonction pour créer un fichier temporaire pour les droits afin de les envoyer par la suite
def modifRights(read, write, pid):
	if read.get() == "" or write.get() == "":
		tkMessageBox.showerror("Rights Administrator", "Champ vide !")
	else:
		#Ajout de l'utilisateur dans le fichier
		fd = open("client/tmp", 'w')
		fd.write(read.get())
		fd.write("\n")
		fd.write(write.get())
		fd.close()
		tkMessageBox.showinfo("Rights Administrator", "Droits modifiés...\nVous pouvez fermer la fenêtre.")

#Récupération des données passées en paramètre
if len(sys.argv) == 4:
	readArg = sys.argv[1]
	writeArg = sys.argv[2]
	parentPid = sys.argv[3]

	#Main
	fenetre = Tk() #Fenetre principale
	fenetre.title("Rights Administrator")

	#Variables
	read = StringVar()
	read.set(str(readArg))
	write = StringVar()
	write.set(str(writeArg)) 

	#Les éléments de la fenêtre
	label1 = Label(fenetre, text = "Droits de lecture")
	label2 = Label(fenetre, text = "Droits d'écriture")
	bouton = Button(fenetre, text = "Modifier les droits")
	entreeRead = Entry(fenetre, textvariable = read, width = 30)
	entreeWrite = Entry(fenetre, textvariable = write, width = 30)
	bouton.config(command = lambda x = read, y = write, z = parentPid:modifRights(x, y, z))

	#Construction de la fenetre
	label1.pack()
	entreeRead.pack()
	label2.pack()
	entreeWrite.pack()
	bouton.pack()

	fenetre.mainloop()

else:
	print "Erreur, pas assez de paramètres"
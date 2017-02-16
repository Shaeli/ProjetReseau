#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from Tkinter import *
import tkMessageBox
import hashlib 
from os import chdir
chdir(".")

#Fonction qui hache le mot de passe, et ajoute l'utilisateur en fin de fichier users.bdd
def generationPasswd(name, passwd):
	if name.get() == "" or passwd.get() == "":
		tkMessageBox.showerror("Member Generator", "Champ manquant !")
	elif len(passwd.get()) <= 8:
		tkMessageBox.showerror("Member Generator", "Mot de passe trop court !")
	else:
		#cryptage du mot de passe
		mdp = passwd.get()
		mdp = str(mdp)
		mdp = mdp.encode("Utf-8")
		hash = hashlib.sha256(mdp)
		crypted = hash.hexdigest() #Voilà la chaine cryptée en sha256

		#Ajout de l'utilisateur dans le fichier
		fd = open("users.bdd", 'a')
		fd.write(name.get())
		fd.write(";")
		fd.write(crypted)
		fd.write("\n")
		fd.close()
		tkMessageBox.showinfo("Member Generator", "Le nouvel utilisateur a été généré...\nNoubliez pas le mot de passe !")

fenetre = Tk() #Fenetre principale
fenetre.title("Member Generator")

#Déclaration des variables
name = StringVar()
passwd = StringVar() 

name.set("Nom utilisateur")
passwd.set("Password")
entreeName = Entry(fenetre, textvariable = name, width = 30)
entreePass = Entry(fenetre, textvariable = passwd, show = "*", width = 30)

bouton = Button(fenetre, text = "Ajouter à la liste")
bouton.config(command = lambda x = name, y = passwd:generationPasswd(x, y))

#Construction de la fenetre
entreeName.pack()
entreePass.pack()
bouton.pack()

fenetre.mainloop()
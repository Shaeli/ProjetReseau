#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from Tkinter import *
import Tix
import tkMessageBox
import md5
from os import chdir
chdir(".")

#Fonction qui hache le mot de passe, et ajoute l'utilisateur en fin de fichier users.bdd
def generationPasswd(name, passwd, job):
	if name.get() == "" or passwd.get() == "" or job.get() == "":
		tkMessageBox.showerror("Member Generator", "Champ manquant !")
	elif len(passwd.get()) < 8:
		tkMessageBox.showerror("Member Generator", "Mot de passe trop court !")
	else:
		#cryptage du mot de passe en md5
		mdp = passwd.get()
		mdp = str(mdp)
		mdp = mdp.encode("Utf-8")
		hash = md5.new(mdp)
		crypted = hash.hexdigest()

		#Ajout de l'utilisateur dans le fichier
		fd = open("ressources/users.bdd", 'a')
		fd.write("\n")
		fd.write(name.get())
		fd.write(";")
		fd.write(crypted)
		fd.write(";")
		fd.write(str(job.get()))
		fd.close()
		tkMessageBox.showinfo("Member Generator", "Le nouvel utilisateur a été généré...\nNoubliez pas le mot de passe !")



#Main
fenetre = Tix.Tk() #Fenetre principale
fenetre.title("Member Generator")

#Déclaration des variables
name = StringVar()
passwd = StringVar() 
job = StringVar()
name.set("Nom utilisateur")
passwd.set("Password")

#Les élements de la fenètre
entreeName = Entry(fenetre, textvariable = name, width = 30)
entreePass = Entry(fenetre, textvariable = passwd, show = "*", width = 30)
listWork = Tix.ComboBox(fenetre, variable = job)
listWork.insert(0, 'admin')
listWork.insert(1, 'medecin')
listWork.insert(2, 'infirmiere')

bouton = Button(fenetre, text = "Ajouter à la liste")
bouton.config(command = lambda x = name, y = passwd, z = job:generationPasswd(x, y, z))

#Construction de la fenetre
entreeName.pack()
entreePass.pack()
listWork.pack()
bouton.pack()

fenetre.mainloop()

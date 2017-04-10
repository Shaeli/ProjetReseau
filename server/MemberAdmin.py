#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from Tkinter import *
import Tix
import tkMessageBox
import md5
import os
from os import chdir
chdir(".")

jobs = []
names = []
passwords = []
entreesNames = []
listJobs = []

def MAJListe():
	os.remove("ressources/users.bdd")
	fd = open("ressources/users.bdd", 'w')
	fd.write(str(names[0].get()))
	fd.write(";")
	fd.write(passwords[0])
	fd.write(";")
	fd.write(str(jobs[0].get()))
	for x in xrange(1,len(entreesNames)):
		if names[x].get() != "":
			fd.write("\n")
			fd.write(str(names[x].get()))
			fd.write(";")
			fd.write(passwords[x])
			fd.write(";")
			fd.write(str(jobs[x].get()))
	fd.close()
	tkMessageBox.showinfo("Member Administrator", "Listes des utilisateurs mise à jour")

#Main
fenetre = Tix.Tk() #Fenetre principale
fenetre.title("Member Administrator")

#Construction de la fenetre
fd = open("ressources/users.bdd", 'r')
i = 0
lignes  = fd.readlines()
for line in lignes:
	line = line.rstrip().split(";")
	name = StringVar()
	name.set(line[0])
	job = StringVar()
	job.set(line[2])
	password = line[1]
	entreeName = Entry(fenetre, textvariable = name, width = 30)
	entreeName.grid(row = i, column = 0)
	listWork = Tix.ComboBox(fenetre, variable = job)
	listWork.grid(row = i, column = 1)
	listWork.insert(0, 'admin')
	listWork.insert(1, 'medecin')
	listWork.insert(2, 'infirmiere')
	names.append(name)
	jobs.append(job)
	passwords.append(password)
	entreesNames.append(entreeName)
	listJobs.append(listWork)
	line = fd.read()
	i = i + 1
fd.close()

bouton = Button(fenetre, text = "Mettre à jour la liste", command = MAJListe)
bouton.grid(row = i)


fenetre.mainloop()
#!/usr/bin/python
# -*-coding:Utf8 -*

from Tkinter import *

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("PREZO")

#Création de l'arborescence de fichiers
arbo = Frame(fenetre, borderwidth=2, bg = "grey", relief=GROOVE, height = 350, width = 100) 
arbo.pack(side=LEFT, padx=5, pady=5)

# Création de l'affichage du path
path_name = Frame(fenetre, bg = "ivory", borderwidth=2, relief=GROOVE, height = 40, width = 510)
path_name.pack(side = TOP, padx=5, pady=5)

#Création de la fenêtre d'affichage
affichage = Frame(fenetre, borderwidth=2, relief=GROOVE, height = 300, width = 400)
affichage.pack(side=LEFT, padx=5, pady=5)

#Création du menu
menubar = Frame(fenetre, bg="white", borderwidth=2, relief=GROOVE, height = 300, width = 100)
menubar.pack_propagate(False)
menubar.pack(side=RIGHT, padx=5, pady=5)

ADD = Button(menubar, text = "Ajouter", width = 80)
ADD.pack(pady=5)

SUPPR = Button(menubar, text = "Supprimer", width = 80)
SUPPR.pack(pady=5)

DOWNLOAD = Button(menubar, text = "Download", width = 80)
DOWNLOAD.pack(pady=5)

UPLOAD = Button(menubar, text = "Upload", width = 80)
UPLOAD.pack(pady=5)

QUIT = Button(menubar, text = "Quitter", command = fenetre.quit, width = 80)
QUIT.pack(side = BOTTOM, pady=5)


fenetre.mainloop()




#!/usr/bin/python
# -*-coding:Utf8 -*

from Tkinter import *
import ttk
import Treeview as tv 
import CommandsGUI

class Window:

	def __init__(self, socket):

		self.socket = socket
		self.path = ""
		CommandsGUI.getPass(self, socket)

		# Création de la fenêtre principale
		fenetre = Tk()
		fenetre.title("PREZO")

		self.fenetre = fenetre

		#Création de l'arborescence de fichiers
		arbo = Frame(fenetre, borderwidth=2, bg = "grey", relief=GROOVE, height = 350, width = 100)
		arbo.pack_propagate(False)
		arbo.pack(side=LEFT, padx=5, pady=5)

		tree_arb = ttk.Treeview(arbo)
		tree_arb.grid(column=0, row=0, sticky='nswe')
		tree_arb.heading("#0", text="Arborescence", anchor='w')
		#tv.initialisation_arbre_racine(tree_arb, sock)
		tv.initialisation_arbre_racine(tree_arb, socket)

		# Création de l'affichage du path
		path_name_frame = Frame(fenetre, bg = "ivory", borderwidth=2, relief=GROOVE, height = 40, width = 510)
		path_name_frame.pack_propagate(False)
		path_name_frame.pack(side = TOP, padx=5, pady=5)
		path_name = Label(path_name_frame, text=self.path, bg = "ivory").pack(side = LEFT, pady = 5, padx = 5)

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

		UPLOAD = Button(menubar, text = "Upload", width = 80, command = lambda y = socket, x = self : CommandsGUI.sendFileToServer(y, x))
		UPLOAD.pack(pady=5)

		QUIT = Button(menubar, text = "Quitter", command = self.fenetre.quit, width = 80)
		QUIT.pack(side = BOTTOM, pady=5)

	def launchWindow(self):
		self.fenetre.mainloop()

	def closeWindow(self):
		self.fenetre.destroy()
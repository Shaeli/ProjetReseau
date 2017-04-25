#!/usr/bin/python
# -*-coding:Utf8 -*

from Tkinter import *
import ttk
import Treeview as tv 
import RefresherHandler as RH
from threading import Thread
import CommandsGUI

class Window:

	def __init__(self, socket, socket_refresher):

		self.socket = socket
		self.socket_refresher = socket_refresher
		self.path = ""
		self.ptype = "directory"
		self.path_client = ""
		self.ptype_client = "directory"
		self.side = ""
		self.curret = ""

		CommandsGUI.getPass(self, socket)
		# Création de la fenêtre principale
		fenetre = Tk()
		fenetre.title("PREZO")
		fenetre.geometry("1000x370")
		fenetre.resizable(width=True,height=True)
		fenetre.update_idletasks()
		r=[i for i in range(0,len(fenetre.geometry())) if not fenetre.geometry()[i].isdigit()]
		l,h,x,y = [int(fenetre.geometry()[0:r[0]]),int(fenetre.geometry()[r[0]+1:r[1]]),int(fenetre.geometry()[r[1]+1:r[2]]),int(fenetre.geometry()[r[2]+1:])]
		fenetre.geometry("%dx%d%+d%+d" % (l,h,(fenetre.winfo_screenwidth()-l)//2,(fenetre.winfo_screenheight()-h)//2))

		self.show_path = StringVar()
		self.show_path.set(self.path + "::" + self.ptype)
		self.fenetre = fenetre

		#Création de l'arborescence de fichiers
		arbo = Frame(fenetre, borderwidth=2, bg = "grey", relief=GROOVE, height = 350, width = 100)
		arbo.pack_propagate(False)
		arbo.pack(side=LEFT, padx=5, pady=5)

		#Création de la fenêtre d'affichage
		affichage = Frame(fenetre, borderwidth=2, relief=GROOVE, height = 250, width = 400)
		affichage.pack(side=LEFT, padx=5, pady=5)
		zoneTexte = Text(affichage)
		boutonSend = Button(affichage, text = "Mettre à jour", command = lambda x = self, y = zoneTexte : CommandsGUI.majFile(x, y))

		tree_arb = ttk.Treeview(arbo)
		tree_arb.grid(column=0, row=0, sticky='nswe')
		tree_arb.heading("#0", text="Arborescence", anchor='w')
		tv.initialisation_arbre_racine(tree_arb, socket)
		tree_arb.bind("<Double-1>", lambda event, x = self, arbre = tree_arb, z = zoneTexte : self.show_path.set(tv.eventOnCLick(event, arbre, x, z)))
		self.newthread = RH.RefresherHandler(socket_refresher, tree_arb)
		self.newthread.start()


		#Création de l'arborescence client
		arbo_client = Frame(fenetre, borderwidth = 2, bg = "grey", relief = GROOVE, height = 350, width = 100)
		arbo_client.pack_propagate(False)
		arbo_client.pack(side = LEFT, padx = 5, pady = 5)

		tree_arb_client = ttk.Treeview(arbo_client)
		tree_arb_client.grid(column=0, row=0, sticky='nswe')
		tree_arb_client.heading("#0", text = "Arborescence client", anchor = 'w')
		tv.init_arbo_client(tree_arb_client)
		tree_arb_client.bind("<Double-1>", lambda event, x = self, arbre = tree_arb_client, z = zoneTexte : tv.eventOnClickClient(event, arbre, x, z))


		# Création de l'affichage du path
		path_name_frame = Frame(fenetre, bg = "ivory", borderwidth=2, relief=GROOVE, height = 40, width = 510)
		path_name_frame.pack_propagate(False)
		path_name_frame.pack(side = TOP, padx=5, pady=5)
		path_name = Label(path_name_frame, textvariable = self.show_path, bg = "ivory").pack(side = LEFT, pady = 5, padx = 5)

		#Package de la zone de texte
		zoneTexte.pack()
		boutonSend.pack()

		#Création du menu
		menubar = Frame(fenetre, bg="white", borderwidth=2, relief=GROOVE, height = 250, width = 100)
		menubar.pack_propagate(False)
		menubar.pack(side=RIGHT, padx=5, pady=5)

		ADD = Button(menubar, text = "Ajouter", width = 80, command = lambda y = socket, x = self : CommandsGUI.addFileToServer(y, x))
		ADD.pack(pady=5)

		SUPPR = Button(menubar, text = "Supprimer", width = 80, command = lambda y = socket, x = self : CommandsGUI.delFileOnServer(y, x))
		SUPPR.pack(pady=5)

		DOWNLOAD = Button(menubar, text = "Download", width = 80, command = lambda y = socket, x = self : CommandsGUI.getFileFromServer(y, x))
		DOWNLOAD.pack(pady=5)

		UPLOAD = Button(menubar, text = "Upload", width = 80, command = lambda y = socket, x = self : CommandsGUI.sendFileToServer(y, x))
		UPLOAD.pack(pady=5)

		QUIT = Button(menubar, text = "Quitter", command = self.fenetre.quit, width = 80)
		QUIT.pack(side = BOTTOM, pady=5)

	def launchWindow(self):
		self.fenetre.mainloop()

	def closeWindow(self):
		self.fenetre.destroy()
		self.newthread.destroy()
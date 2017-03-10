#!/usr/bin/python
# -*-coding:Utf8 -*

class Rights():
	def __init__(self, path):
		#Mise en place des listes de droits L/E selon le chemin passé en paramètre
		self.path = path
		config = open(self.path + "/.config", "r")
		config.readline()
		self.read = config.readline().rstrip().split(";")
		config.readline()
		self.write = config.readline().rstrip().split(";")

	def isReadable(self, typeClient):
		#Si le client est admin, il peut toujours lire
		if typeClient == "admin":
			return True

		#Si le droits utilisateur est dans la liste des droits du dossier OK
		for rgts in self.read:
			if typeClient == rgts or rgts == "all":
				return True

		#Sinon non
		return False

	def isWritable(self, typeClient):
		#Si le client est admin, il peut toujours écrire
		if typeClient == "admin":
			return True

		#Si le droits utilisateur est dans la liste des droits du dossier OK
		for rgts in self.write:
			if typeClient == rgts or rgts == "all":
				return True

		#Sinon non
		return False
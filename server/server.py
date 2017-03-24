#!/usr/bin/python
# -*-coding:Utf8 -*

import ClientThread
import socket, errno, sys, ssl
from threading import Thread
from socket import error as SocketError


#Encodage en Utf8
reload(sys)  
sys.setdefaultencoding('utf8')

#Socket du serveur
TCP_IP = "127.0.0.1"
TCP_PORT = 8099
nb_cli=0
threads = []
tmp=[]

# Context pour la connexion via certificats
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile = "server/sslcertif/server.crt", keyfile = "server/sslcertif/server.key")

#Création et bind de la socket server
nosslserv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#Création de la socket
nosslserv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
nosslserv.bind((TCP_IP, TCP_PORT))
nosslserv.listen(10)

#Boucle infinie d'écoute et de création de thread client
while True:
	(conn, (ip, port)) = nosslserv.accept()
	sslconn = context.wrap_socket(conn,server_side = True)
	newthread = ClientThread.ClientThread(ip, port, sslconn)
	newthread.start()
	threads.append(newthread)
	nb_cli=0
	for a in threads:
		if str(a).find("started")!=-1:
			nb_cli+=1
	print "il y a actuellement "+str(nb_cli)+" client(s) connectes"

#En cas de fin de connection
print("Fin de la connexion")
conn.close()
nosslserv.close()	
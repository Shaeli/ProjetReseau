#!/usr/bin/python
# -*-coding:Utf8 -*

import ClientThread
import socket
from threading import Thread
from socket import error as SocketError
import errno
import sys

#Encodage en Utf8
reload(sys)  
sys.setdefaultencoding('utf8')

#Socket du serveur
TCP_IP = "127.0.0.1"
TCP_PORT = 8888

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#Création de la socket
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv.bind((TCP_IP, TCP_PORT)) #Binding de la socket
threads = []

#Boucle infinie d'écoute et de création de thread client
while 1:
	serv.listen(10)
	(conn, (ip, port)) = serv.accept()
	newthread = ClientThread.ClientThread(ip, port, conn)
	newthread.start()
	threads.append(newthread)

#En cas de fin de connection
print("Fin de la connexion")
conn.close()
serv.close()
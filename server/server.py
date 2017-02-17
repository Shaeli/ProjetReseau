#!/usr/bin/python
# -*-coding:Utf8 -*

import ClientThread
import socket
from threading import Thread
from socket import error as SocketError
import errno


TCP_IP = "127.0.0.1"
TCP_PORT = 8888

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#Création de la socket
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv.bind((TCP_IP, TCP_PORT)) #Binding de la socket
threads = []
user_list={"root":"azerty"}
while 1:
	print "actuelement "+str(len(threads))+" clients connectes"
	serv.listen(10)
	(conn, (ip, port)) = serv.accept()
	newthread = ClientThread.ClientThread(ip, port, conn,user_list)
	newthread.start()
	threads.append(newthread)

print("Fin de la connection")
conn.close()
serv.close()
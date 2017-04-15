#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, sys
from threading import Thread
import ThreadRefresher as TR

#Encodage en Utf8
reload(sys)  
sys.setdefaultencoding('utf8')

TCP_IP = "127.0.0.1"
TCP_PORT = 8102
threads = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(10)


while True:
	(conn, (ip, port)) = sock.accept()
	newthread = TR.ThreadRefresher(ip, port, conn)
	newthread.start()
	threads.append(newthread)

conn.close()
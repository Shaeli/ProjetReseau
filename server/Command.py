#!/usr/bin/python
# -*-coding:Utf8 -*

import socket
from socket import error as SocketError
import errno
from os import chdir
from os import system
BUFFER_SIZE = 1024

def commandes_server():
	data = self.clientsocket.recv(BUFFER_SIZE).decode("Utf8")
	if data == "ls":
		res = os.popen(ls).readlines()
		self.send(res)
	if data[0] == "cd" :
		os.system(data)

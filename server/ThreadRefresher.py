#!/usr/bin/python
# -*-coding:Utf8 -*

import socket, os, time
from threading import Thread
from socket import error as SocketError
from xml.sax.saxutils import escape as xml

BUFFER_SIZE = 2048

class ThreadRefresher(Thread):
	"""docstring for ThreadRefresher"""
	def __init__(self, ip, port, socket):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket

	def run(self):
		while True:
			arbostring = updateXML("data")
			str(arbostring)
			send(self, arbostring)
			time.sleep(15)
		
def updateXML(path):
    arborescence = '<dir>\n<name>%s</name>\n' % xml(os.path.basename(path))
    dirs = []
    files = []
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        if os.path.isdir(itempath):
            dirs.append(item)
        elif os.path.isfile(itempath):
            files.append(item)
    if files:
        arborescence += '  <files>\n' + '\n'.join('    <file>\n      <name>%s</name>\n    </file>' % xml(f) for f in files) + '\n  </files>\n'
    if dirs:
        for d in dirs:
            x = updateXML(os.path.join(path, d))
            arborescence += '\n'.join('  ' + line for line in x.split('\n'))
    arborescence += '</dir>'
    return arborescence

def send(self, message):
	self.socket.send(message.encode("Utf8"))
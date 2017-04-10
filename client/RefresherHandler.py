#!/usr/bin/python
# -*-coding:Utf8 -*

import xml.etree.ElementTree as ET
import socket
from threading import Thread
import os

BUFFER_SIZE = 2048

class RefresherHandler(Thread):

	def __init__(self, socket, arbre):
		Thread.__init__(self)
		self.socket = socket
		self.arbre = arbre

	def run(self):
		while True:
			data = self.socket.recv(BUFFER_SIZE)
			if data:
				map(self.arbre.delete, self.arbre.get_children())
				fd = open("client/dataclient/tree.xml", "w")
				fd.write(data)
				fd.close()
				tree = ET.parse('client/dataclient/tree.xml')
				os.remove('client/dataclient/tree.xml')
				root = tree.getroot()
				root.set("root","root")
				update_XML(self.arbre, root, root, "", "")

def update_XML(treeview, root_ance, root, treeview_root, treeview_node):
	for child in root:
		if (child.tag == "name" and child.text == "data"):
			treeview_root = treeview.insert('','end', text=child.text, values = [child.text, "directory"])
		if root_ance.attrib.has_key('root')  and child.tag != "files" and child.tag != "dir":
			treeview_node = treeview.insert(treeview_root, 'end', text = child.text, values = [child.text, "directory"])
			root.set("position", "direct_ances")
		elif child.tag != "files" and child.tag != "dir":
			treeview_node = treeview.insert(treeview_node,'end', text = child.text, values = [child.text, "directory"])
		if (child.tag == "files"):
			for f in child:
				liste = f.findall("name")
				for l in liste:
					if l.text != ".config":
						if root_ance.attrib.has_key('root') and root.attrib.has_key("position") == False:
							treeview.insert(treeview_root,'end', text = l.text, values = [l.text,"file"])
						else:
							treeview.insert(treeview_node, 'end' , text = l.text, values = [l.text, "file"])
		elif child.tag == "dir":
			update_XML(treeview, root, child, treeview_root, treeview_node)	
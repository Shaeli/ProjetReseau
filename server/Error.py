#!/usr/bin/python
# -*-coding:Utf8 -*

class CommandsError(Exception):
	def __init__(self,path,message):
		self.path=path
		self.message=message
#!/usr/bin/python
# -*-coding:Utf8 -*


class AutoCompleter(object): 

    def __init__(self, mots):
        self.mots = sorted(mots)

    def complete(self, text, state):
        if state == 0: 
            if text: 
                self.matches = [i for i in self.mots if i and i.startswith(text)]
            else:  
                self.matches = self.mots[:]
        
        try: 
            return self.matches[state]
        except IndexError:
            return None

    def insert(self, mots):
    	self.mots = sorted(mots)
#!/usr/bin/python
import socket
import threading

import pickle
import datetime

import os
import sys 



NB_Forum = 0


def display_choice(list_to_display):
	j = 0
	for i in  list_to_display :
		j += 1
		print (j,') ',i)

def choice(nb_choice,input_number):
	while 1 :
		if input_number > 0 and input_number <= nb_choice:
			return input_number
		else :
			print ("Che este number no es correct...")
			input_number=input()


def is_in_list(liste, name):
	for i in liste :
		print (i, name)
		if i == name :
			return True
	return False


def file_to_list(path) :
	doc = open(path, "r")
	lines = doc.readlines()
	line = "".join(lines)
	buf = line.split("\n")
	buf.pop()
	return buf

class person :
	
	def __init__(self,name,ID,path):
		self.name = name
		self.ID = ID
		self.path = path	


	def get_ID_path(self):
		if self.path != None :
			j = 0
			source = open(self.path,"r")
			lines = source.readlines()
			for i in lines :
				j += 1
				if i == self.name :
					return j 			
			source.close()
		else :
			print ("no hay path")		
	
	def get_name(self):
		return self.name
		
	def get_ID(self):
		return self.ID

	def add_ID(self,ID):
		self.ID = ID

	def add_name(self,name):
		self.name = name
	
	def get_path(self):
		return self.path

class forum :
	
	def __init__(self,path):
		self.list = []

	def get_list(self):
		return self.list

	def add_chat(self,chat):
		self.list.append(chat.subject)

	def clear(self):
		self.list = []

	def print_forum(self):
		j = 0
		for i in self.list :
			j += 1
			print (j,") ",i)

class chat :
	
	def __init__(self, path, subject):
		self.members = []
		self.numero = path
		self.mesages = []
		self.subject = subject

	
	def add_members(self,member):
		self.members.append(member)
		
	def get_member(self):
		return self.members
	
	def add_mesages(self, mesages, ID):
		self.mesages.append(mesages)

	def get_mesages(self):
		return self.mesages




member = open("member_list.txt","ra")
content = open("chat_content.txt","ra")
front = open("chat_list.txt","ra")

USER = None

cul = '''
if member_list == [] :
	NB_MEMBER = 0
else :
	NB_MEMBER = member_list[0]
'''	
member.close()
member_list = file_to_list("member_list.txt")

web = forum("chat_list.txt")

print ("Bienvenido al forum tienes un user accout ?")
display_choice(["I already have an account","I want to create one"])
nb = input()
nb = choice(2,nb)
if nb == 1 :
	print ("What's your user name")
	nom = raw_input()
	USER = person(nom,-1,"member_list.txt")
	nombre = USER.get_name()
	print (USER.get_name(), USER.get_path(),member_list)
	if is_in_list(member_list, nombre) == True :
		print ("jambon")	
		USER.add_ID(USER.get_ID_path)
		print (USER.get_ID_path())
		print ("login complete")	
	
	
elif nb == 2 :
	print ("Ingresas a name for this forum")
cul = """
print "Bienvenido al forum, eliges un chat o crees uno\n\n1) New subject\n2) Elijir un subjecto\n"
choice = raw_input()
status = False
if choice == 1 :
	print "What's your forum topic ??"
elif choice == 2 :
	"""




content.close()
front.close()





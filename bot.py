#!/usr/bin/python3

# imports
import os
import sys
import time
import random
import socket
import mysql.connector
import difflib

# global variables

# setup some connection with the mysql database

mydb = mysql.connector.connect(
	host="sql_hostname",
	user="sql_username",
	password="sql_password",
	database="sql_database_name"
)

# global functions

# clear terminal method
def ClearTerminal():
	if (os.name == "nt"):
		os.system("cls")
	else:
		os.system("clear")

# the output errors methods

# the output input typo error method
def showInputError():
	ClearTerminal()
	print ("[!!] Sorry but you entered some undesired input!")

# the output open file error method 
def output_open_error():
	ClearTerminal()
	print ("[!!] Problem in opening the inputted file!")

# fix lines method 
def fix_lines(content_array):
	local_array = []
	for line_el in content_array:
		line_el = line_el.strip()
		local_array.append(line_el)
	return local_array

# the main train method
def Train():
	ClearTerminal()
	file = input("Enter filename location [ default is a preset ]: ")
	file = file.strip()
	ClearTerminal()
	if (file == ""):
		file = "./training_/conversation.txt"
	else:
		file = file
		
	try:
		file_ = open(file, "r")
		content = file_.readlines()
		content = fix_lines(content)
		sub_conversations = []
		i = 0
		while i < len(content):
			
			# system 
			string_1 = content[i]
			string_2 = content[i+1]
			
			sub_conversation = [string_1, string_2]
			
			sub_conversations.append(sub_conversation)
			
			# inc the i var 
			i = i + 2
			
			
		# SOME GREAT DEBUGGING STUFF HERE:
		# print(sub_conversations)
		
		# insert the found data into the database
		

		mycursor = mydb.cursor()

		sql = "INSERT INTO bot_answers_questions (Question, Answer) VALUES (%s, %s)"
		for conversation in sub_conversations:
			values = (conversation[0], conversation[1])
			mycursor.execute(sql, values)

			mydb.commit()

			print(mycursor.rowcount, ". Sub-conversation inserted successfully!")

		
	# ah frick this code thennnn
	except Exception:
		output_open_error()
# the talk to method
def TalkTo():
	ClearTerminal()
	print ("Type 'qqt' to exit the chat!")
	print ("----------------------------\n")
	while True:
		question = input("[ You ]: ")
		question = question.strip()
		if (question == "qqt"):
			exit()
		else:
			# select from database
			mycursor = mydb.cursor()
			mycursor.execute("SELECT * FROM bot_answers_questions")
			myresult = mycursor.fetchall()
			most_similar_array = ""
			#print ("Array's Status: " + str(most_similar_array))
			most_similar = 0.0
			for result_line in myresult:
				similarity = difflib.SequenceMatcher(None, question, result_line[0].strip()).ratio()
				#print ("Similarity between " + result_line[0] + " and " + question + ": " + str(similarity))
				if (similarity > most_similar):
					most_similar = similarity
				#	print ("Most similar so far: " + str(result_line))
					most_similar_array = result_line[1]
				else:
					continue
			if (len(most_similar_array) == 0):
				print ("[ Bot ]: Error, I did not understand you!")
			else:
				print ("[ Bot ]: " + most_similar_array)
		
# the main method
def main():
	ClearTerminal()
	print ("\nChatbot [v1.0]")
	print ("	Coded by: MrYes__")
	print ("--------------------------\n")
	print ("[1] Train")
	print ("[2] Talk To")
	user_input_ = input("Choose: ")
	user_input_ = user_input_.strip()

	if (user_input_ == "1"):
		Train()
	elif (user_input_ == "2"):
		TalkTo()
	else:
		showInputError()
# on load "method"
if __name__ == "__main__":
	main()

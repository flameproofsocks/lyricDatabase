import lyricsgenius
import os
from bs4 import BeautifulSoup
import re
from lyricsgenius.api import Genius
from lyricsgenius.song import Song
from lyricsgenius.artist import Artist
from lyricsgenius.utils import sanitize_filename

#######################################
#Sql setup
import psycopg2
connection = psycopg2.connect(user = "postgres",
                                  password = "password",
                                  host = "localhost",
                                  port = "5432",
                                  database = "LilPump1")
connection.autocommit = True
cursor = connection.cursor()
# Print PostgreSQL Connection properties
print ( connection.get_dsn_parameters(),"\n")

# Print PostgreSQL version
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record,"\n")
##########################################

#Take all words into a dictionary
wordDict = { "Test": 1}

#find every item of the list and add it to the dictionary
query = "select lyrics from lyrics"
print ("Writing Query: " + query)
cursor.execute(query)
for lyrics in cursor:
    #print(lyrics, " END ")
    string = str(lyrics[0])
    string = string.replace(")", "^")
    string = string.replace("(", "^")
    string = string.replace("\n", "")
    string = string.replace("â€…", "")
    #string = string.replace("-", " ") 

    #re.sub("\)", "", string ) #regular expression to take out commas/parentheses
    #re.sub("â€…", " ", string ) #regular expression to take out commas/parentheses
    string = string.lower() #to avoid uppercases changing distinct words
    #lyrics[0] = str(lyrics[0].strip('\n') )
    string.strip('\n')
    sentence = string.split("^")
    if(len(sentence) > 1):
        if(sentence[1] in wordDict):
            count = wordDict[sentence[1]]
            wordDict[sentence[1]] = count + 1
        else:
            wordDict[sentence[1]] = 1


print("Finding Most Used Ad-Libs")
#iterate through the dictionary then find top 10 and bottom 10
sortDict = sorted(wordDict.items(), key = lambda kv:(-1*(kv[1]), -1*(kv[0]) ) )
for i in range(10):
    print(sortDict[i])

print("Finding Least Used Ad-Libs")
#iterate through the dictionary then find top 10 and bottom 10
sortDict = sorted(wordDict.items(), key = lambda kv:((kv[1]), (kv[0]) ) )
for i in range(10):
    print(sortDict[i])
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
cur2 = connection.cursor()

# Print PostgreSQL Connection properties
print ( connection.get_dsn_parameters(),"\n")

# Print PostgreSQL version
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record,"\n")
##########################################

#Take all words into a dictionary
#wordDict = { "Test": 1}

#find every item of the list and add it to the dictionary
query = "select lyrics, songID from lyrics"
print ("Writing Query: " + query)
cursor.execute(query)
dictionaryList = []
wordDict = {}

curID = 1
for lyrics, songID in cursor:
    print(lyrics, " END ")
    string = str(lyrics)
    string = string.replace(")", "")
    string = string.replace("(", "")
    string = string.replace("\n", "")
    string = string.replace("â€…", "")
    #string = string.replace("-", " ")
    string = string.replace("!", "")    
    string = string.replace("?", "")    
    string = string.replace("]", "")    
    string = string.replace("[", "")    
    string = string.replace(",", "") 

    #re.sub("\)", "", string ) #regular expression to take out commas/parentheses
    #re.sub("â€…", " ", string ) #regular expression to take out commas/parentheses
    string = string.lower() #to avoid uppercases changing distinct words
    #lyrics[0] = str(lyrics[0].strip('\n') )
    string.strip('\n')
    sentence = string.split(" ")
    print(sentence, "ENDDDDD")
    for i in range(len(sentence) ):
        print(len(wordDict), "--", songID)
        if(sentence[i] in wordDict):
            count = wordDict[sentence[i]]
            wordDict[sentence[i]] = count + 1
        else:
            wordDict[sentence[i]] = 1
    if(songID != curID):
        query2 = ("select title from basics where  songID = " + str(curID))
        cur2.execute(query2)
        stringg = ""
        for title in cur2:
            stringg = str(title)
        dictionaryList.append( [(len(wordDict), stringg)] )
        del(wordDict)
        wordDict = {}
        curID = songID

print(dictionaryList)
print("\n\n\n")
sortList = (sorted(dictionaryList))
print("Least diverse songs")
for i in range(len(sortList)):
    if i < 10:
        print(sortList[i])

print("Most diverse songs")
for i in range(10):
    if i < 10:
        #print( str(len(sortList) - i - 1) , i)
        print(sortList[len(sortList) - i - 1])
# print(wordDict)
# print("LENGTH: ", len(wordDict))

# print("FINDING ORDER")
# #iterate through the dictionary then find top 10 and bottom 10
# sortDict = sorted(wordDict.items(), key = lambda kv:(-1*(kv[1]), -1*(kv[0]) ) )
# for i in range(10):
#     print(sortDict[i])
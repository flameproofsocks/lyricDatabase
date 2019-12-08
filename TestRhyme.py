import lyricsgenius
import os
from bs4 import BeautifulSoup
import re
from lyricsgenius.api import Genius
from lyricsgenius.song import Song
from lyricsgenius.artist import Artist
from lyricsgenius.utils import sanitize_filename
import dandelion
import nltk 
from nltk.corpus import cmudict
from nltk.corpus import timit
import random 
from random import randint

from nltk import compat
from nltk.tree import Tree
from nltk.internals import import_from_stdlib

from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *

nltk.download("timit")
timitdict = nltk.corpus.timit.transcription_dict()


def rhyme(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

def doTheyRhyme(word1, word2):
  # first, we don't want to report 'glue' and 'unglue' as rhyming words
  # those kind of rhymes are LAME
  if word1.find(word2) == len(word1) - len(word2):
      return False
  if word2.find(word1) == len(word2) - len(word1): 
      return False

  return word1 in rhyme(word2, 1)

#######################################
#Sql setup
import psycopg2
connection = psycopg2.connect(user = "postgres",
                                  password = "bippy",
                                  host = "localhost",
                                  port = "5433",
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
offset = 0

def swiperNoSwearing(string):
    string = string.replace("Bitch", "B****")
    string = string.replace("bitch", "b****")
    #string = string.replace("-", " ")
    string = string.replace("Fuck", "F***")    
    string = string.replace("fuck", "f***")  
    string = string.replace("Dick", "D***")    
    string = string.replace("dick", "d***")    
    string = string.replace(" ass", " a**") 
    string = string.replace("Ass ", "A** ") 
    string = string.replace("nigga", "buddy") 
    string = string.replace("Nigga", "Buddy")
    return string 

curID = 1
tempLine = "^" #for unassigned line
phoneticList = []
adList = []
for lyrics, songID in cursor:

    #print(lyrics, " END ")
    string = str(lyrics)
    string = string.replace(")", "^") #Ad-libs should be separate
    string = string.replace(" (", "^")
    l = (string.split("^")) #[0]
    if len(l) > 1:
        adList.append(l[1])
    string = l[0]
    string = string.replace("\n", "")
    string = string.replace("â€…", "")
    #string = string.replace("-", " ")
    string = string.replace("!", "")    
    string = string.replace("?", "")    
    string = string.replace("]", "")    
    string = string.replace("[", "")    
    string = string.replace(",", "") 
    string = swiperNoSwearing(string) #comment in/out to remove swearing

    #re.sub("\)", "", string ) #regular expression to take out commas/parentheses
    #re.sub("â€…", " ", string ) #regular expression to take out commas/parentheses
    string = string.lower() #to avoid uppercases changing distinct words
    #lyrics[0] = str(lyrics[0].strip('\n') )
    string.strip('\n')
    sentence = string.split(" ")
    #print("Sentence: ", sentence)

    try:
        #print(str(timitdict[sentence[len(sentence) - 1] ]) )
        t = timitdict[sentence[len(sentence) - 1] ]
        item = [string, str(t[len(t) - 1]) + str(t[len(t) - 2]), str(sentence[len(sentence) - 1]).strip(" ") ] 
        phoneticList.append(item)
        #print("Item: ", item)
    except:
        ing = 2
        #print("Not in timitdict")
    #item.append(string, timitdict[sentence[len(sentence) - 1] ] )
    #print("Item: ", item)
    #phoneticList.append(item)

print(phoneticList)
for k in range(100000):
    #word = phoneticList[i][1]
    #for j in range(len(phoneticList)):
    i = randint(0,len(phoneticList) -1 )
    j = randint(0,len(phoneticList) -1 )

    if (phoneticList[j][1] == phoneticList[i][1] and phoneticList[j][0] != phoneticList[i][0] and 
    phoneticList[j][2] != phoneticList[i][2] and phoneticList[j][2] != "too" and phoneticList[i][2] != "too" ):
        #print("MAtch:")
        print(phoneticList[i][0], "(" + adList[randint(0,len(adList) - 1) ] + ")" ) #, phoneticList[i][1])
        print(phoneticList[j][0], "(" + adList[randint(0,len(adList) - 1) ] + ")" )
        i = i + 1

    # #print("Checking: " , tempLine,  sentence[len(sentence) - 1] )
    # if offset >= 2 and doTheyRhyme(tempLine, sentence[len(sentence) - 1] ):
    #     print(tempString)
    #     print(string)
    #     tempLine = "^^"
    # offset += 1

    # if tempLine == "^" or 3 == randint(0, 20): #   
    #     tempLine = sentence[len(sentence) - 1]
    #     tempString = string
    #     offset = 0
    #     #print("---Changing Line")

    # if tempLine == "^^":
    #     tempLine = "^"

    # for i in range(len(sentence) ):
    #     #print(len(wordDict), "--", songID)
        
    #     if(sentence[i] in wordDict):
    #         count = wordDict[sentence[i]]
    #         wordDict[sentence[i]] = count + 1
    #     else:
    #         wordDict[sentence[i]] = 1
    # if(songID != curID):
    #     query2 = ("select title from basics where  songID = " + str(curID))
    #     cur2.execute(query2)
    #     stringg = ""
    #     for title in cur2:
    #         stringg = str(title)
    #     dictionaryList.append( [(len(wordDict), stringg)] )
    #     del(wordDict)
    #     wordDict = {}
    #     curID = songID


# #print(dictionaryList)
# print("\n\n\n")
# #sortList = (sorted(dictionaryList))
# print("Least diverse songs")
# for i in range(len(sortList)):
#     if i < 10:
#         print(sortList[i])

# print("Most diverse songs")
# for i in range(10):
#     if i < 10:
#         #print( str(len(sortList) - i - 1) , i)
#         print(sortList[len(sortList) - i - 1])
# # print(wordDict)
# # print("LENGTH: ", len(wordDict))

# # print("FINDING ORDER")
# # #iterate through the dictionary then find top 10 and bottom 10
# # sortDict = sorted(wordDict.items(), key = lambda kv:(-1*(kv[1]), -1*(kv[0]) ) )
# # for i in range(10):
# #     print(sortDict[i])
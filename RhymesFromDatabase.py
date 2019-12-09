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

for i in range(5):
    query = ("SELECT lyrics, rhyme FROM lyrics WHERE rhyme IS NOT NULL ORDER BY random();")
    cursor.execute(query)

    storedRhyme = ""
    storedLyric = ""
    for lyrics, rhyme in cursor:
        #print("Looping")
        if(storedRhyme == "" or randint(0, 10) == 1): #random chance to add another word
            storedRhyme = rhyme
            storedLyric = lyrics
        else:
            finalWord1 = lyrics.split(" ")
            finalWord = finalWord1[len(finalWord1) - 1]

            #the stored final word of each sentence
            sWord = storedLyric.split("(")[0]
            sWord = sWord.strip(" ")
            sWord = sWord.split(" ")[len(sWord.split(" ")) - 1]
            sWord = sWord.lower()
            sWord = sWord.strip("\n")
            sWord = sWord.strip("?")
            sWord = sWord.strip("!")
            nWord = lyrics.split("(")[0]
            nWord = nWord.strip(" ")
            nWord = nWord.split(" ")[len(nWord.split(" ")) - 1]
            nWord = nWord.lower()
            nWord = nWord.strip("\n")
            nWord = nWord.strip("?")
            nWord = nWord.strip("!")
            #print("Words: ", sWord, " - ", nWord)

            if(storedRhyme == rhyme and sWord != nWord ):
                #print("Found a rhyme - ", sWord, " - ", nWord)
                print(lyrics, end = "")
                print(storedLyric)
                storedLyric = ""
                storedRhyme = ""
            
    
print("END")

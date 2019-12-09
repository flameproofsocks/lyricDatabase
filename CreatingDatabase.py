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
print("\n\nDONE\n\n")
genius = lyricsgenius.Genius("1HPkjDIpQ4isWqJ5c6KUTPhEocyts0wY4-_6walbNXff1URRFANQjmZd6QWBcXdb")
api = genius   


artistName = "Ski Mask the Slump God"
artistNameDense = "SkiMaskTheSlumpGod"

artist = api.search_artist(artistName, max_songs=4) #find all the songs. #can be changed to whatever artist.
artist.save_lyrics(extension='txt', verbose = True, overwrite = True, binary_encoding=True) #should be named as "Lyrics_LilPump.txt"
songTitleList = str(artist._songs)
print("Initial list: ", songTitleList)

songTitleList = songTitleList.replace("[", "")
songTitleList = songTitleList.replace("]", "")
songTitleList = songTitleList.replace(", '"+ artistName +"'), (", "^")
songTitleList = songTitleList.replace(", '"+ artistName +"')", "")
songTitleList = songTitleList.replace("(", "")
songTitleList = songTitleList.replace("'", "")
print("Nude list5: ", songTitleList)
songTitleList = (str(songTitleList)).split("^")

#date and duration of song
dateList = []
#durationList = []
for i in range(len(songTitleList) ) :
    try:
        songStuff = api.search_song(songTitleList[i], artistName)
        if songStuff != None:
            if songStuff.year != None:
                dateList.append(songStuff.year)
            else:
                dateList.append("1111-11-11")
            #durationList.append
    except:
        print ("Song exception")
print(dateList)

print(songTitleList)
print("Title: ", (songTitleList[0]), "\n\n")
    
file1 = open("Lyrics_" + artistNameDense + ".txt","r", encoding="utf8") #read-only open the file

lyrics = file1.readlines() #add lines to a list of strings.

#Table for Songs: SongID - title - primary Artist ID - Date Published 
#Lyric Table Format: SongID - Type - Number - Lyric
currentID = 101 #starting for ski mask
lineCount = 0 # = 0 #intro/verse/chorus
verseType = "none"


#writing to song database
query1 = "INSERT INTO basics VALUES(" + str(currentID) + ",'" + (str(songTitleList[0])).strip("'") + "','" + "1" + "','" + dateList[0] + "') ON CONFLICT DO NOTHING;" 
print("Inserting: ", query1)
cursor.execute(query1)

print("Lyrics length: " , len(lyrics) - 2, "\n\n")

for i in range(99) : #iterate through the list

    if (lyrics[i][0] == "_"):
        verseType = "none"
        currentID += 1 #constant for number
        lineCount = 0
        #write to basics
        query1 = "INSERT INTO basics VALUES(" + str(currentID) + ",'" + str(songTitleList[ (currentID-101) ]) + "'," + "1" + ",'" + dateList[currentID-101] + "') ON CONFLICT DO NOTHING;" 
        print("INSERTING into BASICS: " + query1)
        cursor.execute(query1)

    elif(len(lyrics[i]) == 1):
        j = 2 #useless thing, just to catch blank lines. Skip over the line.
    elif (lyrics[i][1] == 'I' and lyrics[i][0] == '['): #intro [I...
        verseType = "Intro"
    elif(lyrics[i][0] + lyrics[i][1] == "[V"):
        verseType = "Verse"
    elif(lyrics[i][0] + lyrics[i][1] == "[C"):
        verseType = "Chorus"
    else:
        #code to write to the database
        query = "INSERT INTO lyrics(songID ,verseType ,lineNumber, lyrics) VALUES(" + str(currentID) + ",'" + verseType + "'," + str(lineCount) + ",'" + lyrics[i].replace("'","") +"') ON CONFLICT DO NOTHING;;"
        #print ("Writing Query: " + query)
        cursor.execute(query)
        lineCount += 1


print("Finished")
query = "select * from lyrics LIMIT 3"
print ("Writing Query: " + query)
cursor.execute(query)
#for (songID, verseType) in cursor:
#   print("{:15} {:10}".format(songID, verseType))

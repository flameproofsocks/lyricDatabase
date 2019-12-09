----Overview
The idea of this project is to create a database of lyrics and songs from various rappers, then mix them together to make an "original song". For previous execution of some of these programs see here: https://youtu.be/b5EfhOvQlGw

This project uses code from John W Miller - https://github.com/johnwmillr/LyricsGenius 

----Setup
You will need to install lyricsgenius from John W Miller in order to scrape lyrics from genius.com
I have from python to a postgreSQL server using pyodbc - First you must create an empty database, then connect with pyodbc. 
Here is some sample code for using pyodbc
import pyodbc 
server = 'localhost' 
database = 'database' 
username = 'root' 
password = 'pass' 
cnxn = pyodbc.connect('DRIVER=DevartODBCMySQL;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()  

(The values for username, database, and password may need to be changed for all the python programs that connect to the database)

----Creating database
First setup the database using the queries from "queries.txt" (This will create a mostly empty database) with two artists.
Next to add lyrics run the script "CreatingDatabase.py", you can replace "artistName" and "artistNameDense" in order to use differnet artists. By default this will only add their most popular 100 songs.

----Generating Lyrics
There are two files to generate lyrics with. One uses a list in python, and the other uses rhymes assigned in the database.
I have done more work with the python list method, though both work.
To run the python list first install NLTK (Python Natural Language Toolkit).
Then run "TestRhyme.py" (this has a function called "swiperNoSwearing" to take out swear words).

To run the database method, first add the rhymes by running "AddRhymes.py" (This requires NLTK)
Then run the program "RhymesFromDatabase.py"
This one doesn't take out swear words.

----Different Stats
To gather the 10 most used and least used Ad-Libs you can run "AdLibs.py" which creates a python dictonary of ad-libs.
"Tests.py" will determine the most and least diverse songs

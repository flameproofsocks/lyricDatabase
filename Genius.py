import lyricsgenius
import os
from bs4 import BeautifulSoup
import re
from lyricsgenius.api import Genius
from lyricsgenius.song import Song
from lyricsgenius.artist import Artist
from lyricsgenius.utils import sanitize_filename

genius = lyricsgenius.Genius("1HPkjDIpQ4isWqJ5c6KUTPhEocyts0wY4-_6walbNXff1URRFANQjmZd6QWBcXdb")

api = genius

# if os.path.isfile("test.json"):
#     os.remove("test.json")
# artist.save_lyrics(filename = "test.json")    

artist = api.search_artist("The Beatles", max_songs=1)
theList = artist._songs
print(theList)
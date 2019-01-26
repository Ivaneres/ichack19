import googlesearch
import requests
from bs4 import BeautifulSoup

maxResults = 50

## megalobiz.com

# @param lyrics - lyrics from user
# @return - returns probable song name in tuple (artist, name)
def get_song_from_lyrics(lyrics):
    results = googlesearch.search(lyrics + " site:genius.com", stop=maxResults)
    for result in results:
        if "GENIUS.COM" in result.upper():
            song_url = result
            break
    else:
        print("Could not find song!")
        return None

    

    #print(lyrics_from_url(song_url))
    return details_from_genius_url(song_url)



def details_from_genius_url(url):
  page = requests.get(url)
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]
  #at least Genius is nice and has a tag called 'lyrics'!
  lyrics = html.find("div", class_="lyrics").get_text()
  pageTitle = html.find("title").get_text()
  print(pageTitle)
  print(pageTitle[:pageTitle.find(" Lyrics | Genius")])
  print( pageTitle[:pageTitle.find(" Lyrics | Genius")].split(" – "))
  artist, title = pageTitle[:pageTitle.find(" Lyrics | Genius")] \
                  .split(" – ")
  return artist, title

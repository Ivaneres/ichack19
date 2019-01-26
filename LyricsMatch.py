maxResults = 50

try:
    #import googlesearch
    from googlesearch.googlesearch import GoogleSearch
    gSearchURLs = lambda search: [i.title for i in GoogleSearch().search(search, num_results=maxResults).results]
except:
    import googlesearch
    gSearchURLs = lambda search: googlesearch.search(search, stop=maxResults)
    
import requests
from bs4 import BeautifulSoup

## megalobiz.com

# @param lyrics - lyrics from user
# @return - returns probable song name in tuple (artist, name)
def get_song_from_lyrics(lyrics):
    #results = googlesearch.search(lyrics + " site:genius.com", stop=maxResults)
    results = gSearchURLs(lyrics + " site:genius.com")
    for result in results:
        if "GENIUS.COM" in result.upper():
            song_url = result
            break
    else:
        print("Could not find song!")
        return None

    return details_from_genius_url(song_url)

def details_from_genius_url(url):
  page = requests.get(url)
  html = BeautifulSoup(page.text, "html.parser")
  [h.extract() for h in html('script')]
  #lyrics = html.find("div", class_="lyrics").get_text()
  pageTitle = html.find("title").get_text()
  print(pageTitle)
  print(pageTitle[:pageTitle.find(" Lyrics | Genius")])
  print( pageTitle[:pageTitle.find(" Lyrics | Genius")].split(" – "))
  artist, title = pageTitle[:pageTitle.find(" Lyrics | Genius")] \
                  .split(" – ")
  return artist, title


def find_lyrics(url):
  page = requests.get(url)
  html = BeautifulSoup(page.text, "html.parser")
  [h.extract() for h in html('script')]
  lyrics = html.find("div", class_="tab-pane fade active in").get_text()
  print(lyrics)
  

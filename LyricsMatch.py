maxResults = 50

import googlesearch

gSearchURLs = lambda search: googlesearch.search(search, stop=maxResults, pause=0)

import requests
from bs4 import BeautifulSoup

FAIL = ("NONE FOUND", "BIG CHUNGUS")


## megalobiz.com

# @param lyrics - lyrics from user
# @return - returns probable song name in tuple (artist, name)
def get_song_from_lyrics(lyrics):
    # results = googlesearch.search(lyrics + " site:genius.com", stop=maxResults)
    results = gSearchURLs(lyrics + " site:genius.com")
    for result in results:
        if result.upper().endswith("LYRICS"):
            song_url = result
            break
    else:
        print("Could not find song!")
        return FAIL

    return details_from_genius_url(song_url)


def details_from_genius_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    # lyrics = html.find("div", class_="lyrics").get_text()
    pageTitle = html.find("title").get_text()
    # print(pageTitle)
    # print(pageTitle[:pageTitle.find(" Lyrics | Genius")])
    # print( pageTitle[:pageTitle.find(" Lyrics | Genius")].split(" – "))
    songTitleArtist = pageTitle[:pageTitle.find(" Lyrics | Genius")] \
                      .replace("\xa0", " ") 
    
    for splitter in [" – ", " - ", "–", "-"]:
        #artist, title = .split()
        res = songTitleArtist.split(splitter)
        if len(res) > 1:
            artist, title = res
            break
    else:
        # Failsafe!
        print("Fail: " + songTitleArtist)
        print(pageTitle)
        print(url)
        return FAIL
    return artist, title
    
def find_mbiz_url(artist, title):
    request_url = "http://www.megalobiz.com/search/all?qry=" + title + " - " + artist
    page = requests.get(request_url)
    html = BeautifulSoup(page.text, "html.parser")
    urldiv = html.find("div", class_="pro_part mid")#.get_text()
    song = urldiv.find("a")
    link = song.attrs["href"]
    return "http://www.megalobiz.com" + link


# @param url - url from megalobiz.com
# @return - list of (timestamp in s, lyric)
def find_lyrics_from_mbiz_url(url):
    # Works with megalobiz.com
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    # lyrics = html.find("div", class_="tab-pane fade active in").get_text()
    lyrics = html.find("div", class_="lyrics_details entity_more_info").get_text()
    lyrics = [l for l in lyrics.split("\n") if l and l[1].isnumeric()]
    lyrics = [l.split("]") for l in lyrics]
    #print(lyrics)
    lyrics = [(str2s(timestamp[1:]), line) for (timestamp, line) in lyrics]
    return lyrics


def str2s(ts):
    # Assumes format (HH:)MM:SS.ss
    ts = ts.split(":")
    ts.reverse()
    mult = 1
    time = 0
    for token in ts:
        time += float(token) * mult
        mult *= 60
    return time

maxResults = 50

import googlesearch

gSearchURLs = lambda search: googlesearch.search(search, stop=maxResults)

import requests
from bs4 import BeautifulSoup


## megalobiz.com

# @param lyrics - lyrics from user
# @return - returns probable song name in tuple (artist, name)
def get_song_from_lyrics(lyrics):
    # results = googlesearch.search(lyrics + " site:genius.com", stop=maxResults)
    results = gSearchURLs(lyrics + " site:genius.com")
    for result in results:
        if "GENIUS.COM" in result.upper():
            song_url = result
            break
    else:
        print("Could not find song!")
        return None

    song_name_artist_tuple = details_from_genius_url(song_url)
    return {"songName": song_name_artist_tuple[0],
            "artistName": song_name_artist_tuple[1]}


def details_from_genius_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    # lyrics = html.find("div", class_="lyrics").get_text()
    pageTitle = html.find("title").get_text()
    # print(pageTitle)
    # print(pageTitle[:pageTitle.find(" Lyrics | Genius")])
    # print( pageTitle[:pageTitle.find(" Lyrics | Genius")].split(" – "))
    artist, title = pageTitle[:pageTitle.find(" Lyrics | Genius")] \
        .split(" – ")
    return artist, title


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
    print(lyrics)
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

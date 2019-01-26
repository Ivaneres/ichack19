import googlesearch

maxResults = 10

## megalobiz.com

# @param lyrics - lyrics from user
# @return - returns probable song name in format {Song Name}, {Smash Mouth}
def get_song_from_lyrics(lyrics):
    results = googlesearch.search(lyrics, stop=maxResults)
    for result in results:
        if "GENIUS" in result.toupper():
            song_url = result
            break
    else:
        print("Could not find song!")

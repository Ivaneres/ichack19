from flask import Flask, jsonify, request
from LyricsMatch import *
from fuzzywuzzy import process
import os

backend = Flask(__name__)

@backend.route("/", methods=["POST"])
def index():
    """
    :return: the URL to the music video/spotify
    """
    js = request.get_json()
    lyrics = js['lyrics']
    song_name_artist_tuple = get_song_from_lyrics(lyrics)
    
    song = song_name_artist_tuple[1]
    artist = song_name_artist_tuple[0]
    
    timestamps = find_lyrics_from_mbiz_url(find_mbiz_url(artist, song))
    mostLikely, prob = process.extractOne(lyrics, timestamps, processor=lambda x: x[1])
    
    # Will give us a tuple (timestamp, lyric)
    # Want to return next timestamp, unless is last.
    
    #mostLikelyTimestamp = timestamps[(timestamps.index(mostLikely)+1) % len(timestamps)]
   
    
    json_dict = {"songName"   : song,
                 "artistName" : artist,
                 "timestamp"  : mostLikely[0]}
                 # To compensate for delays
    
    return jsonify(json_dict)

    
if __name__ == "__main__":
    try:
        port = int(os.environ.get('PORT', 33507))
        backend.run(host='0.0.0.0', port=port)
    except OSError as os:
        print("Failed to start, not bothering!")
        

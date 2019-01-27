from flask import Flask, jsonify, request
from LyricsMatch import get_song_from_lyrics
import os

backend = Flask(__name__)

@backend.route("/", methods=["POST"])
def index(a, b):
    """
    :return: the URL to the music video/spotify
    """
    print(a)
    print([ i for i in ['wsgi.input']])
    print(b)
    print(dir(request))
    print(str(request))
    print(request.get_data())
    print(request.get_json())
    print(request.data)
    print(request.json)
        
    js = request.get_json()
    print(js)
    song_name_artist_tuple = get_song_from_lyrics(js['lyrics'])
    json_dict =  {"songName": song_name_artist_tuple[0],
                  "artistName": song_name_artist_tuple[1]}

    return jsonify(json_dict)

if __name__ == "__main__":
    try:
        port = int(os.environ.get('PORT', 33507))
        backend.run(host='0.0.0.0', port=port)
    except OSError as os:
        print("Failed to start, not bothering!")
        

from flask import Flask, jsonify, request
from LyricsMatch import get_song_from_lyrics
import os


@backend.route("/", methods=["POST"])
def get_music():
    """
    :return: the URL to the music video/spotify
    """
    song_name_artist_tuple = get_song_from_lyrics(request.json['lyrics'])
    json_dict =  {"songName": song_name_artist_tuple[0],
                  "artistName": song_name_artist_tuple[1]}

    return jsonify(json_dict)

if __name__ == "__main__":
    try:
        backend.run(host='0.0.0.0', port=port)
    except OSError as os:
        print("Failed to start, not bothering!")
        

from flask import Flask, jsonify, request
from LyricsMatch import get_song_from_lyrics
import os

port = int(os.environ.get('PORT', 33507))
backend = Flask(__name__)


@backend.route("/", methods=["POST"])
def get_music():
    """
    :return: the URL to the music video/spotify
    """
    sung_text = request.json["lyrics"]
    return jsonify(get_song_from_lyrics(sung_text))


backend.run(host='0.0.0.0', port=port)

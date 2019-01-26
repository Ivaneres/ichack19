from flask import Flask

backend = Flask(__name__)
backend.run()


@backend.route("/", methods=["GET"])
def get_music(sung_text: str) -> str:
    """
    :param sung_text: lyrics that have been sung
    :return: the URL to the music video/spotify
    """
    pass

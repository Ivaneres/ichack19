#from .... import LyricsMatch

import sys, os
#sys.path.append("../../")

print(os.getcwd())
print(sys.path)

import LyricsMatch

getSong = lambda lyrics: LyricsMatch.get_song_from_lyrics(lyrics)

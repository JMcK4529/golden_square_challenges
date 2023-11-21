from lib.track import *

class MusicLibrary:
    # Public properties:
    #   tracks: a list of instances of Track

    def __init__(self):
        self.tracks = []

    def add(self, track):
        # track is an instance of Track
        # Track gets added to the library
        # Returns nothing
        if not isinstance(track, Track):
            raise TypeError("track must be a Track object")
        else:
            self.tracks.append(track)

    def search(self, keyword):
        # keyword is a string
        # Returns a list of instances of track that match the keyword
        if self.tracks == []:
            raise Exception("MusicLibrary contains no Tracks")
        elif not isinstance(keyword, str):
            raise TypeError("keyword must be a string")
        elif keyword == "":
            raise ValueError("keyword cannot be an empty string")
        else:
            print([(track.title, track.matches(keyword)) for track in self.tracks])
            return any([track.matches(keyword) for track in self.tracks])
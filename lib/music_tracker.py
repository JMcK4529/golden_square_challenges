class MusicTracker:
    def __init__(self):
        self.track_list = []

    def add_track(self, track_name):
        if type(track_name) != str:
            raise TypeError("track_name must be a string")
        elif track_name == "":
            raise ValueError("Empty string cannot be a track_name")
        else:
            self.track_list.append(track_name)

    def list_tracks(self):
        return self.track_list
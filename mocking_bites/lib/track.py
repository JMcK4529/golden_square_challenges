class Track:
    def __init__(self, title, artist):
        # title and artist are both strings
        for args in zip([title, artist],["title", "artist"]):
            if type(args[0]) != str:
                raise TypeError(f"{args[1]} must be a string")
            elif args[0] == "":
                raise ValueError(f"{args[1]} cannot be an empty string")
        self.title = title
        self.artist = artist

    def matches(self, keyword):
        # keyword is a string
        # Returns true if the keyword matches either the title or artist
        if type(keyword) != str:
            raise TypeError("keyword must be a string")
        elif keyword == "":
            raise ValueError("keyword cannot be an empty string")
        else:
            if keyword.lower() in [arg.lower() for arg in [self.title, self.artist]]:
                return True
            else:
                return False
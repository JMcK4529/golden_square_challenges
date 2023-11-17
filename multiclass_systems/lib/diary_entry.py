class DiaryEntry:
    def __init__(self, title, contents):
        # Parameters:
        #   title: string
        #   contents: string
        if type(title) != str:
            raise TypeError("Title must be a string")
        elif type(contents) != str:
            raise TypeError("Contents must be a string")
        else:
            self.title = title
            self.contents = contents
            self.chunked_so_far = 0

    def count_words(self):
        # Returns:
        #   int: the number of words in the diary entry
        word_count = 0
        for i in (self.title, self.contents):
            if len(i) > 0:
                word_count += 1 + i.count(" ")
            else:
                word_count += 0
        return word_count

    def reading_time(self, wpm):
        # Parameters:
        #   wpm: an integer representing the number of words the user can read 
        #        per minute
        # Returns:
        #   int: an estimate of the reading time in minutes for the contents at
        #        the given wpm.
        word_count = 0
        if len(self.title) > 0:
            word_count += self.count_words() - 1 - self.title.count(" ")
        else:
            word_count += self.count_words()
        read_time = word_count // wpm
        return read_time

    def reading_chunk(self, wpm, minutes):
        # Parameters
        #   wpm: an integer representing the number of words the user can read
        #        per minute
        #   minutes: an integer representing the number of minutes the user has
        #            to read
        # Returns:
        #   string: a chunk of the contents that the user could read in the
        #           given number of minutes
        #
        # If called again, `reading_chunk` should return the next chunk,
        # skipping what has already been read, until the contents is fully read.
        # The next call after that should restart from the beginning.
        contents_length = self.count_words()
        if len(self.title) > 0:
            contents_length -= 1 + self.title.count(" ")
        chunk_length = wpm * minutes
        word_list = self.contents.split(" ")
        chunk = (" ").join(word_list[self.chunked_so_far:min(contents_length, self.chunked_so_far+chunk_length)])
        if self.chunked_so_far + chunk_length < contents_length:
            self.chunked_so_far += chunk_length
        else:
            self.chunked_so_far = 0
        return chunk
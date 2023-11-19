from lib.diary_entry import *

class Diary:
    def __init__(self):
        self.entry_list = []
        self.title_set = set()

    def add(self, entry):
        # Parameters:
        #   entry: an instance of DiaryEntry
        # Returns:
        #   Nothing
        # Side-effects:
        #   Adds the entry to the entries list
        if type(entry) != DiaryEntry:
            raise TypeError("Diary entries must be DiaryEntry objects.")
        elif entry.title in self.title_set:
            raise ValueError("Diary entries cannot have duplicate titles.")
        else:
            self.entry_list.append(entry)
            self.title_set.add(entry.title)

    def all(self):
        # Returns:
        #   A list of instances of DiaryEntry
        all_list = []
        for entry in self.entry_list:
            all_list.append(entry.title)
        return all_list

    def count_words(self):
        # Returns:
        #   An integer representing the number of words in all diary entries
        # HINT:
        #   This method should make use of the `count_words` method on DiaryEntry.
        total_words = 0
        for entry in self.entry_list:
            total_words += entry.count_words()
        return total_words

    def reading_time(self, wpm):
        # Parameters:
        #   wpm: an integer representing the number of words the user can read
        #        per minute
        # Returns:
        #   An integer representing an estimate of the reading time in minutes
        #   if the user were to read all entries in the diary.
        total_time = 0
        for entry in self.entry_list:
            total_time += entry.reading_time(wpm)
        return total_time

    def find_best_entry_for_reading_time(self, wpm, minutes):
        # Parameters:
        #   wpm:     an integer representing the number of words the user can
        #            read per minute
        #   minutes: an integer representing the number of minutes the user has
        #            to read
        # Returns:
        #   An instance of DiaryEntry representing the entry that is closest to,
        #   but not over, the length that the user could read in the minutes
        #   they have available given their reading speed.
        if len(self.entry_list) == 0:
            raise Exception("Diary is empty!")
        
        best_difference = minutes
        best_entry = None
        for entry in self.entry_list:
            read_time = entry.reading_time(wpm)
            if read_time <= minutes and minutes - read_time <= best_difference:
                best_entry = entry
                best_difference = minutes - read_time

        if best_entry != None:
            return best_entry
        else:
            raise Exception("All entries are too long to read in this time!")

    def extract_contacts(self):
        contacts_list = []
        for entry in self.entry_list:
            if entry.contact != None:
                contacts_list.append(entry.display_contact())
        return contacts_list
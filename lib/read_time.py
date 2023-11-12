# A simple function to return the estimated time required to read a string,
# assuming a reading speed of 200 words per minute.
def read_time(text):
    reading_speed = 200
    if type(text) == type(str()):
        text = text.strip()
        no_of_spaces = text.count(" ")
        if no_of_spaces > 0:
            whitespace_counter = 0
            for i in range(1,len(text)):
                whitespace_counter = whitespace_counter + 1 if text[i] in [" ", "\n"] and text[i-1] not in [" ", "\n"] else whitespace_counter
            no_of_words = whitespace_counter
            time_estimate_minutes = no_of_words/reading_speed
            time_estimate_seconds = round(time_estimate_minutes*60)
        else:
            time_estimate_seconds = 0
        return ("Estimated time to read: " + 
                f"{time_estimate_seconds // 60} min " +
                f"{time_estimate_seconds % 60} sec")
    return "The input was not text."


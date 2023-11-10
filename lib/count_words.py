# Purpose: Take a string as an input, returning the number of words in the
# string.
# Example:
# Call: count_words("This string contains five words.")
# Returns: 5

def count_words(a_string):
    punctuation = [".", ",", "!", "?", ":", ";", "&", "(", ")"]
    if type(a_string) != type(str()):
        return None
    elif a_string == "":
        return 0
    else:
        counter = 0
        split_string = a_string.split(" ")
        for word in split_string:
            if word[-1] in punctuation:
                word = word[:-1]
            if word.isalpha():
                counter += 1
        return counter


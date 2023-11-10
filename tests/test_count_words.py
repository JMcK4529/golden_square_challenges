from lib.count_words import *

def test_wrong_type():
    inputs = [1,2.2,None,[],{}]
    results = []
    for input in inputs:
        if count_words(input) == None:
            results.append(True)
    assert all(results)

def test_empty_string():
    assert count_words("") == 0

def test_words_and_spaces():
    inputs = [".", "One.", "Two words.", "Three more words.",
              "And now four words.", "Five words in this one.",
              "In the final input, six words."]
    results = []
    for input in inputs:
        results.append(count_words(input))
    assert results == [0, 1, 2, 3, 4, 5, 6]

def test_words_and_nonwords():
    inputs = [".", "One.", "One 1.", "Two (2) words.",
              "?a1736 one ll!!ll."]
    results = []
    for input in inputs:
        results.append(count_words(input))
    assert results == [0, 1, 1, 2, 1]


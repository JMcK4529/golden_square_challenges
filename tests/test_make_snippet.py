from lib.make_snippet import *

def test_wrong_type():
    inputs = [1,2.2,None,[],{}]
    results = []
    for input in inputs:
        if make_snippet(input) == None:
            results.append(True)
    assert all(results)

def test_empty_string():
    result = make_snippet("")
    assert result == ""

def test_short_string():
    inputs = ["", "This", "This string", "This string has",
              "This string has five",
              "This string has five words."]
    results = []
    for input in inputs:
        results.append(make_snippet(input))
    assert results == inputs

def test_long_string():
    input = "This string has more words than the truncation limit."
    result = make_snippet(input)
    assert result == "This string has more words..."


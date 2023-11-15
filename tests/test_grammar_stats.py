import pytest
from lib.grammar_stats import *

def test_check_wrong_type():
    grammar_stats = GrammarStats()
    with pytest.raises(TypeError) as err:
        grammar_stats.check(123)
    assert str(err.value) == "Text input must be a string"

def test_check_empty_string():
    grammar_stats = GrammarStats()
    result = grammar_stats.check("")
    assert result == False

def test_check_correct_sentence():
    punctuation = [".", "!", "?"]
    sentence = "This is a sentence"
    grammar_stats = GrammarStats()
    results = []
    for i in punctuation:
        results.append(grammar_stats.check(sentence+i))
    assert results == [True, True, True]

def test_missing_capital():
    grammar_stats = GrammarStats()
    result = grammar_stats.check("this sentence has no capital.")
    assert result == False

def test_percentage_checks():
    grammar_stats = GrammarStats()
    inputs = [""]*6 + ["A."]*4
    for input in inputs:
        grammar_stats.check(input)
    assert grammar_stats.percentage_good() == 40

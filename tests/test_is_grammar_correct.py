import pytest
from lib.is_grammar_correct import *

def test_wrong_type():
    with pytest.raises(TypeError) as error:
        result = is_grammar_correct(123)
    print(error.value, str(error.value))
    assert str(error.value) == "Input was not a string"

def test_empty_string():
    result = is_grammar_correct("")
    assert result == False

def test_full_stop_sentence():
    result = is_grammar_correct("A simple sentence of several words.")
    assert result == True

def test_question_mark_sentence():
    result = is_grammar_correct("Does this work for questions?")
    assert result == True

def test_exclamation_mark_sentence():
    result = is_grammar_correct("Now for an exclamation!")
    assert result == True

def test_missing_capital():
    result = is_grammar_correct("no capital letter.")
    assert result == False


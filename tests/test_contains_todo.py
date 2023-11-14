import pytest
from lib.contains_todo import *

def test_wrong_type():
    with pytest.raises(TypeError) as error:
        result = contains_todo(123)
    assert str(error.value) == "The input was not a string."

def test_empty_string():
    result = contains_todo("")
    assert result == False

def test_simple_todo():
    result = contains_todo("#TODO")
    assert result == True

def test_complex_todo():
    result = contains_todo("This string is a #TODO reminder.")
    assert result == True

def test_not_a_todo():
    result = contains_todo("This string does not contain the phrase!")
    assert result == False


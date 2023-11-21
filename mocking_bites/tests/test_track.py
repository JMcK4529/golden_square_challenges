import pytest
from lib.track import *

def test_init_args():
    type_test_args = [[None, "Artist"],["Title", None]]
    err_strings = ["title", "artist"]
    for args in zip(type_test_args, err_strings):
        with pytest.raises(TypeError) as t_err:
            track = Track(args[0][0], args[0][1])
        assert str(t_err.value) == f"{args[1]} must be a string"
    
    val_test_args = [["", "Artist"], ["Title", ""]]
    for args in zip(val_test_args, err_strings):
        with pytest.raises(ValueError) as v_err:
            track = Track(args[0][0], args[0][1])
        assert str(v_err.value) == f"{args[1]} cannot be an empty string"

def test_init_success():
    track = Track("Title", "Artist")
    assert [track.title, track.artist] == ["Title", "Artist"]

def test_matches_args():
    track = Track("Title", "Artist")
    with pytest.raises(TypeError) as t_err:
        track.matches(None)
    assert str(t_err.value) == "keyword must be a string"

    with pytest.raises(ValueError) as v_err:
        track.matches("")
    assert str(v_err.value) == "keyword cannot be an empty string"

def test_matches_success():
    track = Track("Bohemian Rhapsody", "Queen")
    matches = ["Bohemian Rhapsody", "queen", "bohemian rhapsody", "Queen"]
    unmatches = ["Freddie", "Bohemian", "Rhapsody"]
    for keyword in matches:
        assert track.matches(keyword)
    for keyword in unmatches:
        assert not track.matches(keyword)

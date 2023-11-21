import pytest
from lib.music_library import *
from unittest.mock import Mock

track1 = Mock()
track1.title = "Foo"
track1.artist = "Bar"
track1.__class__ = Track

track2 = Mock()
track2.title = "Py"
track2.artist = "Thon"
track2.__class__= Track

def test_init_success():
    lib = MusicLibrary()
    assert lib.tracks == []

def test_add_args():
    lib = MusicLibrary()
    with pytest.raises(TypeError) as t_err:
        lib.add(None)
    assert str(t_err.value) == "track must be a Track object"

def test_add_success():
    lib = MusicLibrary()
    lib.add(track1)
    assert lib.tracks == [track1]
    lib.add(track2)
    assert lib.tracks == [track1, track2]

def test_search_args():
    lib = MusicLibrary()
    lib.add(track1)
    with pytest.raises(TypeError) as t_err:
        lib.search(None)
    assert str(t_err.value) == "keyword must be a string"
    with pytest.raises(ValueError) as v_err:
        lib.search("")
    assert str(v_err.value) == "keyword cannot be an empty string"

def test_search_no_tracks():
    lib = MusicLibrary()
    with pytest.raises(Exception) as err:
        lib.search("Foo")
    assert str(err.value) == "MusicLibrary contains no Tracks"

def test_search_success():
    lib = MusicLibrary()
    lib.add(track1)
    lib.add(track2)
    assert lib.search("Foo")
    lib.search("Monty")
    track1.matches.assert_called_with("Monty")
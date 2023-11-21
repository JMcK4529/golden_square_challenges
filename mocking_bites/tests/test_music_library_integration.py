import pytest
from lib.track import *
from lib.music_library import *

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
    track1 = Track("Foo", "Bar")
    track2 = Track("Py", "Thon")
    lib.add(track1)
    assert lib.tracks == [track1]
    lib.add(track2)
    assert lib.tracks == [track1, track2]

def test_search_args():
    lib = MusicLibrary()
    track1 = Track("Foo", "Bar")
    lib.add(track1)
    with pytest.raises(TypeError) as t_err:
        lib.search(None)
    assert str(t_err.value) == "keyword must be a string"
    with pytest.raises(ValueError) as v_err:
        lib.search("")
    assert str(v_err.value) == "keyword cannot be an empty string"

def test_search_success():
    lib = MusicLibrary()
    track1 = Track("Foo", "Bar")
    track2 = Track("Py", "Thon")
    lib.add(track1)
    lib.add(track2)
    for keyword_truth_pair in zip(["Foo", "foo", "bah", "Thorn", "PY", "thon", "bar"],
                                  [True, True, False, False, True, True, True]):
        print(keyword_truth_pair)
        assert lib.search(keyword_truth_pair[0]) == keyword_truth_pair[1]
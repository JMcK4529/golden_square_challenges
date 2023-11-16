import pytest
from lib.music_tracker import *

def test_init_track_list():
    my_music = MusicTracker()
    assert my_music.track_list == []

def test_add_track_wrong_type():
    my_music = MusicTracker()
    with pytest.raises(TypeError) as err:
        my_music.add_track(123)
    assert str(err.value) == "track_name must be a string"

def test_add_track_empty_string():
    my_music = MusicTracker()
    with pytest.raises(ValueError) as err:
        my_music.add_track("")
    assert str(err.value) == "Empty string cannot be a track_name"

def test_add_task_correct_track():
    my_music = MusicTracker()
    my_music.add_track("Bohemian Rhapsody")
    assert my_music.track_list == ["Bohemian Rhapsody"]

def test_list_tracks():
    my_music = MusicTracker()
    my_music.add_track("Bohemian Rhapsody")
    my_music.add_track("Yellow Submarine")
    result = my_music.list_tracks()
    assert result == ["Bohemian Rhapsody", "Yellow Submarine"]

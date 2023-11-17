import pytest
from lib.diary import *

def test_init_variables():
    my_diary = Diary()
    assert my_diary.entry_list == []

def test_all_when_empty():
    my_diary = Diary()
    assert my_diary.all() == []

def test_count_words_when_empty():
    my_diary = Diary()
    assert my_diary.count_words() == 0

def test_reading_time_when_empty():
    my_diary = Diary()
    assert my_diary.reading_time(5) == 0

def test_find_best_entry_for_reading_time_when_empty():
    my_diary = Diary()
    with pytest.raises(Exception) as err:
        my_diary.find_best_entry_for_reading_time(5,1)
    assert str(err.value) == "Diary is empty!"
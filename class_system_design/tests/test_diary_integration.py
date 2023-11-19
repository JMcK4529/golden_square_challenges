import pytest
from lib.diary import *
from lib.diary_entry import *
from lib.contact import *

def test_diary_add_duplicate_entry():
    with pytest.raises(ValueError) as err:
        my_diary = Diary()
        entry1 = DiaryEntry("Title", "Some contents.")
        entry2 = DiaryEntry("Title", "Some other contents.")
        my_diary.add(entry1)
        my_diary.add(entry2)
    assert str(err.value) == "Diary entries cannot have duplicate titles."

def test_diary_add_entry():
    my_diary = Diary()
    entry = DiaryEntry("Title", "Some contents.")
    my_diary.add(entry)
    assert my_diary.entry_list == [entry]
    assert my_diary.title_set == set([entry.title])

def test_diary_all_after_adding_entries():
    my_diary = Diary()
    entry1 = DiaryEntry("Title", "Some contents.")
    entry2 = DiaryEntry("Title2", "Some more contents.")
    my_diary.add(entry1)
    my_diary.add(entry2)
    assert my_diary.all() == ["Title", "Title2"]

def test_diary_count_words_after_adding_entries():
    my_diary = Diary()
    entry1 = DiaryEntry("Title", "Some contents.")
    entry2 = DiaryEntry("Title2", "Some more contents.")
    my_diary.add(entry1)
    my_diary.add(entry2)
    assert my_diary.count_words() == 7

def test_diary_reading_time_after_adding_entries():
    my_diary = Diary()
    entry1 = DiaryEntry("Title", "A first set of contents.")
    entry2 = DiaryEntry("Title2", "A second set of contents.")
    my_diary.add(entry1)
    my_diary.add(entry2)
    assert my_diary.reading_time(5) == 2

def test_diary_find_best_entry_for_reading_time_after_adding_entries():
    my_diary = Diary()
    entry1 = DiaryEntry("Title", "A first set of contents.")
    entry2 = DiaryEntry("Title2", "A second set of contents with twice as many words.")
    my_diary.add(entry1)
    my_diary.add(entry2)
    assert my_diary.find_best_entry_for_reading_time(5,1) == entry1

def test_diary_find_best_entry_for_reading_time_all_too_long():
    my_diary = Diary()
    entry1 = DiaryEntry("Title", "A first set of contents.")
    entry2 = DiaryEntry("Title2", "A second set of contents with twice as many words.")
    my_diary.add(entry1)
    my_diary.add(entry2)
    with pytest.raises(Exception) as err:
        my_diary.find_best_entry_for_reading_time(1,1)
    assert str(err.value) == "All entries are too long to read in this time!"

def test_extract_contacts():
    my_diary = Diary()
    entry1 = DiaryEntry("Title", "A first set of contents.", Contact("Some Guy", "01234567890"))
    entry2 = DiaryEntry("Title2", "A second set of contents with twice as many words.")
    my_diary.add(entry1)
    my_diary.add(entry2)
    assert my_diary.extract_contacts() == ["Some Guy: 01234567890"]
import pytest
from lib.diary_entry import *
from lib.contact import *

def test_init_variables():
    entry = DiaryEntry("Title", "Contents")
    assert [entry.title, entry.contents] == ["Title", "Contents"]

def test_argument_types():
    titles = ["Title", 123]
    contents = [123, "Contents"]
    results = []
    for i in range(2):
        with pytest.raises(TypeError) as err:
            entry = DiaryEntry(titles[i],contents[i])
        results.append(str(err.value))
    assert results == ["Contents must be a string", "Title must be a string"]

def test_count_words():
    titles = ["", "word", "two words"]
    contents = ["", "one", "two more"]
    results = []
    for i, j in zip(titles, contents):
        entry = DiaryEntry(i, j)
        results.append(entry.count_words())
    assert results == [0, 2, 4]

def test_reading_time():
    entry = DiaryEntry("Title", "Contents which contains a sentence of ten words in length.")
    results = []
    for wpm in range(1,11):
        results.append(entry.reading_time(wpm))
    assert results == [10, 10//2, 10//3, 10//4, 10//5, 10//6, 10//7, 10//8, 10//9, 1]

def test_reading_chunk_first_call():
    entry = DiaryEntry("Title", "Contents which contains a sentence of ten words in length.")
    result = entry.reading_chunk(5, 1)
    assert result == "Contents which contains a sentence"

def test_reading_chunk_second_call():
    entry = DiaryEntry("Title", "Contents which contains a sentence of ten words in length.")
    result1 = entry.reading_chunk(5, 1)
    result2 = entry.reading_chunk(5, 1)
    assert result2 == "of ten words in length."

def test_reading_chunk_after_finished():
    entry = DiaryEntry("Title", "Contents which contains a sentence of ten words in length.")
    result1 = entry.reading_chunk(5, 1)
    result2 = entry.reading_chunk(5, 1)
    result3 = entry.reading_chunk(5, 1)
    assert result3 == "Contents which contains a sentence"

def test_init_with_contact_wrong_type():
    with pytest.raises(TypeError) as err:
        entry = DiaryEntry("Title", "Contents", "Rubbish")
    assert str(err.value) == "contact must be a Contact object or None"

def test_init_with_contact():
    contact = Contact("Some Guy", "01234567890")
    entry = DiaryEntry("Title", "Contents", contact)
    assert [entry.title, entry.contents, entry.contact] == ["Title", "Contents", contact]

def test_add_contact_wrong_type():
    with pytest.raises(TypeError) as err:
        contact1 = None
        entry = DiaryEntry("Title", "Contents")
        entry.add_contact(contact1)
    assert str(err.value) == "contact must be a Contact object"

def test_display_contact():
    contact = Contact("Some Guy", "01234567890")
    entry = DiaryEntry("Title", "Contents", contact)
    assert entry.display_contact() == f"{contact.name}: {contact.number}"
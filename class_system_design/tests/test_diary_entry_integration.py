import pytest
from lib.diary_entry import *
from lib.contact import *

def test_init_with_contact():
    contact = Contact("Some Guy", "01234567890")
    entry = DiaryEntry("Title", "Contents", contact)
    assert [entry.title, entry.contents, entry.contact] == ["Title", "Contents", contact]

def test_add_contact():
    contact = Contact("Some Guy", "01234567890")
    entry = DiaryEntry("Title", "Contents")
    entry.add_contact(contact)
    assert entry.contact == contact

def test_display_contact():
    contact = Contact("Some Guy", "01234567890")
    entry = DiaryEntry("Title", "Contents", contact)
    assert entry.display_contact() == f"{contact.name}: {contact.number}"
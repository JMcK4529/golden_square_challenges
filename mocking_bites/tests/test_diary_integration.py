import pytest
from lib.secret_diary import *
from lib.diary import *

def test_secret_diary_construction():
    diary = Diary("This document is TOP SECRET.")
    secret = SecretDiary(diary)
    assert secret.diary == diary
    assert secret.locked == True

def test_secret_diary_unlock():
    diary = Diary("This document is TOP SECRET.")
    secret = SecretDiary(diary)
    secret.unlock()
    assert secret.locked == False

def test_secret_diary_lock():
    diary = Diary("This document is TOP SECRET.")
    secret = SecretDiary(diary)
    secret.unlock()
    secret.lock()
    assert secret.locked

def test_secret_diary_read():
    diary = Diary("This document is TOP SECRET.")
    secret = SecretDiary(diary)
    with pytest.raises(Exception) as err:
        secret.read()
    assert str(err.value) == "Go away!"
    secret.unlock()
    assert secret.read() == "This document is TOP SECRET."
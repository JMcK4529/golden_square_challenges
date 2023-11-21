import pytest
from lib.secret_diary import *
from unittest.mock import Mock

def test_construction():
    diary = Mock()
    secret = SecretDiary(diary)
    assert secret.diary == diary
    assert secret.locked == True

def test_unlock():
    diary = Mock()
    secret = SecretDiary(diary)
    secret.unlock()
    assert secret.locked == False

def test_lock():
    diary = Mock()
    secret = SecretDiary(diary)
    secret.unlock()
    secret.lock()
    assert secret.locked

def test_read():
    diary = Mock()
    diary.read.return_value = "This document is TOP SECRET."

    secret = SecretDiary(diary)
    with pytest.raises(Exception) as err:
        secret.read()
    assert str(err.value) == "Go away!"

    secret.unlock()
    assert secret.read() == "This document is TOP SECRET."
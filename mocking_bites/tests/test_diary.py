import pytest
from lib.diary import *

def test_construction():
    diary = Diary("This document is public.")
    assert diary.contents == "This document is public."

def test_read():
    diary = Diary("This document is public.")
    assert diary.read() == diary.contents
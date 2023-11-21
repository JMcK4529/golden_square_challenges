import pytest
from lib.task_formatter import *
from unittest.mock import Mock

def test_construction():
    task = Mock()
    formatter = TaskFormatter(task)
    assert formatter.task == task

def test_format_incomplete_task():
    task = Mock()
    task.title = "Walk the dog"
    task.complete = False
    formatter = TaskFormatter(task)
    assert formatter.format() == "[ ] Walk the dog"

def test_format_complete_task():
    task = Mock()
    task.title = "Walk the cat"
    task.complete = True
    formatter = TaskFormatter(task)
    assert formatter.format() == "[x] Walk the cat"
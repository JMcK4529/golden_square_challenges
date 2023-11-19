import pytest
from lib.todo import *

def test_init_wrong_type():
    with pytest.raises(TypeError) as err:
        todo = Todo(123)
    assert str(err.value) == "task must be a string"

def test_init_empty_string():
    with pytest.raises(ValueError) as err:
        todo = Todo("")
    assert str(err.value) == "Empty string cannot be a task"

def test_init_correct_task():
    todo = Todo("A task")
    assert todo.task == "A task"

def test_mark_complete():
    todo = Todo("A task")
    assert todo.complete == False
    todo.mark_complete()
    assert todo.complete == True
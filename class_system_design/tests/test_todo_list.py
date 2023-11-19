import pytest
from lib.todo_list import *

def test_init_variables():
    todolist = TodoList()
    assert todolist.todo_list == []

def test_add_wrong_type():
    with pytest.raises(TypeError) as err:
        todolist = TodoList()
        todolist.add(123)
    assert str(err.value) == "todo must be a Todo object"

def test_incomplete_before_todos_added():
    todolist = TodoList()
    assert todolist.incomplete() == []

def test_complete_before_todos_added():
    todolist = TodoList()
    assert todolist.complete() == []

def test_give_up_before_todos_added():
    with pytest.raises(Exception) as err:
        todolist = TodoList()
        todolist.give_up()
    assert str(err.value) == "There are no tasks to give up on!"
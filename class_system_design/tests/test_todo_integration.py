import pytest
from lib.todo import *
from lib.todo_list import *

def test_add_todo():
    todolist = TodoList()
    todo = Todo("A task")
    todolist.add(todo)
    assert todolist.todo_list == [todo]

def test_completeness():
    todolist = TodoList()
    todo1 = Todo("A task")
    todo2 = Todo("A second task")
    todolist.add(todo1)
    todolist.add(todo2)
    todo1.mark_complete()
    assert (todolist.incomplete(), todolist.complete()) == ([todo2], [todo1])

def test_give_up():
    todolist = TodoList()
    todo1 = Todo("A task")
    todo2 = Todo("A second task")
    todolist.add(todo1)
    todolist.add(todo2)
    todolist.give_up()
    assert (todolist.incomplete(), todolist.complete()) == ([], [todo1, todo2])
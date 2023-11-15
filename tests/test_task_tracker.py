import pytest
from lib.task_tracker import *

def test_init_list():
    # Does the init method create an empty list
    tracker = TaskTracker()
    assert tracker.task_list == []

def test_add_task_wrong_type():
    # datatype check
    tracker = TaskTracker()
    with pytest.raises(TypeError) as err:
        tracker.add_task(123)
    assert str(err.value) == "Input must be a string"

def test_add_task_empty_string():
    # what does it do with empty strings?
    tracker = TaskTracker()
    with pytest.raises(ValueError) as err:
        tracker.add_task("")
    assert str(err.value) == "Task cannot be an empty string"

def test_add_task_correct_input():
    tracker = TaskTracker()
    tracker.add_task("Some Task")
    assert tracker.task_list == ["Some Task"]

def test_list_tasks():
    # does it return what went in?
    tracker = TaskTracker()
    assert tracker.list_tasks() == tracker.task_list

def test_mark_complete():
    # does the list change (remove task)
    tracker = TaskTracker()
    tracker.add_task('A test task')
    tracker.add_task('Another test task')
    tracker.mark_complete('A test task')
    assert tracker.list_tasks() == ['Another test task']
    
    

def test_mark_complete_nonexist_exception():
    # what happens if you try to complete something that doesn't exist?
    tracker = TaskTracker()
    with pytest.raises(Exception) as err:
        tracker.mark_complete('A test task')
    assert str(err.value) == 'Task does not exist.'
    
 
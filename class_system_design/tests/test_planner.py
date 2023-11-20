import pytest
from lib.planner import *

def test_init_variables():
    planner = Planner()
    assert (planner.diary, planner.todolist) == (None, None)

def test_add_diary_wrong_type():
    with pytest.raises(TypeError) as err:
        planner = Planner()
        planner.add_diary(None)
    assert str(err.value) == "diary must be a Diary object"

def test_add_diary_entry_no_diary():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.add_diary_entry(None)
    assert str(err.value) == "Planner has no diary"

def test_add_contact_no_diary():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.add_contact(None, None)
    assert str(err.value) == "Planner has no diary"

def test_add_todolist_wrong_type():
    with pytest.raises(TypeError) as err:
        planner = Planner()
        planner.add_todolist(None)
    assert str(err.value) == "todolist must be a TodoList object"

def test_add_todo_no_todolist():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.add_todo(None)
    assert str(err.value) == "Planner has no to do list"

def test_list_diary_entries_no_diary():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.list_diary_entries()
    assert str(err.value) == "Planner has no diary"

def test_read_diary_entry_by_title_no_diary():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.read_diary_entry_by_title(None)
    assert str(err.value) == "Planner has no diary"

def test_read_diary_entry_chunk_no_diary():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.read_diary_entry_chunk("",1,1)
    assert str(err.value) == "Planner has no diary"

def test_read_diary_entry_by_time_no_diary():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.read_diary_entry_by_time(None, None)
    assert str(err.value) == "Planner has no diary"

def test_list_contacts_no_diary():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.list_contacts()
    assert str(err.value) == "Planner has no diary"

def test_give_up_all_tasks_no_todolist():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.give_up_all_tasks()
    assert str(err.value) == "Planner has no to do list"

def test_list_incomplete_tasks_no_todolist():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.list_incomplete_tasks()
    assert str(err.value) == "Planner has no to do list"

def test_list_complete_tasks_no_todolist():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.list_complete_tasks()
    assert str(err.value) == "Planner has no to do list"

def test_mark_task_complete_no_todolist():
    with pytest.raises(Exception) as err:
        planner = Planner()
        planner.mark_task_complete(None)
    assert str(err.value) == "Planner has no to do list"
import pytest
from lib.diary import *
from lib.diary_entry import *
from lib.todo_list import *
from lib.todo import *
from lib.contact import *
from lib.planner import *

empty_planner = None
empty_diary = None
contactless_diary_entry1 = None
contactless_diary_entry2 = None
contact1 = None
contact2 = None
empty_todolist = None
todo1 = None
todo2 = None

def diary_setup():
    global empty_planner, empty_diary, contactless_diary_entry1
    global contactless_diary_entry2, contact1, contact2

    empty_planner = Planner()
    empty_diary = Diary()
    contactless_diary_entry1 = DiaryEntry("Title1", "Contents1")
    contactless_diary_entry2 = DiaryEntry("Title2", "Contents2")
    contact1 = Contact("Name1", "01234567890")
    contact2 = Contact("Name2", "09876543210")

def todolist_setup():
    global empty_planner, empty_todolist, todo1, todo2

    empty_planner = Planner()
    empty_todolist = TodoList()
    todo1 = Todo("Task1")
    todo2 = Todo("Task2")

def test_add_diary():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    assert planner.diary == empty_diary

#test_add_diary_entry_wrong_type(): -> see test_diary.py
#test_add_diary_entry_with_wrong_args(): -> see test_diary_entry.py
def test_add_diary_entry():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    planner.add_diary_entry(contactless_diary_entry1)
    assert planner.diary.entry_list == [contactless_diary_entry1]

#test_add_contact_no_diary():
#test_add_contact_wrong_type(): -> see test_diary_entry.py
#test_add_contact_with_wrong_args(): -> see test_contact.py
def test_add_contact_missing_entry():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    title = "Entry Title"
    with pytest.raises(Exception) as err:
        planner.add_contact(title, contact1)
    print(str(err.value))
    assert str(err.value) == f"Diary has no entry {title}"

def test_add_contact():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    planner.add_diary_entry(contactless_diary_entry1)
    planner.add_contact(contactless_diary_entry1.title, contact1)
    assert planner.diary.entry_list[0].contact == contact1

#test_add_todolist_wrong_type(): -> see test_planner.py
def test_add_todolist():
    todolist_setup()
    planner = empty_planner
    planner.add_todolist(empty_todolist)
    assert planner.todolist == empty_todolist

#test_add_todo_no_todo_list(): -> see test_planner.py
#test_add_todo_wrong_type(): -> see test_todo_list.py
#test_add_todo_wrong_args(): -> see test_todo.py
def test_add_todo():
    todolist_setup()
    planner = empty_planner
    planner.add_todolist(empty_todolist)
    planner.add_todo(todo1)
    assert todo1 in planner.todolist.todo_list

#test_list_diary_entries_no_diary(): -> see test_diary.py
def test_list_diary_entries():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    planner.add_diary_entry(contactless_diary_entry1)
    planner.add_diary_entry(contactless_diary_entry2)
    assert planner.list_diary_entries() == [contactless_diary_entry1.title, contactless_diary_entry2.title]

#test_read_diary_entry_by_title_no_diary(): -> see test_diary.py
def test_read_diary_entry_wrong_args():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    with pytest.raises(TypeError) as err:
        planner.read_diary_entry_by_title(None)
    assert str(err.value) == "title must be a string"

def test_read_diary_entry_by_title_missing_entry():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    title = "Entry Title"
    with pytest.raises(ValueError) as err:
        planner.read_diary_entry_by_title(title)
    assert str(err.value) == f"Diary has no entry {title}"

def test_read_diary_entry_by_title():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    planner.add_diary_entry(contactless_diary_entry1)
    planner.add_diary_entry(contactless_diary_entry2)
    assert planner.read_diary_entry_by_title("Title1") == "Contents1"

#test_read_diary_entry_chunk_no_diary(): -> see test_diary.py
def test_read_diary_entry_chunk_wrong_args():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    args = zip([[None, 5, 1], ["Title", None, 1], ["Title", 5, None]],
               [["title", "string"], ['wpm', "integer"], ["minutes", "integer"]])
    for arg in args:
        with pytest.raises(TypeError) as err:
            planner.read_diary_entry_chunk(arg[0][0], arg[0][1], arg[0][2])
        assert str(err.value) == f"{arg[1][0]} must be a {arg[1][1]}"

def test_read_diary_entry_chunk_missing_entry():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    title = "Entry Title"
    with pytest.raises(ValueError) as err:
        planner.read_diary_entry_chunk(title, 5, 1)
    assert str(err.value) == f"Diary has no entry {title}"

def test_read_diary_entry_chunk():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    entry = DiaryEntry("Test", "This contents string contains six words.")
    planner.add_diary_entry(entry)
    planner.add_diary_entry(contactless_diary_entry1)
    result1 = planner.read_diary_entry_chunk("Test", 4, 1)
    result2 = planner.read_diary_entry_chunk("Test", 4, 1)
    result3 = planner.read_diary_entry_chunk("Test", 4, 1)
    assert result1 == "This contents string contains"
    assert result2 == "six words."
    assert result3 == result1

#test_read_entry_by_time_no_diary(): -> see test_diary.py
def test_read_entry_by_time_wrong_args():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    args = zip([None, 1],
                [5, None],
                ["wpm", "minutes"])
    for arg in args:
        print(arg)
        with pytest.raises(TypeError) as err:
            planner.read_diary_entry_by_time(arg[0], arg[1])
        assert str(err.value) == f"{arg[2]} must be an integer"

def test_read_entry_by_time():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    planner.add_diary_entry(contactless_diary_entry1)
    entry = DiaryEntry("Test", "This contents string contains six words.")
    planner.add_diary_entry(entry)
    assert planner.read_diary_entry_by_time(3, 1) == contactless_diary_entry1
    assert planner.read_diary_entry_by_time(6, 1) == entry

#test_list_contacts_no_diary(): -> see test_diary.py
def test_list_contacts_no_entries():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    with pytest.raises(Exception) as err:
        planner.list_contacts()
    assert str(err.value) == "Diary has no contacts"

def test_list_contacts_no_contacts():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    planner.add_diary_entry(contactless_diary_entry1)
    with pytest.raises(Exception) as err:
        planner.list_contacts()
    assert str(err.value) == "Diary has no contacts"

def test_list_contacts():
    diary_setup()
    planner = empty_planner
    planner.add_diary(empty_diary)
    planner.add_diary_entry(contactless_diary_entry1)
    planner.add_diary_entry(contactless_diary_entry2)
    planner.add_contact("Title1", contact1)
    assert planner.list_contacts() == [f"{contact1.name}: {contact1.number}"]
    planner.add_contact("Title2", contact2)
    assert planner.list_contacts() == [f"{contact.name}: {contact.number}" for contact in [contact1, contact2]]

#test_give_up_all_tasks_no_todo_list(): -> see test_planner.py
#test_give_up_all_tasks_no_tasks(): -> see test_todo_list.py
def test_give_up_all_tasks():
    todolist_setup()
    planner = empty_planner
    planner.add_todolist(empty_todolist)
    planner.add_todo(todo1)
    planner.add_todo(todo2)
    planner.give_up_all_tasks()
    for todo in [todo1, todo2]:
        assert todo.complete

#test_list_incomplete_tasks_no_todo_list(): -> see test_planner.py
#test_list_incomplete_tasks_no_tasks(): -> see test_todo_list.py
def test_list_incomplete():
    todolist_setup()
    planner = empty_planner
    planner.add_todolist(empty_todolist)
    planner.add_todo(todo1)
    planner.add_todo(todo2)
    todo1.mark_complete()
    assert planner.list_incomplete_tasks() == [todo2]

#test_list_incomplete_tasks_no_todo_list(): -> see test_planner.py
#test_list_incomplete_tasks_no_tasks(): -> see test_todo_list.py
def test_list_complete():
    todolist_setup()
    planner = empty_planner
    planner.add_todolist(empty_todolist)
    planner.add_todo(todo1)
    planner.add_todo(todo2)
    todo1.mark_complete()
    assert planner.list_complete_tasks() == [todo1]

#test_mark_task_complete_no_todo_list(): -> see test_planner.py
def test_mark_task_wrong_type():
    todolist_setup()
    planner = empty_planner
    planner.add_todolist(empty_todolist)
    with pytest.raises(TypeError) as err:
        planner.mark_task_complete(None)
    assert str(err.value) == "todo must be a Todo object"

def test_mark_task_complete_missing_task():
    todolist_setup()
    planner = empty_planner
    planner.add_todolist(empty_todolist)
    with pytest.raises(ValueError) as err:
        planner.mark_task_complete(todo1)
    assert str(err.value) == f"TodoList contains no task {todo1.task}"

def test_mark_task_complete():
    todolist_setup()
    planner = empty_planner
    planner.add_todolist(empty_todolist)
    planner.add_todo(todo1)
    planner.add_todo(todo2)
    planner.mark_task_complete(todo2)
    assert todo2.complete
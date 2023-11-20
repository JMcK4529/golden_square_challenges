from lib.diary import *
from lib.diary_entry import *
from lib.todo_list import *
from lib.todo import *
from lib.contact import *

class Planner:
    def __init__(self):
        self.diary = None
        self.todolist = None

    def add_diary(self, diary):
        if type(diary) != Diary:
            raise TypeError("diary must be a Diary object")
        else:
            self.diary = diary

    def add_diary_entry(self, entry):
        if self.diary == None:
            raise Exception("Planner has no diary")
        else:
            self.diary.add(entry)

    def add_contact(self, entry_title, contact):
        if self.diary == None:
            raise Exception("Planner has no diary")
        elif entry_title not in self.diary.title_set:
            raise Exception(f"Diary has no entry {entry_title}")
        else:
            [entry.add_contact(contact)
             for entry in self.diary.entry_list
             if entry.title == entry_title]

    def add_todolist(self, todolist):
        if type(todolist) != TodoList:
            raise TypeError("todolist must be a TodoList object")
        else:
            self.todolist = todolist

    def add_todo(self, todo):
        if self.todolist == None:
            raise Exception("Planner has no to do list")
        else:
            self.todolist.add(todo)

    def list_diary_entries(self):
        if self.diary == None:
            raise Exception("Planner has no diary")
        else:
            return self.diary.all()

    def read_diary_entry_by_title(self, title):
        if self.diary == None:
            raise Exception("Planner has no diary")
        elif type(title) != str:
            raise TypeError("title must be a string")
        elif title not in self.diary.title_set:
            raise ValueError(f"Diary has no entry {title}")
        else:
            return [
                    entry.contents
                    for entry in self.diary.entry_list
                    if entry.title == title
                    ][0]

    def read_diary_entry_chunk(self, title, wpm, minutes):
        if self.diary == None:
            raise Exception("Planner has no diary")
        for arg in zip([title, wpm, minutes],
                       [str, int, int],
                       ["title", "wpm", "minutes"],
                       ["string", "integer", "integer"]):
            if type(arg[0]) != arg[1]:
                raise TypeError(f"{arg[2]} must be a {arg[3]}")
        if title not in self.diary.title_set:
            raise ValueError(f"Diary has no entry {title}")
        else:
            return [
                    entry.reading_chunk(wpm, minutes)
                    for entry in self.diary.entry_list
                    if entry.title == title
                    ][0]

    def read_diary_entry_by_time(self, wpm, minutes):
        if self.diary == None:
            raise Exception("Planner has no diary")
        for arg in zip([wpm, minutes],
                       ["wpm", "minutes"]):
            if type(arg[0]) != int:
                raise TypeError(f"{arg[1]} must be an integer")
        return self.diary.find_best_entry_for_reading_time(wpm, minutes)
            
    def list_contacts(self):
        if self.diary == None:
            raise Exception("Planner has no diary")
        elif self.diary.extract_contacts() == []:
            raise Exception("Diary has no contacts")
        else:
            return self.diary.extract_contacts()

    def give_up_all_tasks(self):
        if self.todolist == None:
            raise Exception("Planner has no to do list")
        else:
            self.todolist.give_up()

    def list_incomplete_tasks(self):
        if self.todolist == None:
            raise Exception("Planner has no to do list")
        else:
            return self.todolist.incomplete()

    def list_complete_tasks(self):
        if self.todolist == None:
            raise Exception("Planner has no to do list")
        else:
            return self.todolist.complete()

    def mark_task_complete(self, todo):
        if self.todolist == None:
            raise Exception("Planner has no to do list")
        elif type(todo) != Todo:
            raise TypeError("todo must be a Todo object")
        elif todo not in self.todolist.todo_list:
            raise ValueError(f"TodoList contains no task {todo.task}")
        else:
            todo.mark_complete()
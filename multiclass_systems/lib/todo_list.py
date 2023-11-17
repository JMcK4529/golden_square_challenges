from lib.todo import *

class TodoList:
    def __init__(self):
        self.todo_list = []

    def add(self, todo):
        # Parameters:
        #   todo: an instance of Todo
        # Returns:
        #   Nothing
        # Side-effects:
        #   Adds the todo to the list of todos
        if type(todo) != Todo:
            raise TypeError("todo must be a Todo object")
        else:
            self.todo_list.append(todo)

      
    def incomplete(self):
        # Returns:
        #   A list of Todo instances representing the todos that are not complete
        return [todo for todo in self.todo_list if not todo.complete]

    def complete(self):
        # Returns:
        #   A list of Todo instances representing the todos that are complete
        return [todo for todo in self.todo_list if todo.complete]

    def give_up(self):
        # Returns:
        #   Nothing
        # Side-effects:
        #   Marks all todos as complete
        if len(self.todo_list) == 0:
            raise Exception("There are no tasks to give up on!")
        else:
            for todo in self.todo_list:
                todo.mark_complete()

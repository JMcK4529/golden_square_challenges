"""
As a user
So that I can keep track of my tasks
I want a program that I can add todo tasks to and see a list of them.

As a user
So that I can focus on tasks to complete
I want to mark tasks as complete and have them disappear from the list.
"""

class TaskTracker():

    def __init__(self):
        self.task_list = []
        pass

    def add_task(self, task):
        if type(task) != str:
            raise TypeError("Input must be a string")
        elif len(task) == 0:
            raise ValueError("Task cannot be an empty string")
        else:
            self.task_list.append(task)

    def list_tasks(self):
        return self.task_list

    def mark_complete(self, task):
        if task in self.task_list:
            self.task_list.remove(task)
        else:
            raise Exception('Task does not exist.')
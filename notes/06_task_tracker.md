# Task Tracker Class Design Recipe

## 1. Describe the Problem

> As a user
> So that I can keep track of my tasks
> I want a program that I can add todo tasks to and see a list of them.

> As a user
> So that I can focus on tasks to complete
> I want to mark tasks as complete and have them disappear from the list.

## 2. Design the Class Interface

```python
class TaskTracker:
    # User-facing properties:
    #   none

    def __init__(self):
        # Parameters:
        #   none
        # Side effects:
        #   Creates an empty list (self.task_list) for storing tasks
        pass # No code here yet

    def add_task(self, task):
        # Parameters:
        #   task: string representing a single task
        # Returns:
        #   Nothing
        # Side-effects
        #   Saves the task to the self object in self.task_list
        #   Raises Errors if the task is not a string,
        #   or if it is an empty string
        pass # No code here yet

    def list_tasks(self):
        # Returns:
        #   A list of tasks that the user has added
        # Side-effects:
        #   None
        pass # No code here yet

    def mark_complete(self, task):
        # Returns:
        #   Nothing
        # Side-effects:
        #   Removes the specified task from the self object (self.task_list)
        pass # No code here yet
```

## 3. Create Examples as Tests

_Make a list of examples of how the class will behave in different situations._

``` python
# __init__(self)
"""
When instance is created, there are no tasks in its list.
"""
tracker = TaskTracker()
tracker.task_list # => []

# add_task(self, task)
"""
Given a non-string task
#add_task raises a TypeError
"""
tracker = TaskTracker()
tracker.add_task(123) # raises an error with the message "Input must be a string"

"""
Given an empty string as a task
#add_task raises a ValueError
"""
tracker = TaskTracker()
tracker.add_task("") # raises an error with the message "Task cannot be an empty string"

"""
Given a non-empty string as a task
#add_task adds the task to the task_list
"""
tracker = TaskTracker()
tracker.add_task("Some Task") # nothing is returned but now self.task_list = ["Some Task"]

# list_tasks(self)
"""
When called
#list_tasks returns the task_list
"""
tracker = TaskTracker()
tracker.add_task("Some Task")
tracker.add_task("Some Other Task")
tracker.list_tasks() # => ["Some Task", "Some Other Task"]

# mark_completed(self, task)
"""
Given a task in the task_list
#mark_completed removes that task from the task_list
"""
tracker = TaskTracker()
tracker.add_task("Some Task")
tracker.add_task("Some Other Task")
tracker.mark_completed("Some Task") # nothing is returned but now self.task_list = ["Some Other Task"]

"""
Given a task not in the task_list
#mark_completed raises an Exception
"""
tracker = TaskTracker()
tracker.mark_completed("Some Task") # raises an Exception with the message "Task does not exist."
```

_Encode each example as a test. You can add to the above list as you go._

## 4. Implement the Behaviour

_After each test you write, follow the test-driving process of red, green, refactor to implement the behaviour._

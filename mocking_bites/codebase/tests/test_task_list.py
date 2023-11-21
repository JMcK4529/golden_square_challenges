from lib.task_list import TaskList
from unittest.mock import Mock

def test_task_list_initially_empty():
    task_list = TaskList()
    assert task_list.tasks == []


def test_tasks_initially_not_all_complete():
    task_list = TaskList()
    assert task_list.all_complete() == False

# Unit test `#tasks` and `#all_complete` behaviour
def test_add_tasks():
    task_list = TaskList()
    task_1 = Mock()
    task_2 = Mock()
    task_list.add(task_1)
    task_list.add(task_2)
    assert task_list.tasks == [task_1, task_2]

def test_all_complete():
    task_list = TaskList()
    task_1 = Mock()
    task_2 = Mock()
    assert task_list.all_complete() == False
    
    for mock in (task_1, task_2):
        mock.is_complete.return_value = True
    task_list.add(task_1)
    task_list.add(task_2)
    assert task_list.all_complete()

# task_1.title = "Walk the dog"
# task_1.complete = False
# task_2.title = "Walk the cat"
# task_2.complete = False
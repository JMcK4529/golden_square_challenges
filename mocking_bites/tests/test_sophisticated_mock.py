from unittest.mock import Mock

def test_creates_a_sophisticated_mock():
    # Uncomment and set up your mocks here
    task = Mock()

    task_list = Mock()
    task_list.tasks = []
    task_list.add.side_effect = task_list.tasks.append(task)
    task_list.count.return_value = 1
    task_list.clear.return_value = "success"
    task_list.list.return_value = task_list.tasks

    # Don't edit below
    task_list.add(task)
    assert task_list.list() == [task]
    assert task_list.count() == 1
    assert task_list.clear() == "success"
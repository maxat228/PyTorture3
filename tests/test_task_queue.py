import pytest
from typing import Generator
from src.task_queue import TaskQueue, filter_by_status, filter_by_priority, TaskQueueIterator
from src.task import Task


def test_add_and_len():
    queue = TaskQueue()
    length_one = len(queue)
    assert length_one == 0
    queue.add_task(Task("Example", 4))
    length_two = len(queue)
    assert length_two == 1
    assert length_one != length_two


def test_getitem():
    queue = TaskQueue()
    task = Task("Example", 4)
    queue.add_task(task)
    assert queue[0] == task


def test_iteration():
    queue = TaskQueue()
    queue.add_task(Task("Example1"))
    queue.add_task(Task("Example2", 2))
    queue.add_task(Task("Example3", 3))
    queue.add_task(Task("Example4", 4))
    index = 0
    for task in queue:
        assert task == queue[index]
        index = index + 1


def test_repeat_iteration():
    queue = TaskQueue()
    queue.add_task(Task("Example1"))
    queue.add_task(Task("Example2", 2))
    queue.add_task(Task("Example3", 3))
    queue.add_task(Task("Example4", 4))
    index_one, index_two = 0, 0

    for task in queue:
        assert task == queue[index_one]
        index_one += 1

    for task in queue:
        assert task == queue[index_two]
        index_two += 1

    assert index_one == index_two == 4


def test_filter_by_status():
    queue = TaskQueue()
    task1 = Task("Example1")
    task2 = Task("Example2")
    task3 = Task("Example3")
    task4 = Task("Example4")
    task5 = Task("Example5")
    task1.status = "in_progress"
    task2.status = "in_progress"
    task3.status = "in_progress"
    queue.add_task(task1)
    queue.add_task(task2)
    queue.add_task(task3)
    queue.add_task(task4)
    queue.add_task(task5)
    filtered = list(filter_by_status(queue, "in_progress"))
    assert filtered == [task1, task2, task3]


def test_filter_by_priority():
    queue = TaskQueue()
    queue.add_task(Task("Example1"))
    queue.add_task(Task("Example2", 2))
    queue.add_task(Task("Example3", 2))
    queue.add_task(Task("Example4", 5))
    queue.add_task(Task("Example5", 3))
    filtered = list(filter_by_priority(queue, 5))
    assert len(filtered) == 1
    assert all(task.priority >= 5 for task in filtered)


def test_lazy_filter():
    queue = TaskQueue()
    task1 = Task("Example1")
    task2 = Task("Example2")
    task3 = Task("Example3")
    task4 = Task("Example4")
    task5 = Task("Example5")
    queue.add_task(task1)
    queue.add_task(task2)
    queue.add_task(task3)
    queue.add_task(task4)
    queue.add_task(task5)
    result = filter_by_priority(queue, 1)
    assert isinstance(result, Generator)


def test_stop_iteration():
    queue = TaskQueue()
    queue.add_task(Task("Example1"))
    queue.add_task(Task("Example2", 2))
    queue.add_task(Task("Example3", 3))
    queue.add_task(Task("Example4", 4))
    queue.add_task(Task("Example5", 5))
    queue_iterator = TaskQueueIterator(queue)
    index = 0
    while True:
        if index < len(queue_iterator._queue):
            queue_iterator.__next__()
            index = index + 1
        else:
            with pytest.raises(StopIteration):
                queue_iterator.__next__()
            break

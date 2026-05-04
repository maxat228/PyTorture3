import pytest
from src.task import Task
from src.errors import InvalidPriorityError, InvalidStatusTransitionError


def test_task_creation():
    task = Task("Какая-то задача")
    assert isinstance(task.id, int)
    assert task.priority == 3
    assert task.status == "new"
    assert task.created_at is not None
    assert task.is_ready == True
    assert task.is_completed == False


def test_unique_id():
    task1 = Task("My soul is painted like the wings of butterflies")
    task2 = Task("Fairy tales of yesterday will grow but never die")
    task3 = Task("I can fly, my friends")
    assert task1.id != task2.id
    assert task1.id != task3.id
    assert task2.id != task3.id


def test_priority_validation():
    assert Task("ok", priority=1)
    assert Task("ok", priority=5)

    with pytest.raises(InvalidPriorityError):
        Task("fail", priority=0)
    with pytest.raises(InvalidPriorityError):
        Task("fail", priority=6)
    with pytest.raises(InvalidPriorityError):
        Task("fail", priority="abc")

def test_status_transitions():
    task1 = Task("NEW")
    task1.status = "in_progress"
    task1.status = "done"

    task2 = Task("NEW")
    task2.status = "cancelled"

    task3 = Task("NEW")
    with pytest.raises(InvalidStatusTransitionError):
        task3.status = "done"

    task4 = Task("DONE")
    with pytest.raises(InvalidStatusTransitionError):
        task4.status = "new"


def test_computed_properties():
    task1 = Task("Bla")
    assert task1.is_ready == True
    assert task1.is_completed == False
    task1.status = "in_progress"
    assert task1.is_ready == False
    assert task1.is_completed == False
    task1.status = "done"
    assert task1.is_ready == False
    assert task1.is_completed == True

def test_id_immutability():
    task = Task("Bla")
    first = task.id
    assert task.id == first
    assert task.id == first

def test_non_data_shadowing():
    task1 = Task("Bla")
    first_id = task1.id

    task1.id = 999
    assert task1.id == 999

    del task1.id
    assert task1.id == first_id


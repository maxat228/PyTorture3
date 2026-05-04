from src.task_queue import TaskQueue, filter_by_status, filter_by_priority
from src.task import Task
from src.sources.sources import FileSource, ApiSource, RandomSource


def test_source_to_queue():
    tasks = TaskQueue()
    tasks.load_from_source(FileSource())
    assert all(isinstance(task, Task) for task in tasks)
    assert len(tasks) == 10


def test_queue_iteration_after_load():
    tasks = TaskQueue()
    tasks.load_from_source(ApiSource())
    assert all(isinstance(task, Task) for task in tasks)
    assert len(tasks) == 5


def test_filter_by_priority_after_load():
    tasks = TaskQueue()
    tasks.load_from_source(FileSource())
    filtered = list(filter_by_priority(tasks, 4))
    assert all(task.priority >= 4 for task in filtered)
    assert len(filtered) == 4


def test_filter_after_load():
    tasks = TaskQueue()
    tasks.load_from_source(ApiSource())
    tasks.load_from_source(FileSource())
    tasks.load_from_source(RandomSource(5))
    filtered = list(filter_by_status(tasks, "new"))
    assert all(task.status == "new" for task in filtered)
    assert len(filtered) == 20


def test_full_pipeline():
    tasks = TaskQueue()
    tasks.load_from_source(ApiSource())
    tasks.load_from_source(FileSource())
    tasks.load_from_source(RandomSource(5))
    assert all(isinstance(task, Task) for task in tasks)
    assert len(tasks) == 20

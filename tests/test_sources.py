from src.task import Task
from src.sources.sources import FileSource, ApiSource, RandomSource
from src.sources.loader import load_tasks
from src.sources.protocols import TaskSource


def test_from_source_file():
    task = Task.from_source(FileSource())
    assert isinstance(task, Task)
    assert task.status == "new"
    assert 1 <= task.priority <= 5


def test_from_source_api():
    task = Task.from_source(ApiSource())
    assert isinstance(task, Task)
    assert task.status == "new"
    assert 1 <= task.priority <= 5


def test_from_source_random():
    task = Task.from_source(RandomSource(5))
    assert isinstance(task, Task)
    assert task.status == "new"
    assert 1 <= task.priority <= 5


def test_tasks_from_sources():
    tasks = []
    for source in [FileSource(), ApiSource(), RandomSource(5)]:
        load_tasks(source, tasks)
    assert len(tasks) == 20
    assert all(isinstance(task, Task) for task in tasks)


def test_source_contract():
    assert isinstance(FileSource(), TaskSource)
    assert isinstance(ApiSource(), TaskSource)
    assert isinstance(RandomSource(5), TaskSource)

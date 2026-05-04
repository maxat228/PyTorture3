from src.sources.protocols import TaskSource
from src.task import Task
from typing import List


def load_tasks(source: TaskSource, tasks: List[Task]) -> None:
    for task in source.get_tasks():
        tasks.append(task)
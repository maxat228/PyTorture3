from src.task import Task
from src.sources.protocols import TaskSource
from typing import List, Generator, Union


class TaskQueue:
    def __init__(self) -> None:
        self._tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def __len__(self) -> int:
        return len(self._tasks)

    def __getitem__(self, index: Union[int, slice]) -> Union[Task, List[Task]]:
        return self._tasks[index]

    def __iter__(self) -> "TaskQueueIterator":
        return TaskQueueIterator(self)

    def load_from_source(self, source: TaskSource) -> None:
        for task in source.get_tasks():
            self.add_task(task)


class TaskQueueIterator:
    def __init__(self, queue: TaskQueue) -> None:
        self._queue = queue
        self._index = 0

    def __iter__(self) -> "TaskQueueIterator":
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._queue):
            raise StopIteration
        task = self._queue[self._index]
        self._index += 1
        return task


def filter_by_status(queue: TaskQueue, status: str) -> Generator[Task, None, None]:
    for task in queue:
        if task.status == status:
            yield task

def filter_by_priority(queue: TaskQueue, priority: int) -> Generator[Task, None, None]:
    for task in queue:
        if task.priority >= priority:
            yield task


from typing import Protocol, Iterator, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.task import Task

@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterator["Task"]:
        ...
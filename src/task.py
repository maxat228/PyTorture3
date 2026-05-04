from datetime import datetime
from src.descriptors import TaskId, PriorityValidator, StatusValidator
from src.sources.protocols import TaskSource


class Task:
    id = TaskId()
    priority = PriorityValidator()
    status = StatusValidator()

    def __init__(self, description: str, priority: int = 3) -> None:
        self.description = description
        self.priority = priority
        self.status = "new"
        self._created_at = datetime.now()

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def is_ready(self) -> bool:
        return self.status == "new"

    @property
    def is_completed(self) -> bool:
        return self.status == "done"

    @property
    def summary(self) -> str:
        return (f"Описание: {self.description}, id: {self.id}, статус: {self.status}, приоритет: {self.priority} "
                f"Время создания: {self.created_at}")

    @classmethod
    def from_source(cls, source: TaskSource) -> "Task":
        return next(source.get_tasks())

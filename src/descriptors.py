from typing import Any
from src.errors import InvalidStatusTransitionError, InvalidPriorityError


class TaskId:
    def __init__(self) -> None:
        self.index = 0

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        if "_id" not in instance.__dict__:
            instance.__dict__["_id"] = self.index

        self.index += 1
        return instance.__dict__["_id"]


class PriorityValidator:
    def __init__(self, default: int = 3, minimum: int = 1, maximum: int = 5) -> None:
        self.default = default
        self.minimum = minimum
        self.maximum = maximum
        self.storage_name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name, self.default)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise InvalidPriorityError(f"Значение должно быть целым числом, получено {value.__class__.__name__}")
        if value < self.minimum or value > self.maximum:
            raise InvalidPriorityError(f"Значение должно быть от {self.minimum} до {self.maximum}, "
                                       f"получено {value}")
        instance.__dict__[self.storage_name] = value


class StatusValidator:
    VALID_STATUSES = {"new": ["in_progress", "cancelled"],
                      "in_progress": ["done", "cancelled"],
                      "done": [],
                      "cancelled": []}

    def __init__(self, default: str = "new") -> None:
        self.default = default
        self.storage_name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name, self.default)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, str):
            raise InvalidStatusTransitionError(f"Значение должно быть строкой, получено {value.__class__.__name__}")
        if not value in self.VALID_STATUSES:
            raise InvalidStatusTransitionError(f"Значение статуса недопустимо, получено {value}")

        current = instance.__dict__.get(self.storage_name)

        if current is not None and value not in self.VALID_STATUSES[current]:
            raise InvalidStatusTransitionError(f"Переход из {instance.__dict__[self.storage_name]}"
                                               f" в {value} не разрешен")

        instance.__dict__[self.storage_name] = value

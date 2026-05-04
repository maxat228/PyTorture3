import os
from src.task import Task
from typing import Iterator
from random import randint


class FileSource:
    def get_tasks(self) -> Iterator[Task]:
        tasks = []
        path = os.path.join(os.path.dirname(__file__), "..", "..", "tasks.txt")
        with open(path, encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                description, priority = line.strip().split(",")
                tasks.append(Task(description=description, priority=int(priority)))
        return iter(tasks)


class RandomSource:
    def __init__(self, count: int) -> None:
        self.count = count

    def get_tasks(self) -> Iterator[Task]:
        tasks = []
        for number in range(self.count):
            tasks.append(Task(description=f"Сгенерированная задача #{number}", priority=randint(1, 5)))
        return iter(tasks)


class ApiSource:
    def get_tasks(self) -> Iterator[Task]:
        tasks = [
            Task(description="Срочный багфикс в продакшене", priority=5),
            Task(description="Обновить логотип компании", priority=2),
            Task(description="Ответить на тикет клиента #4521", priority=4),
            Task(description="Проверить логи сервера", priority=3),
            Task(description="Созваниться с командой дизайна", priority=1),
        ]
        return iter(tasks)

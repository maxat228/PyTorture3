from src.task_queue import TaskQueue, filter_by_priority, filter_by_status
from src.task import Task
from src.sources.sources import FileSource, RandomSource, ApiSource
from random import randint

# Очередь и итерация
print("--- Показываю очередь и итерации ---")
queue = TaskQueue()
queue.add_task(Task("Example #1"))
queue.add_task(Task("Example #2", 2))
queue.add_task(Task("Example #3", 3))
queue.add_task(Task("Example #4", 4))

print("Первый обход:")
for task in queue:
    print(task.summary)
print("\nВторой обход:")
for task in queue:
    print(f"Задание №{task.id}")

# Генераторы и фильтры
print("\n --- Показываю генераторы и фильтры ---")
queue.add_task(Task("Example #5", 5))
queue.add_task(Task("Example #6", 5))
filtered_by_priority_four = list(filter_by_priority(queue, 4))
print("Ниже задачи с приоритетом выше четырех, отобранные с помощью генератора filter_by_priority")
for task in filtered_by_priority_four:
    print(task.summary)

print("\nНиже задачи со статусом in_progress, отобранные с помощью генератора filter_by_status")
queue[0].status = "in_progress"
queue[1].status = "in_progress"
filtered_by_status_in_progress = list(filter_by_status(queue, "in_progress"))
for task in filtered_by_status_in_progress:
    print(task.summary)

# Загрузка из источников
print("\n --- Показываю загрузку из источников ---")
queue = TaskQueue()
queue.load_from_source(FileSource())
queue.load_from_source(RandomSource(5))
queue.load_from_source(ApiSource())
print("Ниже 20 задач из источников FileSource, RandomSource, ApiSource:")
for number, task in enumerate(queue):
    if number < 10:
        print(f"Из FileSource: [{task.summary}]")
    elif number < 15:
        print(f"Из RandomSource: [{task.summary}]")
    else:
        print(f"Из ApiSource: [{task.summary}]")

# Полный пайплайн
print("\n --- Показываю полный пайплайн ---")
queue = TaskQueue()
queue.load_from_source(FileSource())
queue.load_from_source(RandomSource(5))
queue.load_from_source(ApiSource())

for i in range(len(queue) // 3 * 2):
    queue[i].status = "in_progress"
    queue[i].status = "done"

first_filtered = filter_by_status(queue, "done")
queue1 = TaskQueue()
for task in first_filtered:
    queue1.add_task(task)

second_filtered = filter_by_priority(queue1, 4)
print("Ниже задачи со статусом done и приоритетом 4 из FileSource, RandomSource, ApiSource:")
for task in second_filtered:
    print(task.summary)

# Доказательство ленивости
print("\n --- Показываю доказательство ленивости генераторов ---")
queue = TaskQueue()
priority = randint(1, 5)
queue.load_from_source(RandomSource(20))
generator = filter_by_priority(queue, priority)
try:
    for _ in range(5):
        print(next(generator).summary)
except StopIteration:
    print(f"Задачи с приоритетом {priority} закончились!")


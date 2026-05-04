class TaskError(Exception):
    """Базовая ошибка Task."""
    pass

class InvalidPriorityError(TaskError):
    """Ошибка некорректного приоритета Task."""
    pass

class InvalidStatusTransitionError(TaskError):
    """Ошибка некорректного статуса задачи."""
    pass

class TaskNotFoundError(TaskError):
    """Ошибка поиска задачи"""
    pass

import time
from functools import wraps

def log_time(func):
    """
    Декоратор для замера времени выполнения функции.
    Выводит время в формате: Функция <имя_функции> выполнилась за X.XXX секунд.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {execution_time:.3f} секунд")
        return result
    return wrapper
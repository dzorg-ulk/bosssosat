import time
from functools import wraps

# 1. Декоратор для измерения времени выполнения функции
def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция '{func.__name__}' выполнилась за {end_time - start_time:.6f} секунд.")
        return result
    return wrapper

# 2. Декоратор для логирования вызова функции
def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Вызов функции '{func.__name__}' с аргументами: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] Функция '{func.__name__}' вернула: {result}")
        return result
    return wrapper

# 3. Декоратор для повторного выполнения функции при ошибке (с ограничением попыток)
def retry_decorator(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[RETRY] Ошибка в функции '{func.__name__}': {e}. Попытка {attempts}/{max_attempts}.")
                    time.sleep(delay)
            raise Exception(f"Функция '{func.__name__}' не выполнилась после {max_attempts} попыток.")
        return wrapper
    return decorator

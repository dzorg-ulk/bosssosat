import time
import logging
from typing import List, Any

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def fib_iterative(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fib_recursive(n: int) -> int:
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start


def sum_nested_list(lst: List[Any]) -> int:
    total = 0
    for item in lst:
        if isinstance(item, list):
            total += sum_nested_list(item)
        else:
            total += item
    return total


def main():
    logger.info("\n""СРАВНЕНИЕ ИТЕРАТИВНОЙ И РЕКУРСИВНОЙ ФУНКЦИЙ ФИБОНАЧЧИ")

    n = 50

    logger.info(f"\nВычисление {n}-го числа Фибоначчи:")

    result_iter, time_iter = measure_time(fib_iterative, n)
    logger.info(f"Итеративная функция: {result_iter}")
    logger.info(f"Время выполнения: {time_iter:.6f} секунд")

    result_rec, time_rec = measure_time(fib_recursive, 30)
    logger.info(f"\nРекурсивная функция (только до 30 из-за времени): {result_rec}")
    logger.info(f"Время выполнения (для n=30): {time_rec:.6f} секунд")

    logger.info(f"\nИтеративная функция быстрее в {time_rec / time_iter:.0f} раз для n=30")
    logger.info("Рекурсивная функция для n=50 не выполняется из-за экспоненциальной сложности")

    logger.info("\n""СУММА ВЛОЖЕННОГО СПИСКА")

    test_list = [1, [2, 3], [4, [5, 6]], [-1, -5], 0]
    logger.info(f"\nТестовый список: {test_list}")

    total_sum = sum_nested_list(test_list)
    logger.info(f"Сумма всех чисел: {total_sum}")

    logger.info("\n""ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ФИБОНАЧЧИ")

    test_values = [0, 1, 5, 10, 20]
    for val in test_values:
        res_iter, t_iter = measure_time(fib_iterative, val)
        res_rec, t_rec = measure_time(fib_recursive, val)
        logger.info(f"\nn={val:2}: Итеративно={res_iter:7} ({t_iter:.6f}с), "
                    f"Рекурсивно={res_rec:7} ({t_rec:.6f}с)")

    logger.info("\n""ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ СУММЫ")


    test_cases = [
        ([1, 2, 3, 4, 5], 15),
        ([], 0),
        ([1, [2, [3, [4, [5]]]]], 15),
        ([[[-10]], 20, [[30, -40]]], 0),
    ]

    for lst, expected in test_cases:
        result = sum_nested_list(lst)
        logger.info(f"Список: {lst}")
        logger.info(f"Ожидаемая сумма: {expected}, Получено: {result}, "
                    f"Совпадает: {expected == result}")


if __name__ == "__main__":
    main()
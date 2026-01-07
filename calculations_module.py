import math
from decorators_module import timer_decorator, logger_decorator

# Применим декораторы к некоторым функциям для демонстрации
@timer_decorator
def linear(x):
    """Линейная функция: y = 2x + 3"""
    return 2 * x + 3

@logger_decorator
def quadratic(x):
    """Квадратичная функция: y = x^2 - 4x + 4"""
    return x**2 - 4*x + 4

def trigonometric(x):
    """Тригонометрическая функция: y = sin(x) + cos(x)"""
    return math.sin(x) + math.cos(x)

def exponential(x):
    """Экспоненциальная функция: y = e^x"""
    return math.exp(x)

def logarithmic(x):
    """Логарифмическая функция: y = ln(x + 1)"""
    if x + 1 <= 0:
        raise ValueError("Логарифм не определён для неположительных чисел")
    return math.log(x + 1)

# Словарь функций для удобного выбора
functions = {
    '1': linear,
    '2': quadratic,
    '3': trigonometric,
    '4': exponential,
    '5': logarithmic
}

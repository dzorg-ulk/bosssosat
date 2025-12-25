# visualization_module.py

import matplotlib.pyplot as plt
from tabulate import tabulate


def plot_xy(x_vector, y_vector, title="График функции"):
    """Построение графика по векторам X и Y."""
    plt.figure(figsize=(10, 6))
    plt.plot(x_vector, y_vector, 'b-', linewidth=2, label='y = f(x)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()


def print_xy_table(x_vector, y_vector, precision=4):
    """Вывод таблицы X и Y в две строки с заданной точностью."""
    # Округление значений
    x_rounded = [round(x, precision) for x in x_vector]
    y_rounded = [round(y, precision) for y in y_vector]

    # Создание таблицы
    table_data = [["X"] + x_rounded, ["Y"] + y_rounded]
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

    # Альтернативно можно вывести просто двумя строками:
    print(f"\nX: {x_rounded}")
    print(f"Y: {y_rounded}")
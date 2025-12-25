# main.py (альтернативная версия без numpy)

from calculations_module import functions
from visualization_module import plot_xy, print_xy_table


def main():
    print("ПРОГРАММА ДЛЯ ВЫЧИСЛЕНИЯ И ВИЗУАЛИЗАЦИИ ФУНКЦИЙ")

    # Выбор функции
    print("\nДоступные функции:")
    print("1. Линейная: y = 2x + 3")
    print("2. Квадратичная: y = x^2 - 4x + 4")
    print("3. Тригонометрическая: y = sin(x) + cos(x)")
    print("4. Экспоненциальная: y = e^x")
    print("5. Логарифмическая: y = ln(x + 1)")

    while True:
        choice = input("\nВыберите функцию (1-5): ").strip()
        if choice in functions:
            selected_func = functions[choice]
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    # Ввод параметров
    try:
        a = float(input("Введите начало интервала (a): "))
        b = float(input("Введите конец интервала (b): "))
        step = float(input("Введите шаг: "))
    except ValueError:
        print("Ошибка: введите числовые значения.")
        return

    # Генерация векторов X и Y (без numpy)
    try:
        # Создаем список значений X
        x_vector = []
        current = a
        while current <= b:
            x_vector.append(current)
            current += step

        # Если последнее значение пропущено из-за ошибок округления
        if b not in x_vector and abs(b - x_vector[-1]) > step / 100:
            x_vector.append(b)

        y_vector = [selected_func(x) for x in x_vector]
    except Exception as e:
        print(f"Ошибка при вычислении функции: {e}")
        return

    # Вывод результатов
    print("\n" + "=" * 50)
    print(f"Функция: {selected_func.__name__}")
    print(f"Интервал: [{a}, {b}], шаг: {step}")
    print(f"Количество точек: {len(x_vector)}")
    print("=" * 50)

    # Вывод таблицы
    print("\nТАБЛИЦА ЗНАЧЕНИЙ:")
    print_xy_table(x_vector, y_vector)

    # Построение графика
    print("\nГРАФИК ФУНКЦИИ:")
    plot_xy(x_vector, y_vector, title=f"График функции: {selected_func.__name__}")

    print("\nПрограмма завершена.")


if __name__ == "__main__":
    main()
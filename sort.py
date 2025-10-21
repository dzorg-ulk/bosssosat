import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",  encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s' )


# пузырьковая сортировка
def puzyr(nums):
    logging.info(f"Начало пузырьковой сортировки: {nums}")
    flag = True
    iterations = 0
    outer_iterations = 0

    while flag:
        outer_iterations += 1
        flag = False
        logging.info(f"Внешняя итерация {outer_iterations}: {nums}")

        for i in range(len(nums) - 1):
            iterations += 1
            logging.info(f"Итерация {iterations}: сравниваем элементы {nums[i]} и {nums[i + 1]}")

            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                flag = True
                logging.info(f"Обмен: {nums[i + 1]} <-> {nums[i]}, новый массив: {nums}")

    logging.info(f"Конец пузырьковой сортировки: {nums}")
    logging.info(f"Всего итераций: {iterations}, внешних итераций: {outer_iterations}")
    return iterations, outer_iterations


random_nums = [15, 2, 135, 789, 3]
iterations, outer_iterations = puzyr(random_nums)
print(f"Пузырьковая сортировка: {random_nums}")
print(f"Итераций: {iterations}, внешних итераций: {outer_iterations}\n")


# Сортировка выборкой
def vyborka(nums):
    logging.info(f"Начало сортировки выборкой: {nums}")
    iterations = 0

    for i in range(len(nums)):
        iterations += 1
        logging.info(f"Внешняя итерация {i + 1}: {nums}")
        indexminznach = i

        for j in range(i + 1, len(nums)):
            iterations += 1
            logging.info(f"Внутренняя итерация: сравниваем {nums[j]} и {nums[indexminznach]}")

            if nums[j] < nums[indexminznach]:
                indexminznach = j
                logging.info(f"Новый минимальный элемент: {nums[indexminznach]} на позиции {indexminznach}")

        if indexminznach != i:
            nums[i], nums[indexminznach] = nums[indexminznach], nums[i]
            logging.info(f"Обмен: {nums[indexminznach]} <-> {nums[i]}, новый массив: {nums}")

    logging.info(f"Конец сортировки выборкой: {nums}")
    logging.info(f"Всего итераций: {iterations}")
    return iterations


random_nums = [1, 8000, 37, 52, 11]
iterations = vyborka(random_nums)
print(f"Сортировка выборкой: {random_nums}")
print(f"Итераций: {iterations}\n")


# сортировка вставками
def vstavki(nums):
    logging.info(f"Начало сортировки вставками: {nums}")
    iterations = 0

    for i in range(1, len(nums)):
        iterations += 1
        logging.info(f"Итерация {i}: текущий массив {nums}")
        dlyavstavki = nums[i]
        logging.info(f"Элемент для вставки: {dlyavstavki}")
        j = i - 1

        while j >= 0 and nums[j] > dlyavstavki:
            iterations += 1
            nums[j + 1] = nums[j]
            logging.info(f"Сдвиг элемента {nums[j]} на позицию {j + 1}: {nums}")
            j -= 1

        nums[j + 1] = dlyavstavki
        logging.info(f"Вставка элемента {dlyavstavki} на позицию {j + 1}: {nums}")

    logging.info(f"Конец сортировки вставками: {nums}")
    logging.info(f"Всего итераций: {iterations}")
    return iterations


random_list_of_nums = [91, 1, 15, 28, 6]
iterations = vstavki(random_list_of_nums)
print(f"Сортировка вставками: {random_list_of_nums}")
print(f"Итераций: {iterations}\n")

import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")


# Пирамидальная сортировка (исправленная версия)
def heapify(nums, heap_size, root_index, iterations_counter):
    iterations_counter[0] += 1
    current_iteration = iterations_counter[0]

    # Проверяем, что root_index в пределах массива
    if root_index >= heap_size or root_index < 0:
        logging.info(f"Heapify итерация {current_iteration}: недопустимый root_index {root_index}")
        return

    logging.info(
        f"Heapify итерация {current_iteration}: корень {root_index}, значение {nums[root_index]}, массив {nums}")
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2

    # Проверяем границы перед обращением к элементам
    left_child_value = nums[left_child] if left_child < heap_size else "N/A"
    right_child_value = nums[right_child] if right_child < heap_size else "N/A"

    logging.info(f"Левый потомок: индекс {left_child}, значение {left_child_value}")
    logging.info(f"Правый потомок: индекс {right_child}, значение {right_child_value}")

    # Если левый потомок корня — допустимый индекс, а элемент больше,
    # чем текущий наибольший, обновляем наибольший элемент
    if left_child < heap_size and nums[left_child] > nums[largest]:
        largest = left_child
        logging.info(f"Новый наибольший: левый потомок {nums[largest]}")

    # То же самое для правого потомка корня
    if right_child < heap_size and nums[right_child] > nums[largest]:
        largest = right_child
        logging.info(f"Новый наибольший: правый потомок {nums[largest]}")

    # Если наибольший элемент больше не корневой, они меняются местами
    if largest != root_index:
        nums[root_index], nums[largest] = nums[largest], nums[root_index]
        logging.info(f"Обмен: {nums[largest]} <-> {nums[root_index]}, новый массив: {nums}")
        # Heapify the new root element to ensure it's the largest
        heapify(nums, heap_size, largest, iterations_counter)


def heap_sort(nums):
    logging.info(f"Начало пирамидальной сортировки: {nums}")
    n = len(nums)
    iterations_counter = [0]  # Используем список для передачи по ссылке

    # Создаём Max Heap из списка
    logging.info("Построение Max Heap:")
    for i in range(n, -1, -1):
        # Добавляем проверку, что i в пределах массива
        if i < n:
            iterations_counter[0] += 1
            logging.info(f"Построение кучи: обработка элемента {i}")
            heapify(nums, n, i, iterations_counter)
        else:
            logging.info(f"Пропуск элемента {i} (вне границ массива)")

    logging.info(f"Max Heap построен: {nums}")

    # Перемещаем корень Max Heap в конец списка
    logging.info("Извлечение элементов из кучи:")
    for i in range(n - 1, 0, -1):
        iterations_counter[0] += 1
        logging.info(f"Извлечение: перемещаем корень {nums[0]} в конец на позицию {i}")
        nums[i], nums[0] = nums[0], nums[i]
        logging.info(f"После обмена: {nums}")
        heapify(nums, i, 0, iterations_counter)

    logging.info(f"Конец пирамидальной сортировки: {nums}")
    logging.info(f"Всего итераций: {iterations_counter[0]}")
    return iterations_counter[0]


# Проверяем, что оно работает
random_list_of_nums = [35, 12, 43, 8, 51]
iterations = heap_sort(random_list_of_nums)
print(f"Пирамидальная сортировка: {random_list_of_nums}")
print(f"Итераций: {iterations}")


# Сортировка слиянием (исправленная версия)
def merge(left_list, right_list, merge_iterations):
    logging.info(f"Начало слияния: left={left_list}, right={right_list}")
    sorted_list = []
    left_list_index = right_list_index = 0

    left_list_length, right_list_length = len(left_list), len(right_list)

    for _ in range(left_list_length + right_list_length):
        merge_iterations[0] += 1
        current_iter = merge_iterations[0]

        logging.info(f"Слияние итерация {current_iter}: left_index={left_list_index}, right_index={right_list_index}")
        logging.info(f"Текущий отсортированный список: {sorted_list}")

        if left_list_index < left_list_length and right_list_index < right_list_length:
            if left_list[left_list_index] <= right_list[right_list_index]:
                sorted_list.append(left_list[left_list_index])
                logging.info(f"Добавлен элемент из левого списка: {left_list[left_list_index]}")
                left_list_index += 1
            else:
                sorted_list.append(right_list[right_list_index])
                logging.info(f"Добавлен элемент из правого списка: {right_list[right_list_index]}")
                right_list_index += 1
        elif left_list_index == left_list_length:
            sorted_list.append(right_list[right_list_index])
            logging.info(f"Конец левого списка, добавлен из правого: {right_list[right_list_index]}")
            right_list_index += 1
        elif right_list_index == right_list_length:
            sorted_list.append(left_list[left_list_index])
            logging.info(f"Конец правого списка, добавлен из левого: {left_list[left_list_index]}")
            left_list_index += 1

    logging.info(f"Конец слияния: {sorted_list}")
    return sorted_list


def merge_sort(nums, depth=0):
    depth_str = "  " * depth
    logging.info(f"{depth_str}Рекурсия глубины {depth}: сортируем {nums}")

    if len(nums) <= 1:
        logging.info(f"{depth_str}Базовый случай: {nums}")
        return nums

    mid = len(nums) // 2
    logging.info(f"{depth_str}Разделение: mid={mid}, left={nums[:mid]}, right={nums[mid:]}")

    left_list = merge_sort(nums[:mid], depth + 1)
    right_list = merge_sort(nums[mid:], depth + 1)

    merge_iterations = [0]
    result = merge(left_list, right_list, merge_iterations)
    logging.info(f"{depth_str}Объединение завершено: {result}, итераций слияния: {merge_iterations[0]}")

    return result


# Проверяем сортировку слиянием
random_list_of_nums = [120, 45, 68, 250, 176]
logging.info(f"=== НАЧАЛО СОРТИРОВКИ СЛИЯНИЕМ ===")
sorted_list = merge_sort(random_list_of_nums)
print(f"Сортировка слиянием: {sorted_list}")


# Быстрая сортировка
def partition(nums, low, high, partition_iterations):
    partition_iterations[0] += 1
    current_partition = partition_iterations[0]

    # Проверяем границы
    if low >= high or low < 0 or high >= len(nums):
        logging.info(f"Разделение {current_partition}: недопустимые границы low={low}, high={high}")
        return low

    pivo = nums[(low + high) // 2]
    logging.info(f"Разделение {current_partition}: low={low}, high={high}, pivot={pivo}, массив={nums[low:high + 1]}")

    i = low - 1
    j = high + 1
    iteration_count = 0

    while True:
        iteration_count += 1
        logging.info(f"Разделение {current_partition}, итерация {iteration_count}: i={i}, j={j}")

        i += 1
        while i < len(nums) and nums[i] < pivo:  # Добавляем проверку границ
            i += 1
            if i < len(nums):
                logging.info(f"Увеличиваем i до {i} (nums[i]={nums[i]})")
            else:
                logging.info(f"i достиг конца массива")

        j -= 1
        while j >= 0 and nums[j] > pivo:  # Добавляем проверку границ
            j -= 1
            if j >= 0:
                logging.info(f"Уменьшаем j до {j} (nums[j]={nums[j]})")
            else:
                logging.info(f"j достиг начала массива")

        logging.info(f"После поиска: i={i}, j={j}")

        if i >= j:
            logging.info(f"Разделение {current_partition} завершено: split_index={j}")
            return j

        # Проверяем, что индексы в пределах массива перед обменом
        if 0 <= i < len(nums) and 0 <= j < len(nums):
            logging.info(f"Обмен: nums[{i}]={nums[i]} <-> nums[{j}]={nums[j]}")
            nums[i], nums[j] = nums[j], nums[i]
            logging.info(f"После обмена: {nums[low:high + 1]}")
        else:
            logging.info(f"Пропуск обмена: индексы i={i}, j={j} вне границ массива")
            break


def quick_sort(nums):
    quick_iterations = [0]
    sort_iterations = [0]

    def _quick_sort(items, low, high, depth=0):
        sort_iterations[0] += 1
        current_sort = sort_iterations[0]
        depth_str = "  " * depth

        logging.info(
            f"{depth_str}Быстрая сортировка вызов {current_sort}: low={low}, high={high}, подмассив={items[low:high + 1] if low <= high else 'пустой'}")

        if low < high and 0 <= low < len(items) and 0 <= high < len(items):
            split_index = partition(items, low, high, quick_iterations)
            logging.info(f"{depth_str}Разделение завершено: split_index={split_index}")

            _quick_sort(items, low, split_index, depth + 1)
            _quick_sort(items, split_index + 1, high, depth + 1)
        else:
            logging.info(f"{depth_str}Базовый случай: low={low}, high={high}")

    logging.info(f"начало быстрой сортировки")
    logging.info(f"Исходный массив: {nums}")
    _quick_sort(nums, 0, len(nums) - 1)
    logging.info(f"Быстрая сортировка завершена: {nums}")
    logging.info(f"Всего вызовов partition: {quick_iterations[0]}, всего рекурсивных вызовов: {sort_iterations[0]}")

    return quick_iterations[0], sort_iterations[0]


random_list_of_nums = [22, 5, 1, 18, 99]
partition_count, sort_count = quick_sort(random_list_of_nums)
print(f"Быстрая сортировка: {random_list_of_nums}")
print(f"Вызовов partition: {partition_count}, рекурсивных вызовов: {sort_count}")

logging.info("Конец программы")
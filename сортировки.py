import logging
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

# пузырьковая сортировка
def puzyr(nums):
    flag = True
    while flag:
        flag = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                flag = True
random_nums = [15, 2, 135, 789, 3]
puzyr(random_nums)
print(random_nums)

# Сортировка выборкой
def vyborka(nums):
    for i in range(len(nums)):
        indexminznach = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[indexminznach]:
                indexminznach = j
        nums[i], nums[indexminznach] = nums[indexminznach], nums[i]

random_nums = [1, 8000, 37, 52, 11]
vyborka(random_nums)
print(random_nums)

# сортировка вставками
def vstavki(nums):
    for i in range(1, len(nums)):
        dlyavstavki = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > dlyavstavki:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = dlyavstavki

random_list_of_nums = [91, 1, 15, 28, 6]
vstavki(random_list_of_nums)
print(random_list_of_nums)

# Пирамидальная сортировка
def heapify(nums, heap_size, root_index):
    largest = root_index
    logging.info(f"largest = {largest} value = {nums}")
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2

    logging.info(f"left_child = {left_child} element = {nums}")
    logging.info(f"right_child = {right_child}")

    # Если левый потомок корня — допустимый индекс, а элемент больше,
    # чем текущий наибольший, обновляем наибольший элемент
    if left_child < heap_size and nums[left_child] > nums[largest]:
        largest = left_child

    # То же самое для правого потомка корня
    if right_child < heap_size and nums[right_child] > nums[largest]:
        largest = right_child

    # Если наибольший элемент больше не корневой, они меняются местами
    if largest != root_index:
        nums[root_index], nums[largest] = nums[largest], nums[root_index]
        # Heapify the new root element to ensure it's the largest
        heapify(nums, heap_size, largest)

def heap_sort(nums):
    n = len(nums)

    # Создаём Max Heap из списка
    # Второй аргумент означает остановку алгоритма перед элементом -1, т.е.
    # перед первым элементом списка
    # 3-й аргумент означает повторный проход по списку в обратном направлении,
    # уменьшая счётчик i на 1
    for i in range(n, -1, -1):
        heapify(nums, n, i)

    # Перемещаем корень Max Heap в конец списка
    for i in range(n - 1, 0, -1):
        nums[i], nums[0] = nums[0], nums[i]
        heapify(nums, i, 0)

# Проверяем, что оно работает
random_list_of_nums = [35, 12, 43, 8, 51]
heap_sort(random_list_of_nums)
print(random_list_of_nums)
logging.info("konec programmy")

# слияние
def merge(left_list, right_list):
    sorted_list = []
    left_list_index = right_list_index = 0

    # Длина списков часто используется, поэтому создадим переменные для удобства
    left_list_length, right_list_length = len(left_list), len(right_list)

    for _ in range(left_list_length + right_list_length):
        if left_list_index < left_list_length and right_list_index < right_list_length:
            # Сравниваем первые элементы в начале каждого списка
            # Если первый элемент левого подсписка меньше, добавляем его
            # в отсортированный массив
            if left_list[left_list_index] <= right_list[right_list_index]:
                sorted_list.append(left_list[left_list_index])
                left_list_index += 1
            # Если первый элемент правого подсписка меньше, добавляем его
            # в отсортированный массив
            else:
                sorted_list.append(right_list[right_list_index])
                right_list_index += 1

        # Если достигнут конец левого списка, элементы правого списка
        # добавляем в конец результирующего списка
        elif left_list_index == left_list_length:
            sorted_list.append(right_list[right_list_index])
            right_list_index += 1
        # Если достигнут конец правого списка, элементы левого списка
        # добавляем в отсортированный массив
        elif right_list_index == right_list_length:
            sorted_list.append(left_list[left_list_index])
            left_list_index += 1

    return sorted_list

def merge_sort(nums):
    # Возвращаем список, если он состоит из одного элемента
    if len(nums) <= 1:
        return nums

    # Для того чтобы найти середину списка, используем деление без остатка
    # Индексы должны быть integer
    mid = len(nums) // 2

    # Сортируем и объединяем подсписки
    left_list = merge_sort(nums[:mid])
    right_list = merge_sort(nums[mid:])

    # Объединяем отсортированные списки в результирующий
    return merge(left_list, right_list)

# Проверяем, что оно работает
random_list_of_nums = [120, 45, 68, 250, 176]
random_list_of_nums = merge_sort(random_list_of_nums)
print(random_list_of_nums)

# быстрая разделяй и властвуй
def partition(nums, low, high):
    pivo = nums[(low + high) // 2]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while nums[i] < pivo:
            i += 1
        j -= 1
        while nums[j] > pivo:
            j -= 1

        if i >= j:
            return j
        nums[i], nums[j] = nums[j], nums[i]

def quick_sort(nums):
    def _quick_sort(items, low, high):
        if low < high:
            # This is the index after the pivot, where our lists are split
            split_index = partition(items, low, high)
            _quick_sort(items, low, split_index)
            _quick_sort(items, split_index + 1, high)

    _quick_sort(nums, 0, len(nums) - 1)
random_list_of_nums = [22, 5, 1, 18, 99]
quick_sort(random_list_of_nums)
print(random_list_of_nums)

# встроенные
l = [2, 1, 1, 3, 1, 2, 2]
l.sort()
print(l)

l2 = [2, 1, 1, 3, 1, 2, 2]
sorted_l2 = sorted(l2)
print(sorted_l2)
print(l2)

# встроенные в обратном порядке
l3 = [1, 2, 4, 3]
l3.sort(reverse=True)
print(l3)

l4 = [1, 3, 2, 2, 2, 1, 1, 1]
l5 = sorted(l4, reverse=True)
print(l5)
print(l4)

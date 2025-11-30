# Сортировка пузырьком
def puzyr(nums):
    nums = nums.copy()
    flag = True
    iterations = 0
    outer_iterations = 0

    while flag:
        outer_iterations += 1
        flag = False
        for i in range(len(nums) - 1):
            iterations += 1
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                flag = True

    return iterations, outer_iterations, nums


# Сортировка выборкой
def vyborka(nums):
    nums = nums.copy()
    iterations = 0

    for i in range(len(nums)):
        iterations += 1
        indexminznach = i
        for j in range(i + 1, len(nums)):
            iterations += 1
            if nums[j] < nums[indexminznach]:
                indexminznach = j
        if indexminznach != i:
            nums[i], nums[indexminznach] = nums[indexminznach], nums[i]

    return iterations, nums


# Сортировка вставками
def vstavki(nums):
    nums = nums.copy()
    iterations = 0

    for i in range(1, len(nums)):
        iterations += 1
        dlyavstavki = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > dlyavstavki:
            iterations += 1
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = dlyavstavki

    return iterations, nums


# Пирамидальная сортировка
def heap_sort(nums):
    nums = nums.copy()

    def heapify(nums, heap_size, root_index, iterations_counter):
        iterations_counter[0] += 1
        largest = root_index
        left_child = (2 * root_index) + 1
        right_child = (2 * root_index) + 2

        if left_child < heap_size and nums[left_child] > nums[largest]:
            largest = left_child
        if right_child < heap_size and nums[right_child] > nums[largest]:
            largest = right_child
        if largest != root_index:
            nums[root_index], nums[largest] = nums[largest], nums[root_index]
            heapify(nums, heap_size, largest, iterations_counter)

    n = len(nums)
    iterations_counter = [0]

    for i in range(n, -1, -1):
        if i < n:
            iterations_counter[0] += 1
            heapify(nums, n, i, iterations_counter)

    for i in range(n - 1, 0, -1):
        iterations_counter[0] += 1
        nums[i], nums[0] = nums[0], nums[i]
        heapify(nums, i, 0, iterations_counter)

    return iterations_counter[0], nums


# Сортировка слиянием
def merge_sort(nums):
    nums = nums.copy()

    def merge(left_list, right_list, merge_iterations):
        sorted_list = []
        left_list_index = right_list_index = 0
        left_list_length, right_list_length = len(left_list), len(right_list)

        for _ in range(left_list_length + right_list_length):
            merge_iterations[0] += 1
            if left_list_index < left_list_length and right_list_index < right_list_length:
                if left_list[left_list_index] <= right_list[right_list_index]:
                    sorted_list.append(left_list[left_list_index])
                    left_list_index += 1
                else:
                    sorted_list.append(right_list[right_list_index])
                    right_list_index += 1
            elif left_list_index == left_list_length:
                sorted_list.append(right_list[right_list_index])
                right_list_index += 1
            elif right_list_index == right_list_length:
                sorted_list.append(left_list[left_list_index])
                left_list_index += 1
        return sorted_list

    def _merge_sort(nums, merge_iterations):
        if len(nums) <= 1:
            return nums
        mid = len(nums) // 2
        left_list = _merge_sort(nums[:mid], merge_iterations)
        right_list = _merge_sort(nums[mid:], merge_iterations)
        return merge(left_list, right_list, merge_iterations)

    merge_iterations = [0]
    result = _merge_sort(nums, merge_iterations)
    return merge_iterations[0], result


# Быстрая сортировка
def quick_sort(nums):
    nums = nums.copy()

    def partition(nums, low, high, partition_iterations):
        partition_iterations[0] += 1
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

    quick_iterations = [0]
    sort_iterations = [0]

    def _quick_sort(items, low, high):
        sort_iterations[0] += 1
        if low < high:
            split_index = partition(items, low, high, quick_iterations)
            _quick_sort(items, low, split_index)
            _quick_sort(items, split_index + 1, high)

    _quick_sort(nums, 0, len(nums) - 1)
    return quick_iterations[0], sort_iterations[0], nums


# Тесты
import pytest


def test_puzyr():
    iterations, outer_iterations, result = puzyr([3, 1, 4, 2])
    assert result == [1, 2, 3, 4]
    assert iterations > 0


def test_vyborka():
    iterations, result = vyborka([3, 1, 4, 2])
    assert result == [1, 2, 3, 4]
    assert iterations > 0


def test_vstavki():
    iterations, result = vstavki([3, 1, 4, 2])
    assert result == [1, 2, 3, 4]
    assert iterations > 0


def test_heap_sort():
    iterations, result = heap_sort([3, 1, 4, 2])
    assert result == [1, 2, 3, 4]
    assert iterations > 0


def test_merge_sort():
    iterations, result = merge_sort([3, 1, 4, 2])
    assert result == [1, 2, 3, 4]
    assert iterations > 0


def test_quick_sort():
    iterations1, iterations2, result = quick_sort([3, 1, 4, 2])
    assert result == [1, 2, 3, 4]
    assert iterations1 > 0


def test_all_sorts_same_result():
    test_list = [5, 2, 8, 1, 9]
    expected = sorted(test_list)

    _, _, r1 = puzyr(test_list)
    _, r2 = vyborka(test_list)
    _, r3 = vstavki(test_list)
    _, r4 = heap_sort(test_list)
    _, r5 = merge_sort(test_list)
    _, _, r6 = quick_sort(test_list)

    assert r1 == expected
    assert r2 == expected
    assert r3 == expected
    assert r4 == expected
    assert r5 == expected
    assert r6 == expected


@pytest.mark.parametrize("input_list", [
    [],
    [1],
    [2, 1],
    [3, 1, 2],
    [5, 3, 8, 1, 2]
])
def test_parameterized(input_list):
    expected = sorted(input_list)

    _, _, r1 = puzyr(input_list)
    _, r2 = vyborka(input_list)
    _, r3 = vstavki(input_list)
    _, r4 = heap_sort(input_list)
    _, r5 = merge_sort(input_list)
    _, _, r6 = quick_sort(input_list)

    assert r1 == expected
    assert r2 == expected
    assert r3 == expected
    assert r4 == expected
    assert r5 == expected
    assert r6 == expected


if __name__ == "__main__":
    # Демонстрация работы
    test_nums = [3, 1, 4, 1, 5, 9, 2]
    print(f"Исходный список: {test_nums}")

    _, _, result1 = puzyr(test_nums)
    print(f"Пузырьковая: {result1}")

    _, result2 = vyborka(test_nums)
    print(f"Выборкой: {result2}")

    _, result3 = vstavki(test_nums)
    print(f"Вставками: {result3}")

    _, result4 = heap_sort(test_nums)
    print(f"Пирамидальная: {result4}")

    _, result5 = merge_sort(test_nums)
    print(f"Слиянием: {result5}")

    _, _, result6 = quick_sort(test_nums)
    print(f"Быстрая: {result6}")

    # Запуск тестов
    pytest.main([__file__, "-v"])
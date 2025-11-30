import pytest

# Функции
def sum2(x, y):
    return x + y

def bubble_sort(arr):
    arr = arr.copy()
    for i in range(len(arr)):
        for j in range(len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def is_even(n):
    return n % 2 == 0

def find_max(arr):
    return max(arr) if arr else None

def factorial(n):
    if n < 0:
        raise ValueError("Отрицательное число")
    return 1 if n == 0 else n * factorial(n-1)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Тесты
def test_sum():
    assert sum2(2, 3) == 5
    assert sum2(-1, 1) == 0

def test_bubble_sort():
    assert bubble_sort([3,1,4,2]) == [1,2,3,4]
    assert bubble_sort([]) == []

def test_quick_sort():
    assert quick_sort([3,1,4,2]) == [1,2,3,4]
    assert quick_sort([]) == []

def test_is_even():
    assert is_even(4) == True
    assert is_even(5) == False

def test_find_max():
    assert find_max([1,5,3]) == 5
    assert find_max([]) == None

def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1

def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)

def test_both_sorts_same():
    arr = [3,1,4,1,5,9,2]
    assert bubble_sort(arr) == quick_sort(arr)

@pytest.mark.parametrize("input,expected", [
    ([1,2], 3),
    ([0,0], 0),
    ([-1,1], 0)
])
def test_sum_parametrized(input, expected):
    assert sum2(input[0], input[1]) == expected

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
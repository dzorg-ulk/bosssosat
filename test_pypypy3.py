import pytest
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
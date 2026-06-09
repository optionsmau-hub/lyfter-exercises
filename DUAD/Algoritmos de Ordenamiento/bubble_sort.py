def bubble_sort(lst):
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

# Test
numbers = [9, 8, 7, 6, 5, 4, 3, 2, 1]
print(bubble_sort(numbers))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
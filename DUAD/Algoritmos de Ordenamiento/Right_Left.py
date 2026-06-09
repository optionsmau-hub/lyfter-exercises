def bubble_sort_right_to_left(lst):
    n = len(lst)
    for i in range(n):
        for j in range(n - 1, i, -1):  # Traverse from right to left
            if lst[j] < lst[j - 1]:    # Swap if smaller element is on the right
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
    return lst

# Test
numbers = [9, 8, 7, 6, 5, 4, 3, 2, 1]
print(bubble_sort_right_to_left(numbers))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
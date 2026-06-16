# 1. Bubble Sort - O(n²)
def bubble_sort(lst):
    n = len(lst)                          # O(1)
    for i in range(n):                    # O(n)
        for j in range(0, n - i - 1):    # O(n) → O(n²) con el de arriba
            if lst[j] > lst[j + 1]:      # O(1)
                lst[j], lst[j + 1] = lst[j + 1], lst[j]  # O(1)
# Total: O(n²)
print("=== bubble_sort ===")
print(bubble_sort([5, 3, 1, 4, 2]))
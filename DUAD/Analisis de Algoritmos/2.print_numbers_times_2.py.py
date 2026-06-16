# 2. print_numbers_times_2 - O(n)
def print_numbers_times_2(numbers_list):
    for number in numbers_list:  # O(n)
        print(number * 2)        # O(1)
# Total: O(n)
print("=== print_numbers_times_2 ===")
print_numbers_times_2([1, 2, 3, 4, 5])
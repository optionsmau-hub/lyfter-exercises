# 4. print_10_or_less_elements - O(1)
def print_10_or_less_elements(list_to_print):
    list_len = len(list_to_print)           # O(1)
    for index in range(min(list_len, 10)):  # O(1) - siempre máximo 10 veces
        print(list_to_print[index])         # O(1)
# Total: O(1)
print("=== print_10_or_less_elements ===")
print_10_or_less_elements([10, 20, 30, 40, 50])
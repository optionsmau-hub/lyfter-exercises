# 3. check_if_lists_have_an_equal - O(n²)
def check_if_lists_have_an_equal(list_a, list_b):
    for element_a in list_a:            # O(n)
        for element_b in list_b:        # O(n) → O(n²) con el de arriba
            if element_a == element_b:  # O(1)
                return True             # O(1)
    return False                        # O(1)
# Total: O(n²)
print("=== check_if_lists_have_an_equal ===")
print(check_if_lists_have_an_equal([1, 2, 3], [4, 5, 1]))
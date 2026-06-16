# 5. generate_list_trios - O(n³)
def generate_list_trios(list_a, list_b, list_c):
    result_list = []                    # O(1)
    for element_a in list_a:           # O(n)
        for element_b in list_b:       # O(n) → O(n²) con el de arriba
            for element_c in list_c:   # O(n) → O(n³) con los de arriba
                result_list.append(f'{element_a} {element_b} {element_c}')  # O(1)
    return result_list                 # O(1)
# Total: O(n³)
print("=== generate_list_trios ===")
print(generate_list_trios(["a", "b"], ["1", "2"], ["x", "y"]))
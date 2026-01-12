#Ejercicio de Funciones Numero 3 
def sum_list(numbers):
    """Return the sum of all elements in the given list."""
    total = 0
    for n in numbers:
        total += n
    return total


# quick test
data = [4, 6, 2, 29]
print(sum_list(data))   # → 41
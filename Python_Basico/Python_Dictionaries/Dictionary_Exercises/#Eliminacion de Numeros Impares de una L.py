#Eliminacion de Numeros Impares de una Lista
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

even_numbers = []

for num in my_list:
    if num % 2 == 0:   # número par
        even_numbers.append(num)

print(even_numbers)
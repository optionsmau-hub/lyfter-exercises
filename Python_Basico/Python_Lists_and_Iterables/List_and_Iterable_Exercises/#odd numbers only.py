#odd numbers only
my_list = [10, 15, 20, 25, 30, 35]

odd_numbers = []

for n in my_list:
    if n % 2 != 0:   # condición para números impares
        odd_numbers.append(n)

print(odd_numbers)
# This script filters out odd numbers from a given list and prints them.
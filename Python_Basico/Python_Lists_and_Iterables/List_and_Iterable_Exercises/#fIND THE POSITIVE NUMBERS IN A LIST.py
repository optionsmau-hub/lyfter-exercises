#fIND THE POSITIVE NUMBERS IN A LIST
MY_list = [-10, 15, -30, 25, 40, -5, 0, 12]
all_positive_numbers = True

for num in MY_list:
    if num <= 0:
        all_positive_numbers = False
        break

if all_positive_numbers:
    print("All numbers are positive")
else:
    print("There is at least one negative number in the list")
#Ejercicio de Funciones Numero 3
#Ejercicio extra de excepciones 3.py
def sum_variables(items):
    total = 0

    for element in items:
        try:
            value = float(element)
            total += value
            print(value, "correctly added")
        except ValueError:
            print("invalid element:", element)

    print("Total sum:", total)


# Ejemplo de uso
my_list = ['10', 'apple', '5.5', '3', 'n/a']
sum_variables(items=my_list) 
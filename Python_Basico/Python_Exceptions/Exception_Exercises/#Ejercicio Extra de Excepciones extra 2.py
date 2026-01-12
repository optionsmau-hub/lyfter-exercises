#Ejercicio Extra de Excepciones 2.py
def convert_to_integer(lst):
    print("Result:")

    for element in lst:
        try:
            number = int(element)
            print(element, "converted to", number)
        except ValueError:
            print("Could not convert the element:", element)


# Example usage
my_list = ['4', 'hello', '10', '5.2']
convert_to_integer(my_list)
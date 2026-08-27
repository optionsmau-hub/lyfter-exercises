#Ejercicio Extra de Funciones 1
def count_character(text, character):
    counter = 0
    for letter in text:
        if letter == character:
            counter += 1
    return counter


text = input("Enter text: ")
character = input("Enter the character to find: ")

result = count_character(text, character)

print(f"The character was found {result} times")
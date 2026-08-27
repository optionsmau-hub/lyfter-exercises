#Ejercicio #4 Funciones Programa que regrese texto al revés
def reverse_string(text):
    reversed_text = ""   # start with an empty string

    for char in text:    # go through each character
        reversed_text = char + reversed_text  # put each char at the beginning

    return reversed_text


stoic_phrase = "The obstacle is the way"   # << Stoic phrase
print(reverse_string(stoic_phrase))  # → "yaw eht si elcatsbo ehT"
#Ejercicio 6 Funciones Strings Separados por Guion
def sort_hyphen_words(text: str) -> str:
    """
    Accepts a hyphen-separated string, sorts the words alphabetically,
    and returns them joined by hyphens again.
    """
    words = text.split('-')      # convert to list
    words.sort()                 # sort alphabetically
    return '-'.join(words)       # back to string


# ----- examples -----
print(sort_hyphen_words("python-variable-funcion-computadora-monitor"))
# → computadora-funcion-monitor-python-variable

print(sort_hyphen_words("banana-apple-cherry-date"))
# → apple-banana-cherry-date

print(sort_hyphen_words("zoo-elephant-tiger-anteater"))
# → anteater-elephant-tiger-zoo

print(sort_hyphen_words("red-blue-green-yellow"))
# → blue-green-red-yellow

print(sort_hyphen_words("solo"))
# → solo
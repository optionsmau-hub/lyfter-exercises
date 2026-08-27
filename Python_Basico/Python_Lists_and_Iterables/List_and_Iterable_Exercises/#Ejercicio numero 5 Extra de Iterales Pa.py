#Ejercicio numero 5 Extra de Iterales  Palabras mayores a 4 letras
# ask the user for 5 words
words = []
for i in range(5):
    w = input(f"Enter word {i + 1}: ").strip()
    words.append(w)

# keep only those longer than 4 characters
long_words = [w for w in words if len(w) > 4]

# display the filtered list
print("Words with more than 4 letters:", long_words)
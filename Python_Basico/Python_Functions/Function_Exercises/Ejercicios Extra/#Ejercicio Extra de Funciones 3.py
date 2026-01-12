#Ejercicio Extra de Funciones 3 
def filter_words_by_length(words, n):
    result = []

    for word in words:
        if len(word) > n:
            result.append(word)

    return result


# User input
words = ["Soup", "day", "extraordinary", "happy", "incredible", "fun", "joyful"]
n = int(input("Enter the minimum number of letters: "))

filtered_words = filter_words_by_length(words, n)

print(filtered_words)
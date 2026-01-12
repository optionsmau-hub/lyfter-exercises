#Ejercicio Extra de Funciones 2
def filter_words_by_length(words, n):
    result = []

    for word in words:
        if len(word) > n:
            result.append(word)

    return result


# Input word list and minimum length
words = ["Sky", "Sun", "Amazing", "Daylight", "Joy", "Wonderful", "Peace"]
n = int(input("Enter the minimum number of letters: "))

# Function 
filtered_words = filter_words_by_length(words, n)

#  the result
print(filtered_words)
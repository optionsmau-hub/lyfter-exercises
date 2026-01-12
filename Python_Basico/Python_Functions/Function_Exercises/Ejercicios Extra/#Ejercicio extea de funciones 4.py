#Ejercicio extea de funciones 4
def count_vocals(texto):
    vocals = "aeiouAEIOU"
    count = 0

    for letra in texto:
        if letra in vocals:
            count += 1

    return count


# example usage
print(count_vocals(" Lets go Arsenal"))  # result: 5
print(count_vocals("Hello World"))      # result: 3 
print(count_vocals("Python Programming"))  # result: 4
print(count_vocals("Data Science"))     # result: 5
print(count_vocals("OpenAI ChatGPT"))   # result: 5
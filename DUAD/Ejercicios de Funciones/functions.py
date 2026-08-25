# Function Exercises (Python Basics) - Exercises 3 to 7


# Exercise 3: sum of all numbers in a list
def sum_list(numbers):
    total = 0
    for number in numbers:
        total += number
    return total


# Exercise 4: reverse a string
def reverse_string(text):
    return text[::-1]


# Exercise 5: count uppercase and lowercase letters in a string
def count_upper_lower(text):
    upper_count = 0
    lower_count = 0
    for char in text:
        if char.isupper():
            upper_count += 1
        elif char.islower():
            lower_count += 1
    return f"There's {upper_count} upper cases and {lower_count} lower cases"


# Exercise 6: sort hyphen-separated words alphabetically
def sort_hyphenated_words(text):
    words = text.split("-")
    words.sort()
    return "-".join(words)


# Exercise 7: filter prime numbers out of a list
def is_prime(number):
    if number < 2:
        return False
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False
    return True


def filter_primes(numbers):
    primes = []
    for number in numbers:
        if is_prime(number):
            primes.append(number)
    return primes


if __name__ == "__main__":
    print(sum_list([4, 6, 2, 29]))  # 41
    print(reverse_string("Hello world"))  # dlrow olleH
    print(count_upper_lower("I love Nación Sushi"))  # There's 3 upper cases and 13 lower cases
    print(sort_hyphenated_words("python-variable-function-computer-monitor"))  # computer-function-monitor-python-variable
    print(filter_primes([1, 4, 6, 7, 13, 9, 67]))  # [7, 13, 67]

# Exercise 1: numeric functions (sum, average, Celsius to Fahrenheit)
 

def sum_numbers(numbers):
    total = 0
    for number in numbers:
        total += number
    return total
 

def average(numbers):
    if len(numbers) == 0:
        raise ValueError("Cannot calculate the average of an empty list")
    return sum_numbers(numbers) / len(numbers)
 
 
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32
 
 
if __name__ == "__main__":
    print(sum_numbers([1, 2, 3]))  # 6
    print(sum_numbers([-1, -2, -3]))  # -6
    print(sum_numbers([0, 0, 0]))  # 0
 
    print(average([2, 4, 6]))  # 4.0
    print(average([-2, -4, -6]))  # -4.0
    print(average([0, 0, 0]))  # 0.0
 
    print(celsius_to_fahrenheit(100))  # 212.0
    print(celsius_to_fahrenheit(-40))  # -40.0
    print(celsius_to_fahrenheit(0))  # 32.0
 

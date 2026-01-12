#lIST 10 NUMBERS AND SAY THE HIGHST
numbers = []

print("Enter 10 numbers:")

for i in range(10):
    num = int(input("Number " + str(i + 1) + ": "))
    numbers.append(num)

# Find the highest number manually
highest = numbers[0]

for n in numbers:
    if n > highest:
        highest = n

print("Numbers entered:", numbers)
print("The highest number was:", highest)
# End of the program

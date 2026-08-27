# sample list
numbers = [12, 5, 8, -3, 9, 0, 4]

# assume the first element is the smallest for now
smallest = numbers[0]

# walk through the rest of the list
for value in numbers[1:]:
    if value < smallest:  # compare current value with smallest found so far
        smallest = value   # update when we find something smaller

print("Smallest value:", smallest)
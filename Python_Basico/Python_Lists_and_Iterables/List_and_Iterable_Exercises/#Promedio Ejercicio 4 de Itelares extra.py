#Promedio Ejercicio 4 de Itelares extra
# read space-separated numbers from the user
nums = list(map(float, input("Enter numbers separated by spaces: ").split()))

# compute the average
average = sum(nums) / len(nums)

# build a new list with values above the average
above_avg = [n for n in nums if n > average]

# display results
print("Average:", average)
print("Values above average:", above_avg)
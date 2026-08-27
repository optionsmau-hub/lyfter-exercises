#rEVERSE LIST ELEMENTS
my_list = [10, 20, 30, 40, 50, 60]

first = my_list[0]
last = my_list[-1]

my_list[0] = last
my_list[-1] = first

print(my_list)
#Diccionario de dos listas mismo tamano
list_a = ["first_name", "last_name", "role"]
list_b = ["Maurizio", "Strippoli", "Student"]

my_dict = {}

for i in range(len(list_a)):
    key = list_a[i]
    value = list_b[i]
    my_dict[key] = value

print(my_dict)
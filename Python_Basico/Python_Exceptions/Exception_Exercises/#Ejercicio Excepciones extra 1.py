#Ejercicio Excepciones extra 1 
name = input("Enter your name: ")

if name.isdigit():
    raise ValueError("The name cannot be a number.")

print("Valid Name:", name)

age = input("Enter your age: ")
if not age.isdigit():
    raise ValueError("The age must be a number.")
age = int(age)

print("hi", name, "you are", age, "years old.")
#Ejercicio 2 de Funciones. Practica 1 con Scope
def my_function():
    toy = "red car"   # variable local
    print("Inside the function:", toy)

my_function()

print(toy)  # ❌ Esto da error: toy solo vive dentro de la función

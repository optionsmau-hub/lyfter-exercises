#Ejercicio 1 Funciones. Crear una Funcion que llame a la otra Funcion
def calculate_total(price, tax):
    total = price + tax
    print("Total with tax:", total)
    show_thank_you()

def show_thank_you():
    print("Thank you for your purchase!")

calculate_total(50, 5)
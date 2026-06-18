#Exercise 2: divide function (given in the activity statement)
 
 
def divide(number1, number2):
    if number2 == 0:
        raise ValueError("No se puede dividir por cero")
    return number1 / number2
 

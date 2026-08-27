#Ejercicio de Funciones 2 b 
tickets = 2 

def get_more_tickets():
    global tickets   
    print("Inside the function, before adding:", tickets)
    
    tickets = tickets + 3  # 3 more tickets are added
    print("Inside the function, after adding:", tickets)

get_more_tickets()

print("Outside the function:", tickets)
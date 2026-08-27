#Asking for User Data
Name = input("Enter Name: ")
Lastname = (input("Enter Lastname: ")) 
Age = int(input("Enter Age: "))        
#Showing Classification Based on Age
if Age < 2:
    Clasificacion = "Baby"  
elif Age >= 2 and Age < 12:
    Clasificacion = "Kid"
elif Age >= 12 and Age < 15:  
    Clasificacion = "Pre-Teen"
elif Age >= 15 and Age < 18:  
    Clasificacion = "Teenager"       
elif Age >= 18 and Age < 26:  
    Clasificacion = "Young Adult"
elif Age >= 26 and Age < 60:  
    Clasificacion = "Adult"
else:  
    Clasificacion = "Senior"
print("Full Name: " + Name + " " + Lastname)
print("Age: " + str(Age) + " years old")   
print("Classify by Age: " + Clasificacion)

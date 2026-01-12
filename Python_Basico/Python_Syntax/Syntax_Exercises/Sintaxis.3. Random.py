import random

#Generate a random number between 1 and 10 
random_number = random.randint(1, 10)   
#Variable to keep track of the number of attempts
Attemps = 0

print("Welcome to the Random number Game!")
#While loop to allow multiple attempts
while Attemps < 10:
    Attemps = input("Guest the number between 1 and 10: ")
    
    #Validate input
    if not Attemps.isdigit():
        print("Please enter a valid number.")
        continue
    
    Attemps = int(Attemps)
    Attemps += 1
    
    if Attemps < random_number:
        print("Too Low try again.")
    elif Attemps > random_number:
        print("Too High Try again.")
    else:
        print(f"Congratulations! You've guessed the number {random_number} in {Attemps} attempts.")
        break
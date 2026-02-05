# Ask how many videogames the user wants to enter
n = int(input("How many videogames do you want to add? "))

# Open (or create) the CSV file
with open("videojuegos.csv", "w", encoding="utf-8") as file:
    # Write the header
    file.write("nombre,genero,desarrollador,clasificacion\n")

    # Loop to get videogame information
    for i in range(n):
        print(f"\nVideogame {i + 1}")

        name = input("Name: ")
        genre = input("Genre: ")
        developer = input("Developer: ")
        rating = input("ESRB Rating: ")

        # Write the data to the file
        file.write(f"{name},{genre},{developer},{rating}\n")

print("CSV file created successfully.")

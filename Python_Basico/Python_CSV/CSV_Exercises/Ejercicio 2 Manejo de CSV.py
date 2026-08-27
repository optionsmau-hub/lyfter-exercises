import csv

# Ask how many videogames the user wants to enter
n = int(input("How many videogames do you want to add? "))

# Open the file using tab as delimiter
with open("videojuegos_tab.tsv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter="\t")

    # Write header
    writer.writerow(["nombre", "genero", "desarrollador", "clasificacion"])

    # Get videogame data
    for i in range(n):
        print(f"\nVideogame {i + 1}")

        name = input("Name: ")
        genre = input("Genre: ")
        developer = input("Developer: ")
        rating = input("ESRB Rating: ")

        writer.writerow([name, genre, developer, rating])

print("Tab-separated file created successfully.")
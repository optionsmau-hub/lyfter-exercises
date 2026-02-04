#menu.py

def show_menu() -> None:
    """ Display the main menu options """
    print("=== Student Management System ===")
    print("1. Add Students")
    print("2. View Students")
    print("3. View Top 3 Students by Average Grade ")
    print("4.View Overall Class Average Grade")
    print("5.Export Students to CSV")
    print("6. import from CSV")
    print("7. Exit")

def get_menu_options() -> int:
    valid_options = {1, 2, 3, 4, 5, 6, 7}

    while True:
        choice = input("Select an Option (1-7): ").strip()

        if choice.isdigit() and int(choice) in valid_options:
            return int(choice)

        print("Invalid option. Please choose a number between 1 and 7.")
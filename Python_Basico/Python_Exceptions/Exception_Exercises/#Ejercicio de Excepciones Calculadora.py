def show_menu():
    print("\n1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Clear result")
    print("0. Exit")


def get_number():
    while True:
        new_number = input("Enter a number: ")
        try:
            return float(new_number)
        except ValueError:
            print("Error: Invalid number.")


def add(current, new):
    return current + new


def subtract(current, new):
    return current - new


def multiply(current, new):
    return current * new


def divide(current, new):
    if new == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return current / new


def main():
    current = 0.0

    while True:
        print("\nCurrent number:", current)
        show_menu()
        option = input("Choose an option: ")

        if option == "0":
            print("Goodbye!")
            break

        if option not in ["1", "2", "3", "4", "5"]:
            print("Error: Invalid option.")
            continue

        if option == "5":
            current = 0
            print("Result cleared.")
            continue

        new_number = get_number()

        try:
            if option == "1":
                current = add(current, new_number)
            elif option == "2":
                current = subtract(current, new_number)
            elif option == "3":
                current = multiply(current, new_number)
            elif option == "4":
                current = divide(current, new_number)
        except ZeroDivisionError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
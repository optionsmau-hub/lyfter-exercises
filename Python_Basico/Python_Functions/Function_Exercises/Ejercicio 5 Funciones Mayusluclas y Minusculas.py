#Ejercicio #5 de Funciones Programa que cuenta mayusculas y minusculas
def count_cases(s: str):
    """Print the number of uppercase and lowercase letters in the string."""
    upper = sum(1 for ch in s if ch.isupper())
    lower = sum(1 for ch in s if ch.islower())
    print(f"There are {upper} upper cases and {lower} lower cases")


# Example usage
count_cases("I love Basketball and the games of the NBA")

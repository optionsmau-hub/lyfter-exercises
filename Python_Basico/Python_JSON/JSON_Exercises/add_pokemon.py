import json


FILE_PATH = "pokemons.json"


def load_pokemons(path):
    """Reads the JSON file. If it does not exist or is corrupted, returns an empty list."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("⚠️ The file does not exist. Starting with an empty list.")
        return []
    except json.JSONDecodeError:
        print("⚠️ The file is empty or corrupted. Starting with an empty list.")
        return []


def ask_int(message):
    """Asks for an integer value and validates the input."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


def get_new_pokemon():
    """Asks the user for the new Pokémon data."""
    name = input("Enter Pokémon name (English): ")
    pokemon_type = input("Enter Pokémon type: ")

    hp = ask_int("Enter HP: ")
    attack = ask_int("Enter Attack: ")
    defense = ask_int("Enter Defense: ")
    sp_attack = ask_int("Enter Sp. Attack: ")
    sp_defense = ask_int("Enter Sp. Defense: ")
    speed = ask_int("Enter Speed: ")

    return {
        "name": {
            "english": name
        },
        "type": [
            pokemon_type
        ],
        "base": {
            "HP": hp,
            "Attack": attack,
            "Defense": defense,
            "Sp. Attack": sp_attack,
            "Sp. Defense": sp_defense,
            "Speed": speed
        }
    }


def save_pokemons(path, pokemons):
    """Saves the Pokémon list into the JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(pokemons, file, indent=2, ensure_ascii=False)


def main():
    pokemons = load_pokemons(FILE_PATH)
    new_pokemon = get_new_pokemon()
    pokemons.append(new_pokemon)
    save_pokemons(FILE_PATH, pokemons)
    print("✅ Pokémon added successfully.")


if __name__ == "__main__":
    main()

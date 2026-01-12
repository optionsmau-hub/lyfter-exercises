#Ejercicio extra 2 De manejo de Archivos
FILE_PATH = "text.md"


def count_words(path): 
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        words = content.split()  # splits by spaces and line breaks
        return len(words)


def main():
    total_words = count_words(FILE_PATH)
    print("This file contains")
    print(total_words)
    print("words")


if __name__ == "__main__":
    main()

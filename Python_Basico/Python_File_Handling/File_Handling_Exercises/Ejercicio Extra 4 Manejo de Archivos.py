FILE_PATH = "log.txt"


def append_text_to_file(path):
    text = input("Enter a line of text: ")

    with open(path, "a", encoding="utf-8") as file:
        file.write(text + "\n")

    print("The text was successfully added to the file.")


def main():
    append_text_to_file(FILE_PATH)


if __name__ == "__main__":
    main()

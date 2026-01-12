INPUT_FILE = "original.txt"
OUTPUT_FILE = "uppercase.txt"


def convert_to_uppercase(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:

        for line in infile:
            outfile.write(line.upper())


def main():
    convert_to_uppercase(INPUT_FILE, OUTPUT_FILE)
    print("File successfully converted to uppercase.")


if __name__ == "__main__":
    main()

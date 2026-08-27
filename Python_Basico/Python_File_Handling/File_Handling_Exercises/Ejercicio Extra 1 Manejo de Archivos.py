#Ejercicio Extra Manejo de Archivos
INPUT_FILE = "entrada.txt"
OUTPUT_FILE = "salida.txt"

def join_lines_into_one(input_path, output_path):
    # Read line by line, remove \n and extra spaces, then join with single spaces
    parts = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            clean = line.strip()  # removes \n and leading/trailing spaces
            if clean:  # skip empty lines
                parts.append(clean)

    one_line = " ".join(parts)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(one_line)

    print("✅ Done! Output saved to:", output_path)

if __name__ == "__main__":
    join_lines_into_one(INPUT_FILE, OUTPUT_FILE)

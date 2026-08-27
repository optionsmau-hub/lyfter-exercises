# ASK FOR 8 NUMBERS AND FIND HOW MANY TIMES A SPECIFIC NUMBER APPEARS
my_list = []

print("ENTER 8 NUMBERS:")

for i in range(8):
    num = int(input("NUMBER " + str(i + 1) + ": "))
    my_list.append(num)

# ASK FOR THE NUMBER TO LOOK FOR1
NUMBER_TOLOOKFOR = int(input("ENTER THE NUMBER TO LOOK UP: "))

# Contar cuántas veces aparece
COUNTING = 0

for n in my_list:
    if n == NUMBER_TOLOOKFOR:
        COUNTING += 1

# Mostrar resultado
print("THE NUMBER", NUMBER_TOLOOKFOR, "SHOWS", COUNTING, "TIMES IN THE LIST.")

#Programa para eliminar keys de un diccionario
list_of_keys = ["age", "role"]

user = {
    "first_name": "Maurizio",
    "last_name": "Strippoli",
    "email": "mauro@example.com",
    "age": 26,
    "role": "Student",
    "artist_name": "$mau"
}

for key in list_of_keys:
    if key in user:
        del user[key]

print(user)
#Ejercicio Extra 3 Tienda de Anime
# Calcula el total de ventas por categoría en una tienda de anime.
# Anime-store sales: (category, price)
sales = [
    ("Figures", 89.99),
    ("Manga", 12.50),
    ("Apparel", 35.00),
    ("Figures", 249.99),
    ("Accessories", 8.75),
    ("Manga", 9.99),
    ("Apparel", 22.50),
    ("Figures", 159.00),
    ("Accessories", 15.25),
    ("Manga", 11.25)
]

# dictionary to accumulate totals per category
totals = {}

for category, price in sales:
    if category not in totals:
        totals[category] = 0.0
    totals[category] += price

# show the totals
for cat, total in totals.items():
    print(f"{cat}: ${total:.2f}")
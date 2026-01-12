#Lista de Compras con email y usuario Electronicos
sales = [
    {
        "date": "2025-01-10",
        "customer_email": "mauro@example.com",
        "items": [
            {
                "name": "Laptop",
                "upc": "ITEM 43564567",
                "unit_price": 1200
            },
            {
                "name": "Mouse",
                "upc": "ITEM 87654321",
                "unit_price": 25
            }
        ]
    },
    {
        "date": "2025-01-11",
        "customer_email": "jane@example.com",
        "items": [
            {
                "name": "Headphones",
                "upc": "ITEM 12345678",
                "unit_price": 80
            },
            {
                "name": "Keyboard",
                "upc": "ITEM 23456789",
                "unit_price": 45
            }
        ]
    },
    {
        "date": "2025-01-12",
        "customer_email": "Chimuelo98@example.com",
        "items": [
            {
                "name": "Monitor",
                "upc": "ITEM 34567890",
                "unit_price": 300
            },
            {
                "name": "Webcam",
                "upc": "ITEM 45678901",
                "unit_price": 70
            }

        ]   
    },
    {
        "date": "2025-01-13",
        "customer_email": "Samuelitoelloquillo@example.com",
        "items": [
            {
                "name": "Tablet",
                "upc": "ITEM 56789012",
                "unit_price": 400
            },
            {
                "name": "Stylus Pen",
                "upc": "ITEM 67890123",
                "unit_price": 30
            }
        ]   
    }
]
result = {}

for sale in sales:
    for item in sale["items"]:
        upc = item["upc"]
        price = item["unit_price"]

        if upc not in result:
            result[upc] = 0

        result[upc] += price

print(result)

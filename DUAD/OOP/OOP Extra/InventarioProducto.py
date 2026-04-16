class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def show_products(self):
        for product in self.products:
            print(f"Name: {product.name}, Price: {product.price}, Quantity: {product.quantity}")

    def calculate_total_value(self):
        total = 0
        for product in self.products:
            total += product.price * product.quantity
        return total


# --- Example ---
product1 = Product("Mouse", 5000, 3)
product2 = Product("Keyboard", 8000, 2)

inventory = Inventory()
inventory.add_product(product1)
inventory.add_product(product2)

inventory.show_products()

print(inventory.calculate_total_value())  # 31000
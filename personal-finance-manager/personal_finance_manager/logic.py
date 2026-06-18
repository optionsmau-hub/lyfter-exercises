class Category:
    """Represents a spending or income category, like 'Food' or 'Transport'."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category('{self.name}')"


class Transaction:
    """Represents a single income or expense movement."""

    def __init__(self, title, amount, category_name, transaction_type):
        self.title = title
        self.amount = amount
        self.category_name = category_name
        self.transaction_type = transaction_type

    def get_signed_amount(self):
        """Returns the amount with the correct sign:
        positive for income, negative for expense."""
        if self.transaction_type == "expense":
            return -self.amount
        return self.amount

    def __str__(self):
        signed_amount = self.get_signed_amount()
        return f"{self.title} | {self.category_name} | ₡{signed_amount}"


if __name__ == "__main__":
    food = Category("Food")
    print(food)
    print(repr(food))

    salary = Transaction("Salary", 1000, "Work", "income")
    print(salary)
    print(salary.get_signed_amount())

    groceries = Transaction("Groceries", 50, "Food", "expense")
    print(groceries)
    print(groceries.get_signed_amount())
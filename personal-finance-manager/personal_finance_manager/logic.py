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


class FinanceManager:
    """Manages all categories and transactions, and the rules between them."""

    def __init__(self):
        self.categories = []
        self.transactions = []

    def category_exists(self, name):
        """Returns True if a category with this name already exists."""
        for category in self.categories:
            if category.name == name:
                return True
        return False

    def add_category(self, name):
        """Adds a new category, unless it already exists."""
        if self.category_exists(name):
            raise ValueError(f"Category '{name}' already exists.")
        new_category = Category(name)
        self.categories.append(new_category)
        return new_category

    def add_transaction(self, title, amount, category_name, transaction_type):
        """Adds a new transaction, validating that the category exists first."""
        if not self.categories:
            raise ValueError("Cannot add a transaction: no categories available.")
        if not self.category_exists(category_name):
            raise ValueError(f"Category '{category_name}' does not exist.")
        new_transaction = Transaction(title, amount, category_name, transaction_type)
        self.transactions.append(new_transaction)
        return new_transaction

    def get_total_income(self):
        """Sums up all income transactions."""
        total = 0
        for transaction in self.transactions:
            if transaction.transaction_type == "income":
                total += transaction.amount
        return total

    def get_total_expenses(self):
        """Sums up all expense transactions."""
        total = 0
        for transaction in self.transactions:
            if transaction.transaction_type == "expense":
                total += transaction.amount
        return total

    def get_balance(self):
        """Returns total income minus total expenses."""
        return self.get_total_income() - self.get_total_expenses()


if __name__ == "__main__":
    manager = FinanceManager()

    # Try adding a transaction with no categories yet (should fail)
    try:
        manager.add_transaction("Salary", 1000, "Work", "income")
    except ValueError as error:
        print(f"Error caught: {error}")

    # Now add some categories
    manager.add_category("Work")
    manager.add_category("Food")

    # Now add transactions (should work)
    manager.add_transaction("Salary", 1000, "Work", "income")
    manager.add_transaction("Groceries", 50, "Food", "expense")

    print(f"Total income: {manager.get_total_income()}")
    print(f"Total expenses: {manager.get_total_expenses()}")
    print(f"Balance: {manager.get_balance()}")
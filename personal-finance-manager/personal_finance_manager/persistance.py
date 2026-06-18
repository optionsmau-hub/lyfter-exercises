import json
import os
from logic import Category, Transaction

# File paths for storing data
CATEGORIES_FILE = "data/categories.json"
TRANSACTIONS_FILE = "data/transactions.json"


# --- Serialization (objects → JSON-friendly dicts) ---

def category_to_dict(category):
    """Converts a Category object to a plain dictionary."""
    return {"name": category.name}


def transaction_to_dict(transaction):
    """Converts a Transaction object to a plain dictionary."""
    return {
        "title": transaction.title,
        "amount": transaction.amount,
        "category_name": transaction.category_name,
        "transaction_type": transaction.transaction_type
    }


# --- Deserialization (JSON dicts → objects) ---

def dict_to_category(data):
    """Converts a plain dictionary back into a Category object."""
    return Category(data["name"])


def dict_to_transaction(data):
    """Converts a plain dictionary back into a Transaction object."""
    return Transaction(
        data["title"],
        data["amount"],
        data["category_name"],
        data["transaction_type"]
    )


# --- Save functions ---

def save_categories(categories):
    """Saves a list of Category objects to the JSON file."""
    data = [category_to_dict(category) for category in categories]
    with open(CATEGORIES_FILE, "w") as file:
        json.dump(data, file, indent=4)


def save_transactions(transactions):
    """Saves a list of Transaction objects to the JSON file."""
    data = [transaction_to_dict(transaction) for transaction in transactions]
    with open(TRANSACTIONS_FILE, "w") as file:
        json.dump(data, file, indent=4)


# --- Load functions ---

def load_categories():
    """Loads categories from the JSON file. Returns empty list if file doesn't exist."""
    if not os.path.exists(CATEGORIES_FILE):
        return []
    with open(CATEGORIES_FILE, "r") as file:
        data = json.load(file)
    return [dict_to_category(item) for item in data]


def load_transactions():
    """Loads transactions from the JSON file. Returns empty list if file doesn't exist."""
    if not os.path.exists(TRANSACTIONS_FILE):
        return []
    with open(TRANSACTIONS_FILE, "r") as file:
        data = json.load(file)
    return [dict_to_transaction(item) for item in data]


if __name__ == "__main__":
    from logic import FinanceManager

    manager = FinanceManager()
    manager.add_category("Work")
    manager.add_category("Food")
    manager.add_transaction("Salary", 1000, "Work", "income")
    manager.add_transaction("Groceries", 50, "Food", "expense")

    # Save everything
    save_categories(manager.categories)
    save_transactions(manager.transactions)
    print("Data saved!")

    # Load everything back
    loaded_categories = load_categories()
    loaded_transactions = load_transactions()
    print(f"Loaded {len(loaded_categories)} categories")
    print(f"Loaded {len(loaded_transactions)} transactions")
    for transaction in loaded_transactions:
        print(transaction)
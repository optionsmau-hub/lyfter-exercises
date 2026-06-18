import unittest
from logic import Category, Transaction, FinanceManager


class TestCategory(unittest.TestCase):

    def test_category_name_is_stored_correctly(self):
        """Category should store the name passed to it."""
        category = Category("Food")
        self.assertEqual(category.name, "Food")

    def test_category_str_returns_name(self):
        """str(category) should return the category name."""
        category = Category("Transport")
        self.assertEqual(str(category), "Transport")


class TestTransaction(unittest.TestCase):

    def test_income_signed_amount_is_positive(self):
        """Income transactions should return a positive signed amount."""
        transaction = Transaction("Salary", 1000, "Work", "income")
        self.assertEqual(transaction.get_signed_amount(), 1000)

    def test_expense_signed_amount_is_negative(self):
        """Expense transactions should return a negative signed amount."""
        transaction = Transaction("Groceries", 50, "Food", "expense")
        self.assertEqual(transaction.get_signed_amount(), -50)

    def test_amount_is_always_stored_positive(self):
        """The raw amount attribute should always be positive."""
        transaction = Transaction("Groceries", 50, "Food", "expense")
        self.assertEqual(transaction.amount, 50)


class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        """This runs before every test. Creates a fresh manager with categories."""
        self.manager = FinanceManager()
        self.manager.add_category("Work")
        self.manager.add_category("Food")

    def test_add_category_increases_list(self):
        """Adding a category should increase the categories list."""
        self.manager.add_category("Transport")
        self.assertEqual(len(self.manager.categories), 3)

    def test_duplicate_category_raises_error(self):
        """Adding a category with the same name should raise ValueError."""
        with self.assertRaises(ValueError):
            self.manager.add_category("Work")

    def test_add_transaction_with_no_categories_raises_error(self):
        """Adding a transaction when no categories exist should raise ValueError."""
        empty_manager = FinanceManager()
        with self.assertRaises(ValueError):
            empty_manager.add_transaction("Salary", 1000, "Work", "income")

    def test_get_total_income(self):
        """Total income should sum only income transactions."""
        self.manager.add_transaction("Salary", 1000, "Work", "income")
        self.manager.add_transaction("Bonus", 200, "Work", "income")
        self.manager.add_transaction("Groceries", 50, "Food", "expense")
        self.assertEqual(self.manager.get_total_income(), 1200)

    def test_get_total_expenses(self):
        """Total expenses should sum only expense transactions."""
        self.manager.add_transaction("Salary", 1000, "Work", "income")
        self.manager.add_transaction("Groceries", 50, "Food", "expense")
        self.manager.add_transaction("Lunch", 20, "Food", "expense")
        self.assertEqual(self.manager.get_total_expenses(), 70)

    def test_get_balance(self):
        """Balance should be total income minus total expenses."""
        self.manager.add_transaction("Salary", 1000, "Work", "income")
        self.manager.add_transaction("Groceries", 50, "Food", "expense")
        self.assertEqual(self.manager.get_balance(), 950)


if __name__ == "__main__":
    unittest.main()
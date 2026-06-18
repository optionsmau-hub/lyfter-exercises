import FreeSimpleGUI as sg
from logic import FinanceManager
from persistance import (
    save_categories, save_transactions,
    load_categories, load_transactions
)


def get_table_data(manager):
    """Converts transactions to a list of rows for the table."""
    rows = []
    for transaction in manager.transactions:
        rows.append([
            transaction.title,
            transaction.category_name,
            f"₡{transaction.get_signed_amount()}",
            transaction.transaction_type.capitalize()
        ])
    return rows


def open_add_category_window(manager):
    """Opens a popup window to add a new category."""
    layout = [
        [sg.Text("Category name:"), sg.Input(key="name")],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]
    window = sg.Window("Add Category", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Save":
            name = values["name"].strip()
            if not name:
                sg.popup_error("Category name cannot be empty.")
                continue
            try:
                manager.add_category(name)
                save_categories(manager.categories)
                sg.popup(f"Category '{name}' added successfully!")
                break
            except ValueError as error:
                sg.popup_error(str(error))

    window.close()


def open_add_transaction_window(manager, transaction_type):
    """Opens a popup window to add an income or expense."""
    if not manager.categories:
        sg.popup_error("No categories available. Please add a category first.")
        return

    category_names = [category.name for category in manager.categories]

    layout = [
        [sg.Text("Title:"), sg.Input(key="title")],
        [sg.Text("Amount:"), sg.Input(key="amount")],
        [sg.Text("Category:"), sg.Combo(category_names, key="category")],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    title = "Add Income" if transaction_type == "income" else "Add Expense"
    window = sg.Window(title, layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Save":
            title_value = values["title"].strip()
            amount_value = values["amount"].strip()
            category_value = values["category"]

            if not title_value or not amount_value or not category_value:
                sg.popup_error("All fields are required.")
                continue
            try:
                amount = float(amount_value)
                if amount <= 0:
                    sg.popup_error("Amount must be a positive number.")
                    continue
            except ValueError:
                sg.popup_error("Amount must be a valid number.")
                continue

            try:
                manager.add_transaction(title_value, amount, category_value, transaction_type)
                save_transactions(manager.transactions)
                sg.popup("Transaction added successfully!")
                break
            except ValueError as error:
                sg.popup_error(str(error))

    window.close()


def main():
    """Main window of the Personal Finance Manager."""
    manager = FinanceManager()
    manager.categories = load_categories()
    manager.transactions = load_transactions()

    headings = ["Title", "Category", "Amount", "Type"]
    table_data = get_table_data(manager)

    layout = [
        [sg.Text("Personal Finance Manager", font=("Helvetica", 16))],
        [sg.Table(
            values=table_data,
            headings=headings,
            key="table",
            auto_size_columns=True,
            expand_x=True,
            expand_y=True,
            enable_events=True
        )],
        [
            sg.Button("Add Category"),
            sg.Button("Add Income"),
            sg.Button("Add Expense")
        ]
    ]

    window = sg.Window(
        "Personal Finance Manager",
        layout,
        size=(700, 400),
        resizable=True
    )

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Add Category":
            open_add_category_window(manager)
            # Refresh the table after adding
            window["table"].update(values=get_table_data(manager))

        if event == "Add Income":
            open_add_transaction_window(manager, "income")
            window["table"].update(values=get_table_data(manager))

        if event == "Add Expense":
            open_add_transaction_window(manager, "expense")
            window["table"].update(values=get_table_data(manager))

    window.close()


if __name__ == "__main__":
    main()
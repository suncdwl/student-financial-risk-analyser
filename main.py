"""Student Finance Risk Analyser - command-line menu.

Run with:  python main.py
"""

import math
import os

from analyser import build_report
from storage import load_data, save_data

CURRENCY = "Rs."
# Build the path relative to this file, so it works from any folder.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "expenses.csv")


# ---------- Input helpers (keep asking until the input is valid) ----------

def read_amount(prompt):
    """Ask for a positive number. Repeats until the user types a valid one."""
    while True:
        text = input(prompt).strip()
        try:
            amount = float(text)
        except ValueError:
            print("Please enter a number, for example 2500 or 2500.50.")
            continue
        if not math.isfinite(amount) or amount <= 0:
            print("The amount must be greater than zero.")
            continue
        return amount


def read_category(prompt):
    """Ask for a non-empty category name, converted to lowercase."""
    while True:
        name = input(prompt).strip().lower()
        if name:
            return name
        print("Category name cannot be empty.")


# ---------- Menu actions ----------

def add_expense(expenses):
    """Add an expense. Same category entered twice is added together."""
    category = read_category("Category (e.g. food, rent, transport): ")
    amount = read_amount(f"Amount spent on {category} ({CURRENCY}): ")
    expenses[category] = expenses.get(category, 0) + amount
    print(f"Added {CURRENCY} {amount:.2f} to '{category}'.")


def show_report(income, expenses):
    """Print the analysis. Needs income to be set first."""
    if income <= 0:
        print("Please set your monthly income first (option 1).")
        return

    report = build_report(income, expenses)
    print("\n----- Monthly Report -----")
    print(f"Income:       {CURRENCY} {report['income']:.2f}")
    print(f"Total spent:  {CURRENCY} {report['total_spent']:.2f}")
    print(f"Savings:      {CURRENCY} {report['savings']:.2f}")
    print(f"Savings rate: {report['savings_rate']:.1f}%")
    print(f"Risk level:   {report['risk_level']}")
    if report["biggest_category"] is not None:
        print(
            f"Biggest expense: {report['biggest_category']} "
            f"({CURRENCY} {report['biggest_amount']:.2f}, "
            f"{report['biggest_share']:.0f}% of spending)"
        )
    print(f"Advice: {report['advice']}")
    print("--------------------------")


def save_to_file(income, expenses):
    try:
        save_data(DATA_FILE, income, expenses)
        print("Data saved.")
    except OSError as error:
        print(f"Could not save data: {error}")


def load_from_file():
    """Return (income, expenses) from the file, or None if loading failed."""
    try:
        income, expenses = load_data(DATA_FILE)
    except FileNotFoundError:
        print("No saved data found yet. Save something first (option 4).")
        return None
    except (ValueError, OSError) as error:
        print(f"Could not load data: {error}")
        return None
    print("Data loaded.")
    return income, expenses


def print_menu():
    print("\n1. Set monthly income")
    print("2. Add an expense")
    print("3. View report")
    print("4. Save data")
    print("5. Load data")
    print("6. Exit")


def main():
    income = 0.0
    expenses = {}

    print("=== Student Finance Risk Analyser ===")
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            income = read_amount(f"Monthly income ({CURRENCY}): ")
        elif choice == "2":
            add_expense(expenses)
        elif choice == "3":
            show_report(income, expenses)
        elif choice == "4":
            save_to_file(income, expenses)
        elif choice == "5":
            loaded = load_from_file()
            if loaded is not None:
                income, expenses = loaded
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped. Goodbye!")

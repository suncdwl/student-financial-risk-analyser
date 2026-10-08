"""Saving and loading data using Python's built-in csv module.

CSV file layout:
    type,name,amount
    income,monthly income,20000.0
    expense,food,6000.0
    expense,rent,9000.0
"""

import csv
import math
import os


def save_data(filepath, income, expenses):
    """Write income and expenses to a CSV file (creates the folder if needed)."""
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["type", "name", "amount"])
        writer.writerow(["income", "monthly income", income])
        for category, amount in expenses.items():
            writer.writerow(["expense", category, amount])


def load_data(filepath):
    """Read a CSV file and return (income, expenses).

    Raises FileNotFoundError if the file is missing and ValueError if
    any row is malformed.
    """
    income = 0.0
    expenses = {}

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # Line 1 is the header, so data starts on line 2.
        for line_number, row in enumerate(reader, start=2):
            row_type = row.get("type")
            name = row.get("name")
            try:
                amount = float(row.get("amount"))
            except (TypeError, ValueError):
                raise ValueError(f"Invalid amount on line {line_number}.")

            if not math.isfinite(amount) or amount < 0:
                raise ValueError(f"Amount must be a non-negative number on line {line_number}.")

            if row_type == "income":
                income = amount
            elif row_type == "expense" and name:
                # If a category appears twice, add the amounts together.
                expenses[name] = expenses.get(name, 0) + amount
            else:
                raise ValueError(f"Unrecognised row on line {line_number}.")

    return income, expenses

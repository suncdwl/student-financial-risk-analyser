# Student Finance Risk Analyser

A command-line tool, written in plain Python, that helps a student see how healthy their monthly budget is. You enter your income and expenses, and the program calculates your savings rate, assigns a **risk level (LOW / MEDIUM / HIGH)**, shows your biggest spending category, and gives a short tip.

It uses only Python's standard library. No external packages, frameworks, or databases are needed.

## Features

- Set a monthly income and add expenses by category (food, rent, transport, etc.)
- Repeated categories are added together (entering `food` twice sums both amounts)
- Calculates total spent, savings, and savings rate
- Assigns a risk level using simple, transparent rules
- Identifies the biggest expense category and its share of total spending
- Saves and loads data using a CSV file
- Input validation: invalid, negative, zero, or non-numeric amounts are rejected and the user is asked again
- Error handling for missing or corrupted data files
- Simple automated tests for the calculation logic

## Project structure

```
finance-risk-analyser/
├── main.py            # Menu and user interaction (input/print)
├── analyser.py        # Calculations and risk rules (no input/print)
├── storage.py         # Saving and loading CSV data
├── test_analyser.py   # Tests for analyser.py
├── data/
│   └── expenses.csv   # Created automatically when you save
└── README.md
```

Each file has one job. Keeping the calculations in `analyser.py`, separate from the menu, makes them easy to test.

## How to run

**Requirements:** Python 3.8 or newer. Nothing else to install.

1. Open a terminal in the `finance-risk-analyser` folder.
2. Start the program:
   ```
   python main.py
   ```
   (On some systems, use `python3 main.py`.)
3. Use the menu:
   ```
   1. Set monthly income
   2. Add an expense
   3. View report
   4. Save data
   5. Load data
   6. Exit
   ```

To run the tests:
```
python test_analyser.py
```
If everything is correct, it prints `All tests passed!`.

## How the calculations work

| Value | Formula |
|---|---|
| Total spent | sum of all expense amounts |
| Savings | income − total spent |
| Savings rate (%) | (income − total spent) ÷ income × 100 |
| Biggest share (%) | biggest category amount ÷ total spent × 100 |

**Risk levels** are based on the savings rate:

| Savings rate | Risk level |
|---|---|
| 20% or more | LOW |
| 10% to under 20% | MEDIUM |
| Below 10% (including negative) | HIGH |

A negative savings rate means you spent more than you earned. The thresholds are constants at the top of `analyser.py` and can be changed in one place.

## Example output

Income `20000`, with expenses food `6000`, rent `9000`, transport `1500`, and misc `1000`:

```
----- Monthly Report -----
Income:       Rs. 20000.00
Total spent:  Rs. 17500.00
Savings:      Rs. 2500.00
Savings rate: 12.5%
Risk level:   MEDIUM
Biggest expense: rent (Rs. 9000.00, 51% of spending)
Advice: You are saving some money, but there is little room for surprises. Start by looking at your 'rent' spending.
--------------------------
```

Saved file (`data/expenses.csv`):
```
type,name,amount
income,monthly income,20000.0
expense,food,6000.0
expense,rent,9000.0
expense,transport,1500.0
expense,misc,1000.0
```

## Limitations

- **One month at a time.** There are no dates, so it cannot track trends or compare months.
- **One saved file.** Saving overwrites the previous data.
- **One income value.** Multiple income sources must be entered as a single total.
- **Free-text categories.** `food` and `foood` count as different categories; there is no spell-checking.
- **Rule-of-thumb risk levels.** The 10% and 20% thresholds are simple guidelines, not professional financial advice, and they ignore things like debts or emergency funds.
- **Fixed currency label.** The label (`Rs.`) is set by the `CURRENCY` constant in `main.py`.
- **Limited tests.** Only the calculation logic is tested; menu and file handling were checked manually.
- **Command line only.** There is no graphical interface.

## Possible future improvements

- Per-category budget limits with overspend warnings
- Comparing this month with the previous month
- Tests for the CSV save/load functions

## What I learned

Functions and modules, dictionaries and loops, input validation with `try/except`, reading and writing CSV files, and writing simple tests with `assert`.

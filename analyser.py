"""Calculations and risk rules for the Student Finance Risk Analyser.

This file contains NO input() or print() calls. It only takes numbers in
and gives results back, which makes it easy to test.
"""

# Risk thresholds (percent of income saved). Named constants make the
# rules easy to find and change later.
LOW_RISK_MIN_SAVINGS_RATE = 20.0
MEDIUM_RISK_MIN_SAVINGS_RATE = 10.0


def calculate_total_spent(expenses):
    """Add up all expense amounts. `expenses` is a dict: {category: amount}."""
    return sum(expenses.values())


def calculate_savings_rate(income, total_spent):
    """Return the percentage of income left after spending.

    A negative result means the student spent more than they earned.
    """
    if income <= 0:
        raise ValueError("Income must be greater than zero.")
    savings = income - total_spent
    return savings / income * 100


def find_biggest_category(expenses):
    """Return (category, amount) with the highest spending, or None if empty."""
    biggest_name = None
    biggest_amount = 0
    for category, amount in expenses.items():
        if amount > biggest_amount:
            biggest_name = category
            biggest_amount = amount
    if biggest_name is None:
        return None
    return biggest_name, biggest_amount


def get_risk_level(savings_rate):
    """Convert a savings rate (in percent) into LOW, MEDIUM or HIGH risk."""
    if savings_rate >= LOW_RISK_MIN_SAVINGS_RATE:
        return "LOW"
    if savings_rate >= MEDIUM_RISK_MIN_SAVINGS_RATE:
        return "MEDIUM"
    return "HIGH"


def get_advice(risk_level, biggest_category):
    """Return a short, plain-English tip based on the risk level."""
    if risk_level == "LOW":
        advice = "Good job! You are saving a healthy share of your income."
    elif risk_level == "MEDIUM":
        advice = "You are saving some money, but there is little room for surprises."
    else:
        advice = "You are saving very little (or overspending). Review your expenses."

    if risk_level != "LOW" and biggest_category is not None:
        advice += f" Start by looking at your '{biggest_category}' spending."
    return advice


def build_report(income, expenses):
    """Combine all calculations into one dictionary that main.py can print."""
    total_spent = calculate_total_spent(expenses)
    savings_rate = calculate_savings_rate(income, total_spent)
    risk_level = get_risk_level(savings_rate)

    biggest = find_biggest_category(expenses)
    if biggest is None:
        biggest_category, biggest_amount, biggest_share = None, 0, 0
    else:
        biggest_category, biggest_amount = biggest
        biggest_share = biggest_amount / total_spent * 100

    return {
        "income": income,
        "total_spent": total_spent,
        "savings": income - total_spent,
        "savings_rate": savings_rate,
        "risk_level": risk_level,
        "biggest_category": biggest_category,
        "biggest_amount": biggest_amount,
        "biggest_share": biggest_share,
        "advice": get_advice(risk_level, biggest_category),
    }

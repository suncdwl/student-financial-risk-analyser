"""Simple tests for analyser.py. Run with:  python test_analyser.py

`assert condition` does nothing if the condition is True and stops the
program with an error if it is False.
"""

from analyser import build_report, get_risk_level


def test_medium_risk_example():
    expenses = {"food": 6000, "rent": 9000, "transport": 1500, "misc": 1000}
    report = build_report(20000, expenses)
    assert report["total_spent"] == 17500
    assert report["savings"] == 2500
    assert report["savings_rate"] == 12.5
    assert report["risk_level"] == "MEDIUM"
    assert report["biggest_category"] == "rent"


def test_low_risk():
    report = build_report(20000, {"food": 5000, "rent": 6000})
    assert report["risk_level"] == "LOW"


def test_high_risk_when_overspending():
    report = build_report(10000, {"food": 7000, "rent": 5000})
    assert report["savings"] == -2000
    assert report["risk_level"] == "HIGH"


def test_risk_level_boundaries():
    assert get_risk_level(20) == "LOW"
    assert get_risk_level(19.99) == "MEDIUM"
    assert get_risk_level(10) == "MEDIUM"
    assert get_risk_level(9.99) == "HIGH"


def test_no_expenses():
    report = build_report(5000, {})
    assert report["risk_level"] == "LOW"
    assert report["biggest_category"] is None


def test_zero_income_raises_error():
    try:
        build_report(0, {"food": 100})
    except ValueError:
        return  # This is the expected behaviour.
    raise AssertionError("Expected a ValueError for zero income.")


if __name__ == "__main__":
    test_medium_risk_example()
    test_low_risk()
    test_high_risk_when_overspending()
    test_risk_level_boundaries()
    test_no_expenses()
    test_zero_income_raises_error()
    print("All tests passed!")

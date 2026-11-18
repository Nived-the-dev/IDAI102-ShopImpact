import unittest
from datetime import date
from decimal import Decimal
from model import purchase, summary

class ShopImpactTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(summary([], date(2026, 11, 1))["impact"], 0)

    def test_invalid_prices(self):
        for amount in ("", "0", "-10", "NaN", "Infinity", "abc", "1000001", "0.001"):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                purchase("New clothing", amount, "Demo", date(2026, 11, 1))

    def test_twelve_purchases(self):
        day = date(2026, 11, 1)
        categories = ["New clothing", "Second-hand clothing", "New electronics",
                      "Refurbished electronics", "Footwear", "Household goods"]
        expected = [Decimal(x) for x in ("1.3", "0.4", "1.9", "0.7", "1.4", "1.0")]
        records = []
        for i, category in enumerate(categories * 2):
            amount = "100" if i < 6 else "200"
            row = purchase(category, amount, "Demo", day)
            self.assertEqual(row["impact"], expected[i % 6] * (1 if i < 6 else 2))
            records.append(row)
        self.assertEqual(summary(records, day)["spend"], 1800)
        self.assertEqual(summary(records, day)["impact"], Decimal("20.1"))
        self.assertEqual(summary(records, day)["badge"], "Eco Saver")

    def test_month_year(self):
        dates = [date(2025, 11, 1), date(2026, 10, 31), date(2026, 11, 1)]
        rows = [purchase("Footwear", "100", "Demo", day) for day in dates]
        self.assertEqual(len(summary(rows, dates[-1])["rows"]), 1)

    def test_badge_boundary(self):
        day = date(2026, 11, 1)
        a = purchase("Household goods", "1200", "Demo", day)
        b = purchase("Household goods", "1300", "Demo", day)
        c = purchase("Household goods", "1300.01", "Demo", day)
        self.assertIsNone(summary([a], day)["badge"])
        self.assertEqual(summary([a, b], day)["badge"], "Low Impact Shopper")
        self.assertIsNone(summary([a, c], day)["badge"])


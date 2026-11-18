"""Purchase validation and monthly impact calculations."""
from datetime import date
from decimal import Decimal, InvalidOperation

# Teaching assumptions in kg CO2e per INR, not measured product data.
CATEGORIES = {
    "New clothing": ("0.013", ("Repair an item you own.", "Check a local thrift shop or clothing swap.")),
    "Second-hand clothing": ("0.004", ("Borrow an item for a one-off event.", "Try a clothing swap.")),
    "New electronics": ("0.019", ("Ask a repair shop for a quote.", "Compare certified refurbished options with warranties.")),
    "Refurbished electronics": ("0.007", ("Check the seller's repair support and warranty.", "Compare with repairing your current device.")),
    "Footwear": ("0.014", ("Ask a cobbler about resoling your current pair.", "Look for an unused or lightly worn second-hand pair.")),
    "Household goods": ("0.010", ("Compare refillable or repairable alternatives.", "Borrow tools and appliances you rarely use.")),
}
LOWER_IMPACT = {"Second-hand clothing", "Refurbished electronics"}

def purchase(category: str, price: str, brand: str, day: date) -> dict:
    """Validate a purchase and calculate its impact using decimal arithmetic."""
    if category not in CATEGORIES:
        raise ValueError("Select a valid category.")
    try:
        amount = Decimal(price.strip())
    except InvalidOperation as exc:
        raise ValueError("Enter a valid price in rupees.") from exc
    if not amount.is_finite() or not 0 < amount <= 1_000_000:
        raise ValueError("Enter a price above ?0 and up to ?10,00,000.")
    if not brand.strip() or len(brand.strip()) > 50:
        raise ValueError("Enter a brand or use Unbranded (maximum 50 characters).")
    amount = amount.quantize(Decimal("0.01"))
    if amount == 0:
        raise ValueError("Enter at least ?0.01.")
    factor = Decimal(CATEGORIES[category][0])
    return {"category": category, "price": amount, "brand": brand.strip(),
            "date": day, "impact": amount * factor}

def summary(purchases: list[dict], month: date) -> dict:
    rows = [row for row in purchases if (row["date"].year, row["date"].month)
            == (month.year, month.month)]
    spend, impact = Decimal(0), Decimal(0)
    breakdown = {}
    alternatives = 0
    for row in rows:
        spend += row["price"]
        impact += row["impact"]
        category = row["category"]
        breakdown[category] = breakdown.get(category, Decimal(0)) + row["impact"]
        alternatives += category in LOWER_IMPACT
    badge = "Eco Saver" if len(rows) >= 2 and alternatives >= 2 else (
        "Low Impact Shopper" if len(rows) >= 2 and impact <= 25 else None
    )
    return {"rows": rows, "spend": spend, "impact": impact,
            "breakdown": breakdown, "badge": badge}


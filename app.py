"""Streamlit dashboard for planned purchases."""
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

from model import CATEGORIES, purchase, summary
from turtle_art import leaf_svg

st.set_page_config(page_title="ShopImpact", page_icon="??", layout="wide")
st.title("ShopImpact")
st.write("See how your planned purchases add up, and explore alternatives.")
st.caption("Estimates use illustrative factors. Your entries are held in this browser session.")
today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
st.session_state.setdefault("purchases", [])
category = st.selectbox("Product type", CATEGORIES.keys())
left, right = st.columns(2)
price = left.text_input("Price in rupees", placeholder="1250")
brand = right.text_input("Brand", placeholder="Unbranded", max_chars=50)
day = st.date_input("Purchase date", today)
draft = None
if price.strip():
    try:
        draft = purchase(category, price, brand or "Unbranded", day)
    except ValueError as exc:
        st.caption(str(exc))
if draft:
    st.info(f"Estimated impact for this purchase: {draft['impact']:,.2f} kg CO2e")
if st.button("Add purchase", type="primary"):
    if draft is None:
        st.error("Enter a valid price before adding a purchase.")
    else:
        st.session_state.purchases.append(draft)
        st.success(f"Purchase added to {day:%B %Y}.")

st.divider()
months = sorted({today.replace(day=1)} | {
    row["date"].replace(day=1) for row in st.session_state.purchases
}, reverse=True)
month = st.selectbox("Dashboard month", months, index=months.index(today.replace(day=1)),
                     format_func=lambda value: value.strftime("%B %Y"))
result = summary(st.session_state.purchases, month)
main, aside = st.columns([2, 1])
with main:
    a, b, c = st.columns(3)
    a.metric("Planned spend", f"?{result['spend']:,.2f}")
    b.metric("Estimated CO2e", f"{result['impact']:,.2f} kg")
    c.metric("Purchases", len(result["rows"]))
    if result["rows"]:
        st.bar_chart([{"Category": key, "Estimated kg CO2e": float(value)}
                      for key, value in result["breakdown"].items()],
                     x="Category", y="Estimated kg CO2e")
        st.dataframe([{"Date": row["date"], "Category": row["category"], "Brand": row["brand"],
                       "Price (?)": float(row["price"]), "Estimate (kg)": round(float(row["impact"]), 2)}
                      for row in sorted(result["rows"], key=lambda row: row["date"], reverse=True)],
                     hide_index=True)
    else:
        st.info("Add a purchase to see this month's breakdown.")
with aside:
    st.subheader("Consider an alternative")
    for alternative in CATEGORIES[category][1]:
        st.markdown(f"- {alternative}")
    if result["badge"]:
        st.success(result["badge"])
        st.image(leaf_svg(), width=120)
    else:
        st.caption("Two logged purchases unlock badge eligibility.")
    tips = ["Repair before replacing.", "Borrow items you rarely use.",
            "Check whether refurbished products include a warranty."]
    st.caption("Tip � " + tips[len(st.session_state.purchases) % len(tips)])

with st.expander("How the estimate and badges work"):
    st.write("Price x illustrative category factor gives estimated kg CO2e. A higher price "
             "can raise the estimate even for similar items. Brand is a label and does not change the factor.")
    st.table([{"Category": name, "Illustrative kg CO2e per ?": values[0]}
              for name, values in CATEGORIES.items()])
    st.write("Eco Saver requires two second-hand or refurbished entries. Low Impact Shopper "
             "requires at least two entries and a total of 25 kg CO2e or less. Eco Saver takes priority.")


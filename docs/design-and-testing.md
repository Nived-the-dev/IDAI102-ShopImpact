# Design and testing

## User needs

A student comparing two purchases needs an immediate estimate and an affordable alternative. A family tracking several planned purchases needs monthly totals and a way to review the original entries. Both should be able to see why a result changes, so the category factors and badge rules are visible inside the app.

## Dashboard wireframe

| Area | Main elements | Intended action |
| --- | --- | --- |
| Top | Category selector, price, brand, date | Compare the live estimate, then add a row |
| Main | Month selector, spend, CO2e, count, chart, ledger | Review the selected month |
| Side | Alternative, badge, Turtle leaf, tip | Explore a lower-impact option |
| Bottom | Method and badge rules | Understand the numbers and their limits |

Evergreen against off-white supports a clear hierarchy. Badges include text labels, and numerical estimates always show their unit.

## Test and feedback evidence

All five model tests passed locally on Python 3.12. A 12-purchase synthetic dataset produced the expected total of INR 1,800 and 20.10 kg CO2e. The suite also checked empty state, invalid prices, month and year boundaries, and badge thresholds.

| Manual scenario | Expected | Observed |
| --- | --- | --- |
| Preview a valid price | Estimate updates before Add | |
| Add two second-hand items | Eco Saver text and leaf appear | |
| Enter an invalid price | Error with no new ledger row | |
| Select another month | Only records in that month count | |
| Open in a fresh browser session | App loads with an empty ledger | |
| First-time shopper adds an item | Can find Add and explain the estimate | |

First-time shopper feedback is pending. Ask a shopper to log a purchase and explain the estimate. Record the observed difficulty, any change and the result of a retest.



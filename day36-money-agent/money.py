"""Where did your salary go? Categorize a bank statement and get advice (Day 36).

Usage: python money.py statement.csv

Read-only by design: it only reads an exported CSV. It never logs in to your bank or moves money.
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

MODEL = "gpt-4.1-mini"
CATEGORIES = ["Rent", "Food", "Groceries", "Shopping", "Travel", "Bills", "Subscriptions", "Health",
              "Entertainment", "Transfers", "Other"]

CATEGORIZE_PROMPT = f"""Categorize each bank transaction description into exactly one of: {", ".join(CATEGORIES)}.
Food = restaurants and food delivery. Groceries = supermarkets. Subscriptions = recurring apps and memberships.
Reply in JSON: {{"categories": {{"<description>": "<category>"}}}}"""

ADVICE_PROMPT = """You are a friendly personal finance coach. Given monthly spending totals by category and the
largest transactions, give 3 short, specific tips to save money. Use the real numbers. Spot subscriptions the
person may have forgotten. No investment advice. Amounts are in rupees."""


def read_statement(path):
    """Read debits from a CSV with columns: date, description, amount (debits positive or negative)."""
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            row = {k.strip().lower(): (v or "").strip() for k, v in row.items()}
            amount = float(row["amount"].replace(",", ""))
            if row.get("type", "debit").lower() == "credit" or row["description"].lower().startswith("salary"):
                continue
            rows.append({"date": row["date"], "description": row["description"], "amount": abs(amount)})
    return rows


def categorize(transactions, client):
    descriptions = sorted({t["description"] for t in transactions})
    r = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": CATEGORIZE_PROMPT},
                  {"role": "user", "content": "\n".join(descriptions)}])
    mapping = json.loads(r.choices[0].message.content).get("categories", {})
    return [{**t, "category": mapping.get(t["description"]) if mapping.get(t["description"]) in CATEGORIES
             else "Other"} for t in transactions]


def totals_by_category(transactions):
    """The math happens in Python, not in the model: LLMs are bad at adding up numbers."""
    totals = defaultdict(float)
    for t in transactions:
        totals[t["category"]] += t["amount"]
    grand = sum(totals.values()) or 1
    return sorted(((c, round(v, 2), round(100 * v / grand, 1)) for c, v in totals.items()),
                  key=lambda x: -x[1])


def advice(totals, transactions, client):
    biggest = sorted(transactions, key=lambda t: -t["amount"])[:5]
    summary = {"totals": [{"category": c, "amount": a, "percent": p} for c, a, p in totals],
               "largest_transactions": biggest}
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": ADVICE_PROMPT},
                  {"role": "user", "content": json.dumps(summary)}])
    return r.choices[0].message.content


def bar_chart(totals, width=30):
    top = totals[0][1] if totals else 1
    return "\n".join(f"{c:<14} {'█' * max(1, round(width * a / top)):<{width}} Rs {a:>10,.0f}  {p:>5.1f}%"
                     for c, a, p in totals)


def main():
    from dotenv import load_dotenv
    from openai import OpenAI

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("statement", type=Path, help="exported bank statement CSV")
    args = p.parse_args()

    load_dotenv()
    client = OpenAI()
    transactions = categorize(read_statement(args.statement), client)
    totals = totals_by_category(transactions)
    print("WHERE IT WENT\n" + bar_chart(totals))
    print("\nADVICE\n" + advice(totals, transactions, client))


if __name__ == "__main__":
    main()

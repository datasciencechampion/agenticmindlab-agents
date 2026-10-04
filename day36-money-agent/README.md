# Day 36: Where did your salary go?

Export your bank statement as CSV. The agent categorizes every transaction, shows where the money went, and
gives you specific tips to save.

```bash
pip install -r requirements.txt
cp ../.env.example .env        # then add your OPENAI_API_KEY
python money.py sample/statement.csv
```

Example output (the categories and advice will vary):

```text
WHERE IT WENT
Rent           ██████████████████████████████ Rs     30,000   57.2%
Shopping       ██████                         Rs      5,698   10.9%
Groceries      ████                           Rs      4,330    8.3%
Food           ████                           Rs      4,000    7.6%
Subscriptions  ██                             Rs      2,398    4.6%
...

ADVICE
1. You spent Rs 4,000 on Swiggy and Zomato this month...
```

## Your statement

Most banks let you download a statement as CSV from net banking. The file needs these columns:

| Column | Example |
|---|---|
| `date` | `2026-09-03` |
| `description` | `Swiggy order` |
| `amount` | `-450` (debits can be negative or positive) |

Rename your bank's column headers to match if needed. Rows with `type` set to `credit`, and rows starting with
"Salary", are skipped.

## How it works

1. **Read** the CSV.
2. **Categorize**: the model labels each unique description once (Rent, Food, Subscriptions...).
3. **Total**: Python adds up the numbers. LLMs are bad at arithmetic, so the model never does the math.
4. **Advise**: the model sees the totals and biggest transactions and suggests 3 ways to save.

## Safety first

- It only reads an **exported file**. Never give an agent your bank password.
- It's **read-only**: there's no tool that can move money.
- Transaction descriptions are sent to the AI provider. Remove anything you don't want to share.

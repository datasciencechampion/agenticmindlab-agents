import json
from types import SimpleNamespace as NS

import money

CSV = """date,description,amount
2026-09-01,SALARY SEPT,85000
2026-09-01,Rent September,-30000
2026-09-03,Swiggy order,-450
2026-09-05,Swiggy order,-620
2026-09-07,Netflix,-649
2026-09-09,Mystery shop,"-1,200"
"""


class FakeClient:
    def __init__(self, replies):
        self.replies, self.requests = list(replies), []
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return NS(choices=[NS(message=NS(content=self.replies.pop(0)))])


def write_csv(tmp_path):
    path = tmp_path / "statement.csv"
    path.write_text(CSV)
    return path


def test_reads_debits_and_skips_salary(tmp_path):
    rows = money.read_statement(write_csv(tmp_path))
    assert [r["description"] for r in rows] == ["Rent September", "Swiggy order", "Swiggy order", "Netflix",
                                                 "Mystery shop"]
    assert rows[-1]["amount"] == 1200


def test_categorizes_each_description_once_and_rejects_unknown_categories(tmp_path):
    reply = json.dumps({"categories": {"Rent September": "Rent", "Swiggy order": "Food",
                                       "Netflix": "Subscriptions", "Mystery shop": "Shoes"}})
    client = FakeClient([reply])
    txns = money.categorize(money.read_statement(write_csv(tmp_path)), client)
    assert client.requests[0]["messages"][1]["content"].count("Swiggy order") == 1
    assert [t["category"] for t in txns] == ["Rent", "Food", "Food", "Subscriptions", "Other"]


def test_totals_are_computed_in_python():
    txns = [{"category": "Rent", "amount": 30000}, {"category": "Food", "amount": 450},
            {"category": "Food", "amount": 550}]
    assert money.totals_by_category(txns) == [("Rent", 30000, 96.8), ("Food", 1000, 3.2)]

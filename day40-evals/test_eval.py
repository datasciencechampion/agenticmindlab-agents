import json
from pathlib import Path

import eval as ev

CASES = json.loads(Path(__file__).parent.joinpath("cases.json").read_text(encoding="utf-8"))


def test_good_chunking_passes_every_case():
    rows = ev.run(CASES)
    passed, n, pct = ev.scoreboard(rows)
    assert passed == n == 5
    assert pct == 100.0


def test_bad_chunking_fails_last_entry():
    from chunk import chunk_text

    tiny = chunk_text(ev.DOC, size=8, overlap=0)

    def broken(question):
        return ev.retrieve(question, tiny, k=1)[0]

    rows = {r["id"]: r for r in ev.run(CASES, answer_fn=broken)}
    assert rows["last-entry"]["passed"] is False
    assert "1:30" in rows["last-entry"]["missing"]


def test_grade_catches_a_hallucination():
    case = {"must_contain": ["2pm"], "must_not": ["8pm"]}
    passed, missing, leaked = ev.grade(case, "Open Sunday 10am to 8pm")
    assert passed is False
    assert missing == ["2pm"]
    assert leaked == ["8pm"]

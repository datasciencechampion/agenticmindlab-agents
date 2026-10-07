"""How do you know your agent is good? Evals (Day 40).

An eval is a test for an agent: a question, what good looks like, and a score.
This one grades a tiny RAG helper. Swap `answer()` for your own agent.

Usage: python eval.py
"""
import json
from pathlib import Path

from chunk import chunk_text, retrieve

ROOT = Path(__file__).resolve().parent
DOC = (ROOT / "sample" / "clinic.txt").read_text(encoding="utf-8")
# Overlapping chunks — the setting Day 39 showed actually works.
CHUNKS = chunk_text(DOC, size=16, overlap=6)


def answer(question, chunks=CHUNKS):
    """Naive RAG: return the best-matching chunk. Replace this with your agent."""
    return retrieve(question, chunks, k=1)[0]


def grade(case, reply):
    text = reply.lower()
    missing = [n for n in case["must_contain"] if n.lower() not in text]
    leaked = [n for n in case["must_not"] if n.lower() in text]
    passed = not missing and not leaked
    return passed, missing, leaked


def run(cases, answer_fn=answer):
    rows = []
    for case in cases:
        reply = answer_fn(case["q"])
        passed, missing, leaked = grade(case, reply)
        rows.append({**case, "reply": reply, "passed": passed, "missing": missing, "leaked": leaked})
    return rows


def scoreboard(rows):
    passed = sum(1 for r in rows if r["passed"])
    return passed, len(rows), round(100 * passed / len(rows), 1) if rows else 0.0


def main():
    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    rows = run(cases)
    n_pass, n, pct = scoreboard(rows)
    for r in rows:
        mark = "PASS" if r["passed"] else "FAIL"
        why = ""
        if r["missing"]:
            why += f"  missing {r['missing']}"
        if r["leaked"]:
            why += f"  leaked {r['leaked']}"
        print(f"{mark:4}  {r['id']:18}  {r['q']}{why}")
    print(f"\nScore: {n_pass}/{n}  ({pct}%)")
    print("Ship only when the score holds. If it drops, you caught a regression.")


if __name__ == "__main__":
    main()

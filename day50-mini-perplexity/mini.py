"""Mini Perplexity in 5 steps (Day 50): plan, search, read, answer, cite.

Default search is a local sample so it runs offline. Swap `search()` for a real web API when
you're ready.

Usage: python mini.py "Is the EV market growing in India?"
"""
import argparse
import json
from pathlib import Path

MODEL = "gpt-4.1-mini"
PAGES = Path(__file__).resolve().parent / "sample" / "pages.json"
PLAN_PROMPT = """Break the user's question into 2 or 3 short web-search queries.
Reply JSON: {"queries": ["...", "..."]}"""
ANSWER_PROMPT = """Answer using ONLY the numbered sources. Every factual sentence needs a [n] cite.
If a source doesn't support a claim, don't say it. End with a Sources list of url per number.
No extra preamble."""


def load_pages(path=PAGES):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def plan(question, client):
    r = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": PLAN_PROMPT},
                  {"role": "user", "content": question}])
    queries = json.loads(r.choices[0].message.content).get("queries") or [question]
    return [q.strip() for q in queries if str(q).strip()][:3]


def _score(page, query):
    q = {w.strip("?.") for w in query.lower().split()}
    return sum(1 for w in (page["title"] + " " + page["text"]).lower().split() if w.strip(".,") in q)


def search(query, pages, k=2):
    """Keyword search over local pages. Replace this with a real web search later."""
    return sorted(pages, key=lambda p: _score(p, query), reverse=True)[:k]


def read(pages):
    """Keep a short snippet per page so the model can't wander outside the source."""
    out = []
    for i, p in enumerate(pages, 1):
        out.append({"n": i, "title": p["title"], "url": p["url"], "snippet": p["text"][:500]})
    return out


def answer(question, snippets, client):
    sources = "\n\n".join(f"[{s['n']}] {s['title']} ({s['url']})\n{s['snippet']}" for s in snippets)
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": ANSWER_PROMPT},
                  {"role": "user", "content": f"Question: {question}\n\nSources:\n{sources}"}])
    return r.choices[0].message.content


def run(question, client, pages=None):
    pages = pages if pages is not None else load_pages()
    queries = plan(question, client)
    seen, hits = set(), []
    for q in queries:
        for p in search(q, pages):
            if p["url"] not in seen:
                seen.add(p["url"])
                hits.append(p)
    snippets = read(hits)
    return {"queries": queries, "snippets": snippets, "answer": answer(question, snippets, client)}


def main():
    from dotenv import load_dotenv
    from openai import OpenAI

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("question", nargs="?", default="Is the EV market growing in India?")
    args = p.parse_args()
    load_dotenv()
    result = run(args.question, OpenAI())
    print("PLAN")
    for q in result["queries"]:
        print(f"  - {q}")
    print("\nSOURCES")
    for s in result["snippets"]:
        print(f"  [{s['n']}] {s['title']}  {s['url']}")
    print("\nANSWER\n" + result["answer"])


if __name__ == "__main__":
    main()

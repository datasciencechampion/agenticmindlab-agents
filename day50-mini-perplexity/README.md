# Day 50: Mini Perplexity in 5 steps

Day 45 tore down Perplexity. Today you build a tiny version of the same loop.

```bash
pip install -r requirements.txt
cp ../.env.example .env        # then add your OPENAI_API_KEY
python mini.py "Is the EV market growing in India?"
```

```text
PLAN
  - India EV sales
  - India EV policy
SOURCES
  [1] IEA — Global EV Outlook  https://example.com/iea-ev
  ...
ANSWER
Sales are rising [1]. Policy support continues [2].
```

## The 5 steps

1. **Plan** — break the question into 2–3 search queries.
2. **Search** — keyword match over `sample/pages.json` (swap in a real web API later).
3. **Read** — keep a short snippet per page.
4. **Answer** — the model may only use those snippets.
5. **Cite** — every factual sentence gets a `[n]`. No source, no sentence.

That last rule is the product. The sample pages are stand-ins so the demo runs offline and costs
only the two model calls.

## Try next

- Point `search()` at DuckDuckGo, Tavily, or Bing.
- Add Day 40 evals: `must_contain` a cite, `must_not` a fact that isn't in the snippets.
- Add Day 41's output check: if the model is unsure, say so instead of guessing.

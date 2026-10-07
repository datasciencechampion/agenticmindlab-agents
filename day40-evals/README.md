# Day 40: How do you know your agent is good? Evals

An eval is a test for an agent: a question, what good looks like, and a score.
No vibes. Write real cases, run the agent, pass or fail.

```bash
python eval.py
```

```text
PASS  sunday-hours        Are you open on Sunday?
PASS  last-entry          What is the last entry time on Sunday?
...
Score: 5/5  (100.0%)
```

Each case in `cases.json` has `must_contain` (the answer has to say this) and `must_not`
(the answer must not invent this). That covers two of the three scores from the reel:

1. **Did it answer?** — the retrieved chunk has the fact.
2. **Did it stay true?** — `must_not` catches weekday hours leaking into a Sunday answer.
3. **Did it use the right tool?** — add a `tool` field and assert it when you eval a real agent.

## Ship only when the score holds

Change the chunk size in `eval.py` to `size=8, overlap=0` and rerun. The last-entry case
fails. That's a regression — the same one Day 39 showed — caught by a test, not a user.

## Try next

- Replace `answer()` with a call to your Day 32 / 33 / 34 agent.
- Add ten cases from real chats, not ones you invented at a desk.
- Fail the build in CI if the score drops.

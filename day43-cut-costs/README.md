# Day 43: Same agent. 10x cheaper.

Day 26: agents can cost 100x more than a chatbot. Today we cut the bill.

```bash
python cheaper.py
```

```text
TASK                              ROUTE   FAT $     CHEAP $
Are you open on Sunday?           small    0.2000    0.0004
What's the price of a cleaning?   small    0.2000    0.0004
Where is the clinic?              small    0.2000    0.0004
Why was I charged twice last mo   large    0.2000    0.0350
Compare our refund policy to la   large    0.2000    0.0350

5 tasks  fat $1.00   cheap $0.07   14x cheaper
```

## The four cuts

1. **Small models for easy steps** — hours and prices don't need a frontier model.
2. **Trim old context** — fewer tokens per step (`1500` / `3000` vs `4000`).
3. **Cache the system prompt** — pay those tokens once, not on every step.
4. **Cap the steps** — 3 or 6, not 20 (same idea as `MAX_STEPS` on Day 16).

Prices in `PRICE` are illustrative. Paste your model's real per-million-token rate
before you trust the dollar amounts. The *ratio* is the point: measure **cost per task**.

## Try next

- Plug `route()` in front of Day 16's `run()`.
- Log tokens in, tokens out, steps, and $ per task.
- Eval (Day 40) the cheap path so you don't trade away quality for the 10x.

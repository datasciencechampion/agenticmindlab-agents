"""Same agent. 10x cheaper. Here's how (Day 43).

1. Small models for easy steps
2. Trim old context
3. Cache the system prompt (don't resend it as new tokens every time)
4. Cap the steps

Usage: python cheaper.py
"""
EASY_HINTS = ("open", "hours", "price", "timing", "address", "where")
SMALL, LARGE = "small", "large"
# Illustrative prices, dollars per 1 million tokens. Check your model's real pricing.
PRICE = {SMALL: 0.15, LARGE: 2.50}
SYSTEM_TOKENS = 800


def is_easy(question):
    q = question.lower()
    return any(w in q for w in EASY_HINTS)


def route(question):
    return SMALL if is_easy(question) else LARGE


def estimate(steps, tokens_per_step, model, cached_system=False):
    """Rough $ cost. Caching the system prompt means you pay those tokens once, not per step."""
    billed = steps * tokens_per_step
    if cached_system:
        billed -= max(0, steps - 1) * SYSTEM_TOKENS
    return round(billed * PRICE[model] / 1_000_000, 4)


def bill_for(questions, fat=False):
    """fat=True is the wasteful agent: big model, 20 steps, full prompt every time."""
    total = 0.0
    for q in questions:
        if fat:
            total += estimate(20, 4000, LARGE, cached_system=False)
        else:
            model = route(q)
            steps = 3 if model == SMALL else 6
            tokens = 1500 if model == SMALL else 3000
            total += estimate(steps, tokens, model, cached_system=True)
    return round(total, 4)


DEMO = [
    "Are you open on Sunday?",
    "What's the price of a cleaning?",
    "Where is the clinic?",
    "Why was I charged twice last month?",
    "Compare our refund policy to last year",
]


def main():
    fat = bill_for(DEMO, fat=True)
    cheap = bill_for(DEMO, fat=False)
    ratio = round(fat / cheap, 1) if cheap else float("inf")
    print("TASK                              ROUTE   FAT $     CHEAP $")
    for q in DEMO:
        one_fat = bill_for([q], fat=True)
        one_cheap = bill_for([q], fat=False)
        print(f"{q[:32]:32}  {route(q):5}  {one_fat:8.4f}  {one_cheap:8.4f}")
    print(f"\n5 tasks  fat ${fat:.2f}   cheap ${cheap:.2f}   {ratio}x cheaper")
    print("Measure cost per TASK, not per message. Then cut the waste.")


if __name__ == "__main__":
    main()

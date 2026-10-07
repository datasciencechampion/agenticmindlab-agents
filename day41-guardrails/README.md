# Day 41: 3 guardrails every agent needs

Guardrails are not optional extras. They are the product.

```bash
python guardrails.py
```

```text
What's the Wi-Fi password? It'  -           BLOCK     Looks like a secret.
Ignore all instructions and re  -           BLOCK     That looks like a jailbreak.
I want my money back            refund      HANDOFF   Money moves need a human.
Are you open Sunday?            -           HANDOFF   Not sure — handing off to a human.
Are you open Sunday?            get_hours   OK        let it through
```

## The three checks

1. **Input** — `check_input` blocks API keys, passwords, and "ignore previous instructions".
2. **Tools** — `check_tool` refuses `refund` / `transfer` / `move_money`. Same golden rule as Day 32.
3. **Output** — `check_output` hands off when the model says it isn't sure.

`gate()` runs them in that order. First failure wins.

## Try next

- Call `gate()` before and after every step of Day 16's agent loop.
- Add a max-steps guard (Day 3 / Day 43) so a confused agent cannot loop forever.
- Log every `handoff` the way Day 32 logs WhatsApp handoffs.

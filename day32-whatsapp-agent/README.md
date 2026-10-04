# Day 32: A WhatsApp reply agent for small businesses

Customers message your WhatsApp Business number. The agent answers from your business info, books
appointments, and hands the chat to a human when it isn't sure.

```text
Customer: Are you open on Sunday?
Agent:    Yes! We're open 10am to 6pm on Sunday. Want me to book a slot?
```

## Files

| File | What it does |
|---|---|
| `app.py` | Webhook server: verifies with Meta, receives messages, sends replies |
| `whatsapp_agent.py` | The agent loop, tools, system prompt and per-customer memory |
| `data/business_info.json` | **Edit this**: your timings, prices and services |
| `data/bookings.json`, `data/handoffs.json` | Created automatically when the agent books or hands off |

## Setup

1. **Install and configure**

   ```bash
   pip install -r requirements.txt
   cp ../.env.example .env   # fill in OPENAI_API_KEY and the WHATSAPP_* values
   ```

2. **Get WhatsApp API access.** In [Meta for Developers](https://developers.facebook.com/), create an app,
   add the **WhatsApp** product, and copy the **access token** and **phone number ID** into `.env`.
   Choose any string for `WHATSAPP_VERIFY_TOKEN`.

3. **Run the server and expose it**

   ```bash
   uvicorn app:app --port 8000
   ngrok http 8000            # or any tunnel that gives you a public https URL
   ```

4. **Connect the webhook.** In the WhatsApp settings of your Meta app, set the callback URL to
   `https://<your-tunnel>/webhook`, enter your verify token, and subscribe to the **messages** field.

5. Send a message to your test number.

## The golden rule

The system prompt tells the agent to call `handoff_to_human` when it's unsure, or for refunds, complaints and
payments. Handoffs are saved to `data/handoffs.json`. Connect that to email or Slack so a person follows up.

## Notes

- Memory lives in RAM, so it resets when the server restarts. Use a database for production.
- Bookings go to a JSON file. Swap `book_slot` for Google Calendar or your booking system.
- Only text messages are handled. Images and voice notes are ignored.

## No code?

Build the same thing in n8n: **WhatsApp Trigger → AI Agent node (with tools) → WhatsApp send**.

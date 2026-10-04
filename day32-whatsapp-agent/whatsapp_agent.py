"""The agent behind the WhatsApp bot: answers from your business info, books slots, hands off to a human."""
import json
from datetime import datetime
from pathlib import Path

MODEL = "gpt-4.1-mini"
MAX_STEPS = 6
HISTORY_LIMIT = 12
DATA = Path(__file__).parent / "data"

SYSTEM_PROMPT = """You are the WhatsApp assistant for {name}.
Answer questions about timings, prices and services using lookup_info. Book appointments with book_slot.
Golden rule: if you are not sure, or the customer asks about refunds, complaints or payments,
call handoff_to_human. Never guess about money.
Reply in 1-3 short, friendly sentences."""

TOOLS = [
    {"type": "function", "function": {
        "name": "lookup_info",
        "description": "Get the business's timings, prices, services and address.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "book_slot",
        "description": "Book an appointment for the customer.",
        "parameters": {"type": "object", "properties": {
            "name": {"type": "string", "description": "Customer name"},
            "time": {"type": "string", "description": "Requested day and time, e.g. 'Sunday 11am'"},
            "service": {"type": "string"}},
            "required": ["name", "time"]}}},
    {"type": "function", "function": {
        "name": "handoff_to_human",
        "description": "Pass the chat to a human when unsure, or for refunds, complaints and payments.",
        "parameters": {"type": "object", "properties": {"reason": {"type": "string"}}, "required": ["reason"]}}},
]


def load_info():
    return json.loads((DATA / "business_info.json").read_text())


def append_record(filename, record):
    path = DATA / filename
    records = json.loads(path.read_text()) if path.exists() else []
    records.append({**record, "at": datetime.now().isoformat(timespec="seconds")})
    path.write_text(json.dumps(records, indent=2))


class WhatsAppAgent:
    def __init__(self, client):
        self.client = client
        self.history = {}  # customer phone number -> recent messages (short-term memory)

    def call_tool(self, customer, name, args):
        if name == "lookup_info":
            return json.dumps(load_info())
        if name == "book_slot":
            append_record("bookings.json", {"customer": customer, **args})
            return f"Booked {args['time']} for {args['name']}."
        if name == "handoff_to_human":
            append_record("handoffs.json", {"customer": customer, **args})
            return "A team member has been notified and will reply soon."
        return f"Unknown tool: {name}"

    def reply(self, customer, text):
        history = self.history.setdefault(customer, [])
        history.append({"role": "user", "content": text})
        system = {"role": "system", "content": SYSTEM_PROMPT.format(name=load_info()["name"])}
        messages = [system, *history[-HISTORY_LIMIT:]]
        for _ in range(MAX_STEPS):
            r = self.client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
            msg = r.choices[0].message
            if not msg.tool_calls:
                history.append({"role": "assistant", "content": msg.content})
                return msg.content
            messages.append(msg)
            for call in msg.tool_calls:
                result = self.call_tool(customer, call.function.name, json.loads(call.function.arguments))
                messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
        return "Sorry, let me get a team member to help you."

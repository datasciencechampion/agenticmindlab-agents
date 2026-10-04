"""A real AI agent in ~20 lines: a loop + a model + tools (Day 16)."""
import json

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-4.1-mini"
MAX_STEPS = 10


def get_weather(city):
    return f"28°C in {city}"  # swap in a real weather API here


TOOLS = [{"type": "function", "function": {
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]


def run(question, client):
    messages = [{"role": "user", "content": question}]
    for _ in range(MAX_STEPS):
        r = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
        msg = r.choices[0].message
        if not msg.tool_calls:
            return msg.content
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": get_weather(**args)})
    return "Stopped: too many steps."


if __name__ == "__main__":
    load_dotenv()
    print(run("Weather in Goa?", OpenAI()))

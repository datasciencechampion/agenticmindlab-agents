import json
from types import SimpleNamespace as NS

import pytest
from fastapi.testclient import TestClient

import app as webhook
import whatsapp_agent


class FakeClient:
    def __init__(self, replies):
        self.replies, self.requests = list(replies), []
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return NS(choices=[NS(message=self.replies.pop(0))])


def tool_call(name, args):
    return NS(content=None, tool_calls=[NS(id="call_1", function=NS(name=name, arguments=json.dumps(args)))])


def answer(text):
    return NS(content=text, tool_calls=None)


@pytest.fixture(autouse=True)
def temp_data(tmp_path, monkeypatch):
    (tmp_path / "business_info.json").write_text(
        (whatsapp_agent.DATA / "business_info.json").read_text())
    monkeypatch.setattr(whatsapp_agent, "DATA", tmp_path)
    return tmp_path


def test_answers_from_business_info():
    client = FakeClient([tool_call("lookup_info", {}), answer("Yes! Sunday 10am to 6pm.")])
    assert whatsapp_agent.WhatsAppAgent(client).reply("9199", "Open on Sunday?") == "Yes! Sunday 10am to 6pm."
    assert "10am to 6pm" in client.requests[1]["messages"][-1]["content"]


def test_books_a_slot(temp_data):
    client = FakeClient([tool_call("book_slot", {"name": "Asha", "time": "Sunday 11am"}), answer("Booked!")])
    whatsapp_agent.WhatsAppAgent(client).reply("9199", "Book me Sunday 11am, I'm Asha")
    booking = json.loads((temp_data / "bookings.json").read_text())[0]
    assert booking["customer"] == "9199" and booking["time"] == "Sunday 11am"


def test_hands_off_refunds(temp_data):
    client = FakeClient([tool_call("handoff_to_human", {"reason": "refund"}), answer("A human will help.")])
    whatsapp_agent.WhatsAppAgent(client).reply("9199", "I want a refund")
    assert json.loads((temp_data / "handoffs.json").read_text())[0]["reason"] == "refund"


def test_remembers_conversation():
    client = FakeClient([answer("Hi Asha!"), answer("Your name is Asha.")])
    bot = whatsapp_agent.WhatsAppAgent(client)
    bot.reply("9199", "I'm Asha")
    bot.reply("9199", "What's my name?")
    contents = [m["content"] for m in client.requests[1]["messages"]]
    assert "I'm Asha" in contents and "Hi Asha!" in contents


def test_webhook_verification(monkeypatch):
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "secret")
    api = TestClient(webhook.app)
    ok = api.get("/webhook", params={"hub.mode": "subscribe", "hub.verify_token": "secret", "hub.challenge": "42"})
    assert ok.status_code == 200 and ok.text == "42"
    assert api.get("/webhook", params={"hub.mode": "subscribe", "hub.verify_token": "wrong"}).status_code == 403


def test_webhook_replies_to_text_messages(monkeypatch):
    sent = []
    monkeypatch.setattr(webhook, "get_agent", lambda: NS(reply=lambda sender, text: f"echo: {text}"))
    monkeypatch.setattr(webhook, "send_whatsapp", lambda to, text: sent.append((to, text)))
    payload = {"entry": [{"changes": [{"value": {"messages": [
        {"from": "9199", "type": "text", "text": {"body": "Hello"}},
        {"from": "9199", "type": "image", "image": {"id": "x"}}]}}]}]}
    assert TestClient(webhook.app).post("/webhook", json=payload).status_code == 200
    assert sent == [("9199", "echo: Hello")]

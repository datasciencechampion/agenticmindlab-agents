"""WhatsApp Business Cloud API webhook: receive a message, let the agent reply."""
import os

import httpx
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Request, Response
from openai import OpenAI

from whatsapp_agent import WhatsAppAgent

load_dotenv()
GRAPH_URL = "https://graph.facebook.com/v21.0"

app = FastAPI()
_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = WhatsAppAgent(OpenAI())
    return _agent


def extract_messages(payload):
    """Yield (sender, text) for every incoming text message in a webhook payload."""
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            for m in change.get("value", {}).get("messages", []):
                if m.get("type") == "text":
                    yield m["from"], m["text"]["body"]


def send_whatsapp(to, text):
    r = httpx.post(f"{GRAPH_URL}/{os.environ['WHATSAPP_PHONE_NUMBER_ID']}/messages",
                   headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"},
                   json={"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}},
                   timeout=15)
    r.raise_for_status()


def handle(sender, text):
    send_whatsapp(sender, get_agent().reply(sender, text))


@app.get("/webhook")
def verify(request: Request):
    q = request.query_params
    if q.get("hub.mode") == "subscribe" and q.get("hub.verify_token") == os.environ.get("WHATSAPP_VERIFY_TOKEN"):
        return Response(q.get("hub.challenge", ""), media_type="text/plain")
    return Response("Forbidden", status_code=403)


@app.post("/webhook")
async def receive(request: Request, tasks: BackgroundTasks):
    for sender, text in extract_messages(await request.json()):
        tasks.add_task(handle, sender, text)  # reply after returning 200, so Meta doesn't retry
    return {"ok": True}

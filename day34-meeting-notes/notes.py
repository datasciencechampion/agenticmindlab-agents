"""Turn a meeting transcript into a summary, decisions and action items (Day 34).

Usage: python notes.py transcript.vtt [--slack]
"""
import argparse
import json
import os
import re
import urllib.request
from pathlib import Path

MODEL = "gpt-4.1-mini"

SYSTEM_PROMPT = """You write meeting notes from a transcript.
Quote, don't guess: only include what was actually said.
- summary: at most 3 short lines
- decisions: things the group agreed on
- action_items: who does what, by when. If nobody owns a task, set owner to "UNASSIGNED".
  If no deadline was said, set due to null.

Reply in JSON:
{"summary": ["..."], "decisions": ["..."], "action_items": [{"owner": "...", "task": "...", "due": "..."}]}"""

TIMESTAMP = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?[.,]\d{3} --> ")


def clean_transcript(raw):
    """Strip WEBVTT/SRT headers, cue numbers and timestamps; plain text passes through unchanged."""
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line == "WEBVTT" or line.isdigit() or TIMESTAMP.match(line):
            continue
        lines.append(re.sub(r"^<v ([^>]+)>(.*?)(</v>)?$", r"\1: \2", line))
    return "\n".join(lines)


def make_notes(transcript, client):
    r = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": clean_transcript(transcript)}])
    notes = json.loads(r.choices[0].message.content)
    for item in notes.setdefault("action_items", []):
        item["owner"] = item.get("owner") or "UNASSIGNED"
    notes.setdefault("summary", [])
    notes.setdefault("decisions", [])
    return notes


def to_markdown(notes):
    out = ["*Summary*", *[f"• {s}" for s in notes["summary"]], "", "*Decisions*"]
    out += [f"• {d}" for d in notes["decisions"]] or ["• None"]
    out += ["", "*Action items*"]
    for a in notes["action_items"]:
        out.append(f"• {a['owner']}: {a['task']}" + (f" (by {a['due']})" if a.get("due") else ""))
    if not notes["action_items"]:
        out.append("• None")
    return "\n".join(out)


def post_to_slack(text, webhook_url):
    req = urllib.request.Request(webhook_url, data=json.dumps({"text": text}).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=15)


def main():
    from dotenv import load_dotenv
    from openai import OpenAI

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("transcript", type=Path, help=".vtt, .srt or .txt transcript")
    p.add_argument("--slack", action="store_true", help="post to SLACK_WEBHOOK_URL")
    args = p.parse_args()

    load_dotenv()
    text = to_markdown(make_notes(args.transcript.read_text(), OpenAI()))
    print(text)
    if args.slack:
        post_to_slack(text, os.environ["SLACK_WEBHOOK_URL"])
        print("\nPosted to Slack.")


if __name__ == "__main__":
    main()

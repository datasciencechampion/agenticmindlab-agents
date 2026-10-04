import json
from types import SimpleNamespace as NS

import notes

VTT = """WEBVTT

1
00:00:01.000 --> 00:00:04.000
<v Priya>Can we move the launch to 15 October?</v>

2
00:00:05.000 --> 00:00:07.500
<v Rahul>Yes, agreed.</v>
"""


class FakeClient:
    def __init__(self, reply):
        self.reply, self.requests = reply, []
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return NS(choices=[NS(message=NS(content=json.dumps(self.reply)))])


def test_cleans_vtt():
    assert notes.clean_transcript(VTT) == "Priya: Can we move the launch to 15 October?\nRahul: Yes, agreed."


def test_plain_text_passes_through():
    assert notes.clean_transcript("Priya: hello\nRahul: hi") == "Priya: hello\nRahul: hi"


def test_marks_unowned_tasks_unassigned():
    client = FakeClient({"summary": ["Launch moved"], "decisions": ["Launch on 15 Oct"],
                         "action_items": [{"owner": "Priya", "task": "Update deck", "due": "Friday"},
                                          {"owner": None, "task": "Tell support", "due": None}]})
    result = notes.make_notes(VTT, client)
    assert [a["owner"] for a in result["action_items"]] == ["Priya", "UNASSIGNED"]
    assert "Priya: Can we move" in client.requests[0]["messages"][1]["content"]


def test_markdown_output():
    text = notes.to_markdown({"summary": ["Launch moved"], "decisions": [],
                              "action_items": [{"owner": "Priya", "task": "Update deck", "due": "Friday"}]})
    assert "• Priya: Update deck (by Friday)" in text
    assert "*Decisions*\n• None" in text

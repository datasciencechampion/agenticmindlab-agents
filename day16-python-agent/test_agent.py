import json
from types import SimpleNamespace as NS

import agent


class FakeClient:
    """Replays scripted model replies and records every request."""

    def __init__(self, replies):
        self.replies, self.requests = list(replies), []
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return NS(choices=[NS(message=self.replies.pop(0))])


def tool_call(name, args, id="call_1"):
    return NS(content=None, tool_calls=[NS(id=id, function=NS(name=name, arguments=json.dumps(args)))])


def test_calls_tool_then_answers():
    client = FakeClient([tool_call("get_weather", {"city": "Goa"}),
                         NS(content="It's 28°C in Goa.", tool_calls=None)])
    assert agent.run("Weather in Goa?", client) == "It's 28°C in Goa."
    tool_msg = client.requests[1]["messages"][-1]
    assert tool_msg == {"role": "tool", "tool_call_id": "call_1", "content": "28°C in Goa"}


def test_stops_after_max_steps():
    client = FakeClient([tool_call("get_weather", {"city": "Goa"})] * agent.MAX_STEPS)
    assert agent.run("Loop forever", client) == "Stopped: too many steps."
    assert len(client.requests) == agent.MAX_STEPS

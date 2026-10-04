import json
from types import SimpleNamespace as NS

import tailor


class FakeClient:
    def __init__(self, reply):
        self.reply, self.requests = reply, []
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return NS(choices=[NS(message=NS(content=json.dumps(self.reply)))])


def test_returns_tailored_resume_and_score():
    client = FakeClient({"tailored_resume": "# Asha\n- Built Python APIs", "match_score": 82,
                         "missing_skills": ["Docker"], "changes": ["Reworded backend bullet"]})
    result = tailor.tailor("# Asha\n- Worked on backend services", "Python developer, Docker a plus", client)
    assert result["match_score"] == 82 and result["missing_skills"] == ["Docker"]
    request = client.requests[0]
    assert request["response_format"] == {"type": "json_object"}
    assert "Never invent experience" in request["messages"][0]["content"]
    assert "Worked on backend services" in request["messages"][1]["content"]


def test_cleans_up_bad_model_output():
    result = tailor.tailor("resume", "job", FakeClient({"tailored_resume": "x", "match_score": "140"}))
    assert result["match_score"] == 100
    assert result["missing_skills"] == [] and result["changes"] == []

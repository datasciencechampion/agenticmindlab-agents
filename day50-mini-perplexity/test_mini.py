import json
from types import SimpleNamespace as NS

import mini


class FakeClient:
    def __init__(self, replies):
        self.replies, self.requests = list(replies), []
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return NS(choices=[NS(message=NS(content=self.replies.pop(0)))])


PAGES = mini.load_pages()


def test_search_ranks_the_ev_sales_page_first():
    hits = mini.search("EV sales India", PAGES)
    assert "EV Outlook" in hits[0]["title"]


def test_read_numbers_snippets():
    snippets = mini.read(PAGES[:2])
    assert [s["n"] for s in snippets] == [1, 2]
    assert snippets[0]["url"] == PAGES[0]["url"]


def test_run_plans_searches_then_answers_from_sources():
    client = FakeClient([
        json.dumps({"queries": ["India EV sales", "India EV policy"]}),
        "Sales are rising [1]. Policy support continues [2].\nSources: [1] [2]",
    ])
    result = mini.run("Is the EV market growing in India?", client, pages=PAGES)
    assert result["queries"] == ["India EV sales", "India EV policy"]
    assert "[1]" in result["answer"]
    assert client.requests[1]["messages"][0]["content"].startswith("Answer using ONLY")
    assert "example.com/iea-ev" in client.requests[1]["messages"][1]["content"]

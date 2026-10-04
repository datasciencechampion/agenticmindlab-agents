# Agentic Mind Lab: AI agent builds

Source code for the build reels on Instagram [@agenticmindlab](https://www.instagram.com/agenticmindlab/).
Every project is small, runs on its own, and matches what you saw in the reel.

| Day | Build | Folder |
|---|---|---|
| 16 | A real AI agent in ~20 lines of Python | [`day16-python-agent`](day16-python-agent) |
| 32 | WhatsApp reply agent for small businesses | [`day32-whatsapp-agent`](day32-whatsapp-agent) |
| 33 | Resume tailor: match any job post, never invent experience | [`day33-resume-agent`](day33-resume-agent) |
| 34 | Meeting notes: summary, decisions, action items, Slack | [`day34-meeting-notes`](day34-meeting-notes) |
| 36 | Money agent: where did your salary go? | [`day36-money-agent`](day36-money-agent) |

## Quick start

You need Python 3.10+ and an [OpenAI API key](https://platform.openai.com/api-keys).

```bash
git clone https://github.com/datasciencechampion/agenticmindlab-agents.git
cd agenticmindlab-agents/day16-python-agent
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env                               # add your OPENAI_API_KEY
python agent.py
```

Each folder's README explains its setup. The models are set with `MODEL = "gpt-4.1-mini"` at the top of each
file; change it to any OpenAI model that supports tool calling and JSON output.

## Tests

The tests use a fake model, so they run offline and cost nothing:

```bash
pip install pytest fastapi httpx
pytest
```

## Safety

- Never commit your `.env` file or paste API keys anywhere public.
- These are learning projects. Review the code before you connect it to real customers, money or data.
- Running them calls the OpenAI API, which costs money (usually a fraction of a rupee per run).

## License

MIT. Use it, change it, build on it. A shout-out to [@agenticmindlab](https://www.instagram.com/agenticmindlab/) is
appreciated!

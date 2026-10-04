# Day 16: A real AI agent in ~20 lines of Python

No framework. Just a loop, a model and one tool.

```bash
pip install -r requirements.txt
cp ../.env.example .env        # then add your OPENAI_API_KEY
python agent.py
# It's 28°C in Goa.
```

## How it works

1. **The tool**: `get_weather` is a normal Python function, and `TOOLS` describes it so the model knows how to call it.
2. **The loop**: send the messages and tools to the model. If it doesn't ask for a tool, print the answer and stop.
3. **Run the tool**: append the model's request, call the function, send the result back, and loop again.

`MAX_STEPS` stops the loop if the model keeps calling tools forever (see Day 3).

## Try next

- Replace `get_weather` with a real API such as [Open-Meteo](https://open-meteo.com/) (free, no key).
- Add a second tool and watch the model choose between them.
- Change `MODEL` to any OpenAI model that supports tool calling.

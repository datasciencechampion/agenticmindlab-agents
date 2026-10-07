# Day 38: Your own MCP server in ~15 lines

Day 11 called MCP the USB-C of AI. Today you build the plug: a tiny server with two tools,
`get_hours` and `book_slot`. Any MCP client can call them.

```bash
pip install -r requirements.txt
python server.py
```

Then connect `server.py` as an MCP server in Claude Desktop or Cursor and ask:

```text
Are you open on Sunday?
```

The client discovers `get_hours`, calls it with `day="sunday"`, and answers from the result.

## The 15 lines

`server.py` is the whole build. The two tools are ordinary Python functions. `FastMCP`
names the server, `mcp.tool()` exports each function, and `mcp.run()` speaks the protocol
over stdio.

## Only install servers you trust

An MCP server can see whatever you give it access to — files, APIs, calendars. Treat a new
server like an app permission prompt.

## Try next

- Edit `HOURS` to match a real shop.
- Add `lookup_price(item)` and watch the client pick the right tool.
- Point Day 32's WhatsApp agent at these same tools.

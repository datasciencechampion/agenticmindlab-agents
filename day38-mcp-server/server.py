"""Your own MCP server in ~15 lines (Day 38).

An MCP server wraps a tool. Any MCP client (Claude, Cursor, or your own agent) can then call it.

Usage:
    pip install -r requirements.txt
    python server.py          # stdio MCP server — connect this in Claude / Cursor
"""
HOURS = {"monday": "10am-8pm", "tuesday": "10am-8pm", "wednesday": "10am-8pm",
         "thursday": "10am-8pm", "friday": "10am-8pm", "saturday": "10am-6pm",
         "sunday": "10am-2pm. Last entry 1:30pm"}


def get_hours(day: str) -> str:
    """Return opening hours for a weekday (monday … sunday)."""
    return HOURS.get(day.strip().lower(), "Closed that day.")


def book_slot(name: str, time: str) -> str:
    """Book a walk-in slot. Demo only — does not write to a real calendar."""
    return f"Booked {name} at {time}. We'll text if anything changes."


if __name__ == "__main__":
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("shop-hours")
    mcp.tool()(get_hours)
    mcp.tool()(book_slot)
    mcp.run()

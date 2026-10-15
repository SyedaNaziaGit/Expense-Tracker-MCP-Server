#  Expense Tracker MCP Server

A simple **Expense Tracker MCP (Model Context Protocol) server** built with [FastMCP](https://gofastmcp.com) and SQLite, designed to be used from **Claude Desktop**. Ask Claude in plain English to log, list, and summarize your expenses.

This repo is also my learning log for MCP: it documents how I built this server step by step, how I connected it to Claude Desktop, and how I tried out a few other community MCP servers (Manim, Weather).
---
## ✨ Features

### Tools

| Tool | What it does |
| --- | --- |
| `add_expense` | Add a new expense (date, amount, category, note) |
| `list_expenses` | View expenses within a date range |
| `summarize` | Summarize spending by category |

### Resources

| Resource | What it returns |
| --- | --- |
| `expense:///categories` | Available expense categories and subcategories |

>  *Tool and resource names above follow the reference project. Adjust the table to match whatever is defined in `main.py`.*

---

##  Tech Stack

- **Python** 3.12+
- **FastMCP** (tested with 3.4.4) and **MCP** (tested with 1.28.1)
- **SQLite** for storage
- **uv** for dependency and environment management
- **Claude Desktop** as the MCP client
- **MCP Inspector** (by Anthropic) for testing and debugging

---

##  Project Structure

```
Expense-Tracker-MCP-Server/
├── main.py          # FastMCP server: tools and resources
├── expenses_db      # SQLite database file
├── pyproject.toml   # Project metadata and dependencies (uv)
├── uv.lock          # Locked dependency versions
└── README.md
```

---

##  Getting Started

### Prerequisites

- Python 3.12 or newer
- [Claude Desktop](https://claude.ai/download)
- VS Code (or any editor)

### 1. Install `uv`

```bash
pip install uv
```

### 2. Create the project

```bash
mkdir expense-tracker-mcp-server
cd expense-tracker-mcp-server
uv init .
```

### 3. Add FastMCP

```bash
uv add fastmcp
```

### 4. Verify the installation

```bash
fastmcp version
```

Sample output:

```
FastMCP version: 3.4.4
MCP version:     1.28.1
Python version:  3.12.6
Platform:        Windows-11
```

### 5. Write the server

Create `main.py` with your FastMCP tools and resources for a clean async SQLite example using `aiosqlite`).

---

##  Run and Debug

**Test with MCP Inspector** (the quickest way to check that tools work before touching Claude):

```bash
uv run fastmcp dev main.py
```

**Run the server directly:**

```bash
uv run fastmcp run main.py
```

---

##  Connect to Claude Desktop

### Option A: One-line install (recommended)

```bash
uv run fastmcp install claude-desktop main.py
```

### Option B: Edit the config manually

1. Open **Claude Desktop → Settings → Developer → Edit Config**
2. This opens `claude_desktop_config.json`. Add your server under `mcpServers`:

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/absolute/path/to/main.py"
      ]
    }
  }
}
```

3. **Fully quit and restart Claude Desktop.** Do this after every config change or newly added MCP server.

### Screenshots

<!-- Replace these with your own images, e.g. put them in a docs/ folder -->
![Claude Desktop MCP config](docs/claude-config.png)
![Expense tracker in action](docs/demo.png)

---

##  Example Prompts

Once connected, try these in Claude Desktop:

**Add an expense**
```
Add an expense for a cab ride to Delhi last Sunday. The fare was ₹600.
```

**List expenses**
```
Show all expenses between 2026-06-01 and 2026-06-30.
```

**Summarize**
```
Summarize my expenses for June 2026 by category.
```

---

##  Expense Categories

The server supports categories such as:

Food · Transport · Housing · Utilities · Health · Education · Entertainment · Shopping · Travel · Business · Investments · Personal Care · Taxes · Miscellaneous

---

## ☁️ Deploying to FastMCP Cloud (Optional)

The local setup above only works on your machine. To make the server available remotely, you can deploy it to **FastMCP Cloud**, as done in [expense-tracker-mcp-cloud](https://github.com/NeelContractor/expense-tracker-mcp-cloud).

Once deployed you get a remote endpoint like:

```
https://<your-project-name>.fastmcp.app/mcp
```

To use it from Claude Desktop, create a small local proxy (`proxy.py`):

```python
from fastmcp import FastMCP

mcp = FastMCP.as_proxy(
    "https://<your-project-name>.fastmcp.app/mcp",  # get your URL from FastMCP Cloud
    name="Expense Tracker Proxy"
)

if __name__ == "__main__":
    mcp.run()
```

Then install it into Claude Desktop and restart:

```bash
uv run fastmcp install claude-desktop proxy.py
```

---

## Other MCP Servers I Tried

While learning MCP I also set up a few community servers. Notes below for future me (and anyone else).

> After adding any server, **restart Claude Desktop**.

###  Manim MCP Server (math animations)

Repo: [abhiemj/manim-mcp-server](https://github.com/abhiemj/manim-mcp-server)

**Setup**

```bash
pip install manim
pip install mcp

cd ~/Desktop
git clone https://github.com/abhiemj/manim-mcp-server.git
cd manim-mcp-server
```

**Find the paths you need**

```bash
which python3        # path to your Python executable  -> "command"
which manim          # path to the manim executable    -> MANIM_EXECUTABLE
cd src && pwd        # folder containing manim_server.py
```

> On Windows use `where python` and `where manim` instead of `which`.

**Add to `claude_desktop_config.json`** (Settings → Developer → Edit Config):

```json
{
  "mcpServers": {
    "manim-server": {
      "command": "/absolute/path/to/python",
      "args": [
        "/absolute/path/to/manim-mcp-server/src/manim_server.py"
      ],
      "env": {
        "MANIM_EXECUTABLE": "/absolute/path/to/manim"
      }
    }
  }
}
```

**Test prompt**

```
Use the manim-server to create an animation showing the concept of vector
transformation in linear algebra.

- Start with a 2D coordinate grid.
- Show two basis vectors: i = (1,0) in red and j = (0,1) in blue.
- Animate a transformation by applying a matrix A = [[2,1],[1,1]] to the
  grid and the vectors.
- Show the grid warping and the basis vectors moving to their new
  transformed positions.
- Add a title above: 'Linear Algebra: Matrix Transformation Demo'.
```

###  Twitter / X MCP Server (local)

Repo: [EnesCinr/twitter-mcp](https://github.com/EnesCinr/twitter-mcp)

Add this inside the `mcpServers` object of your Claude config:

```json
{
  "mcpServers": {
    "twitter-mcp": {
      "command": "npx",
      "args": ["-y", "@enescinar/twitter-mcp"],
      "env": {
        "API_KEY": "your_api_key_here",
        "API_SECRET_KEY": "your_api_secret_key_here",
        "ACCESS_TOKEN": "your_access_token_here",
        "ACCESS_TOKEN_SECRET": "your_access_token_secret_here"
      }
    }
  }
}
```

You get the keys from the Twitter/X developer console.

###  Weather MCP Server (remote via `uvx`)

Repo: [adhikasp/mcp-weather](https://github.com/adhikasp/mcp-weather)

Get a free API key from [AccuWeather Developer](https://developer.accuweather.com/home), then add:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/adhikasp/mcp-weather.git",
        "mcp-weather"
      ],
      "env": {
        "ACCUWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

###  Finding more MCP servers

Browse the curated list: [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)

>  **Never commit real API keys.** Keep them in your local config file only.

---

##  Troubleshooting

| Problem | Fix |
| --- | --- |
| Server doesn't show up in Claude | Fully quit Claude Desktop (check the system tray) and reopen it |
| `fastmcp` command not found | Close and reopen VS Code / your terminal after installing |
| Config changes have no effect | Check the JSON is valid and paths are **absolute** |
| Not sure if the server works | Run `uv run fastmcp dev main.py` and test the tools in MCP Inspector first |
| Wrong Python or manim path | Re-run `which python3` / `which manim` (or `where` on Windows) |

---

##  What I Learned

- FastMCP fundamentals: tools and resources
- Building and debugging an MCP server with MCP Inspector
- SQLite integration for persistent storage
- Connecting MCP servers to Claude Desktop (via `fastmcp install` and manual config)
- Setting up third-party MCP servers (Manim, Twitter/X, Weather)
- Remote deployment and proxying with FastMCP Cloud

---

##  Credits

- [abhiemj/manim-mcp-server](https://github.com/abhiemj/manim-mcp-server)
- [EnesCinr/twitter-mcp](https://github.com/EnesCinr/twitter-mcp)
- [adhikasp/mcp-weather](https://github.com/adhikasp/mcp-weather)
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- [FastMCP](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

<img width="857" height="277" alt="image" src="https://github.com/user-attachments/assets/312e336a-6e80-480a-9f86-2d9da102ff86" />

<img width="857" height="277" alt="image" src="https://github.com/user-attachments/assets/70ceb26d-d0c1-4beb-acf3-29e7f881e6b3" />

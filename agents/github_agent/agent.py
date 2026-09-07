"""
github_agent — Interacts with GitHub using the official GitHub MCP server.

Uses Model Context Protocol (MCP) to connect to @modelcontextprotocol/server-github
via npx. The MCP server exposes GitHub APIs as tools that ADK can call natively.

Key concept: Instead of writing individual tool functions, McpToolset connects
to an external MCP server and imports ALL its tools automatically. This is how
you give an agent access to entire platforms (GitHub, Slack, Notion, etc.)
with just a few lines of code.

Available GitHub MCP tools (subset used here):
  - search_repositories     search GitHub repos by query
  - get_file_contents       read any file from any repo
  - list_issues             list issues on a repo
  - get_issue               get details of a specific issue
  - search_code             search code across GitHub
  - list_commits            list recent commits on a repo
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioServerParameters

# Load GITHUB_PERSONAL_ACCESS_TOKEN from .env
load_dotenv()

github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
if not github_token:
    raise ValueError(
        "GITHUB_PERSONAL_ACCESS_TOKEN not found in .env\n"
        "Run: echo 'GITHUB_PERSONAL_ACCESS_TOKEN=$(gh auth token)' >> .env"
    )

# McpToolset connects to the GitHub MCP server via npx.
# npx downloads and runs @modelcontextprotocol/server-github on first use.
# The token is passed as an environment variable to the MCP server process.
github_toolset = McpToolset(
    connection_params=StdioServerParameters(
        command="github-mcp-server",   # native binary via: brew install github-mcp-server
        args=["stdio"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token},
    ),
    # Only expose the tools we actually need — keeps the agent focused
    tool_filter=[
        "search_repositories",
        "get_file_contents",
        "list_issues",
        "get_issue",
        "search_code",
        "list_commits",
    ],
)

root_agent = Agent(
    name="github_agent",
    model="gemini-2.5-flash",
    description="Interacts with GitHub repos using the GitHub MCP server.",
    instruction="""
    You are a helpful GitHub assistant for the user BigBro2454.
    You have access to GitHub via the MCP protocol. Use your tools to:

    - Search for repositories on GitHub
    - Read files from any public repository
    - List and inspect issues on repositories
    - Search code across GitHub
    - List recent commits

    When the user asks about their own repos, search for user:BigBro2454.
    Always be specific with repo names in the format owner/repo (e.g. BigBro2454/google-adk).
    Present results clearly and concisely.
    """,
    tools=[github_toolset],
)

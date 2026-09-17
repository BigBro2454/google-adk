"""
research_agent — Orchestrator delegating lookups to search_specialist via AgentTool.

Week 6 — Agent-as-a-Tool and Sub-Agents (Project 5.1)

Key concept:
- Single Responsibility Principle: One agent delegates to an expert sub-agent.
- AgentTool: Exposes an agent directly as a callable tool for another agent.
"""

from google.adk.agents import Agent
from google.adk.tools import AgentTool
from shared.utils.fallback_model import FallbackLlm
from .search_agent import search_agent

# Expose the specialist search_agent as an executable tool
search_agent_tool = AgentTool(
    agent=search_agent,
    skip_summarization=False,
)

root_agent = Agent(
    name="research_orchestrator",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="A senior research orchestrator that analyzes complex technical questions by delegating queries to a search specialist sub-agent.",
    instruction="""
    You are a Lead AI Architect and Research Orchestrator named Ada.
    Your objective is to answer technical questions comprehensively by consulting your specialist tools.

    Workflow:
    1. Analyze the user's research question.
    2. Delegate targeted technical inquiries to your `search_specialist` tool.
    3. Synthesize the findings into an executive-level summary with architecture implications, benefits, and key specs.
    """,
    tools=[search_agent_tool],
    sub_agents=[search_agent],
)

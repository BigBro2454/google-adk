"""
writer_reviewer pipeline — Generator + Reviewer collaborative authoring.

Week 6 — Agent-as-a-Tool and Sub-Agents (Project 5.2)

Key concept:
- Generator Pattern: Sub-agent synthesizes content.
- Reviewer Pattern: Sub-agent critiques and verifies content.
- Orchestrator combines the loop to deliver publication-ready output.
"""

from google.adk.agents import Agent
from google.adk.tools import AgentTool
from shared.utils.fallback_model import FallbackLlm
from .generator_agent import generator_agent
from .reviewer_agent import reviewer_agent

generator_tool = AgentTool(agent=generator_agent)
reviewer_tool = AgentTool(agent=reviewer_agent)

root_agent = Agent(
    name="editorial_director",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="Orchestrates a collaborative writing and editorial review pipeline using Generator and Reviewer sub-agents.",
    instruction="""
    You are the Managing Editor and Editorial Director.
    When a user requests a blog post or technical article:
    1. First, call `blog_generator` to produce an initial comprehensive draft.
    2. Next, pass that draft to `blog_reviewer` to obtain an editorial critique and quality score.
    3. Finally, synthesize both: present the initial draft, summarize the reviewer's score & feedback, and provide the final polished publication-ready version incorporating the feedback!
    """,
    tools=[generator_tool, reviewer_tool],
    sub_agents=[generator_agent, reviewer_agent],
)

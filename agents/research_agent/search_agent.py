"""
Specialist search_agent dedicated to querying and retrieving technical facts.

Week 6 — Agent-as-a-Tool and Sub-Agents (Project 5.1)
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm
from .tools.search_tools import search_knowledge_base

search_agent = Agent(
    name="search_specialist",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="A specialist agent that retrieves raw technical documents and documentation.",
    instruction="""
    You are a fast, precise technical retrieval specialist.
    Your only job is to query the technical knowledge base using `search_knowledge_base(query=...)`
    and return the factual results concisely. Do not add fluff or speculate.
    """,
    tools=[search_knowledge_base],
)

"""
Generator agent for drafting technical blog posts.

Week 6 — Agent-as-a-Tool and Sub-Agents (Project 5.2)
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm

generator_agent = Agent(
    name="blog_generator",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="Generates engaging, technically accurate blog post drafts on software engineering and AI architectures.",
    instruction="""
    You are an expert technical writer and software blogger.
    Given a topic or outline, write a well-structured blog post draft including:
    - Catchy title
    - Executive summary
    - Key architectural concepts
    - Code snippet or workflow illustration
    - Conclusion and key takeaways
    """,
    tools=[],
)

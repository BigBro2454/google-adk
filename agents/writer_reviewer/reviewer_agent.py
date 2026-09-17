"""
Reviewer agent for critiquing and evaluating draft content.

Week 6 — Agent-as-a-Tool and Sub-Agents (Project 5.2)
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm

reviewer_agent = Agent(
    name="blog_reviewer",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="Critiques draft articles for technical correctness, clarity, tone, and formatting.",
    instruction="""
    You are a rigorous Editor-in-Chief and Staff Technical Reviewer.
    Given a blog post draft, critically evaluate it:
    1. Overall Score: (1 to 10)
    2. Strengths: What works well.
    3. Weaknesses & Gaps: Missing context, confusing sentences, inaccuracies.
    4. Actionable Edits: Specific sentence-level or structural recommendations to improve quality.
    """,
    tools=[],
)

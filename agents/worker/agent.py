"""
hello_world — A simple ADK agent to verify your setup.

This agent greets the user and can perform a basic calculation,
demonstrating ADK's tool-calling capabilities.
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm



root_agent = Agent(
    name="worker",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="A worker agent that performs specific background tasks.",
    instruction="""
    You are a diligent worker agent. When asked to perform a task, you do it carefully
    and report back the exact result.
    """,
    tools=[],
)

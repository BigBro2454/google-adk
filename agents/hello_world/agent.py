"""
hello_world — A simple ADK agent to verify your setup.

This agent greets the user and can perform a basic calculation,
demonstrating ADK's tool-calling capabilities.
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm
from .tools.calculator import add, multiply, subtract


root_agent = Agent(
    name="hello_world",
    model=FallbackLlm(
        primary="gemini-2.5-flash",          # used normally
        fallback="ollama_chat/qwen2.5:7b",   # kicks in on rate limits
    ),
    description="A friendly greeting agent that can also do simple math.",
    instruction="""
    You are a math assistant. Greet the user warmly and help them with
    any questions on mathematics. You also have access to calculator tools — use them
    when the user asks for arithmetic.
    """,
    tools=[add, subtract, multiply],
)

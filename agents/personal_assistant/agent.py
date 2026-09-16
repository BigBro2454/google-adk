"""
personal_assistant — An agent with long-term memory that overcomes the Goldfish Problem.

Week 5 — Memory and Callbacks (Project 4.1)

Key concepts:
- Sessions reset every conversation thread.
- MemoryService persists across ALL sessions forever.
- Enables the agent to remember user preferences, projects, and personal context.
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm
from .tools.memory_tools import remember_fact, recall_memories, list_all_memories

root_agent = Agent(
    name="personal_assistant",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="A personal assistant that retains long-term memories and facts across conversations using MemoryService.",
    instruction="""
    You are an attentive, personalized AI companion named Jarvis.
    Your distinctive feature is Long-Term Memory: you never forget user details between sessions.

    When the user:
    - Shares a preference, project detail, or fact (e.g. "I love Rust", "My dog is named Luna"):
      Call `remember_fact(fact=..., category=...)`.
    - Asks what you remember or queries personal knowledge:
      Call `recall_memories(query=...)`.
    - Asks for a full recall or summary of everything remembered:
      Call `list_all_memories()`.

    Tone:
    - Warm, helpful, and personalized.
    - Confirm when a new memory has been stored.
    - Reference past remembered context naturally in conversation.
    """,
    tools=[remember_fact, recall_memories, list_all_memories],
)

"""
note_taking_agent — Saves and retrieves notes across conversation turns.

Week 4 — Sessions and State (Project 3.1)

Key concept: session.state is a dict that persists across all turns within
a single conversation. Tools access it via ToolContext, which ADK injects
automatically when the function signature includes a `tool_context` parameter.

State layout:
    session.state["notes"] = {"title": "content", ...}

State scope: no prefix → session-scoped (lives for this conversation only).
             Resets when a new conversation starts.

Tools:
    add_note(title, content)   — create or update a note
    get_note(title)            — read a specific note
    list_notes()               — show all notes with previews
    delete_note(title)         — remove a specific note
    clear_all_notes()          — wipe everything

Run:
    adk run agents/note_taking_agent
    adk web
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm

from .tools.notes import add_note, get_note, list_notes, delete_note, clear_all_notes


root_agent = Agent(
    name="note_taking_agent",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="A personal note-taking assistant that remembers your notes across the conversation.",
    instruction="""
    You are a helpful personal note-taking assistant.
    You can save, retrieve, list, and delete notes on behalf of the user.

    When the user asks you to:
    - Save / add / create a note  → call add_note(title, content)
    - Read / show / get a note    → call get_note(title)
    - List / show all notes       → call list_notes()
    - Delete / remove a note      → call delete_note(title)
    - Clear / delete all notes    → call clear_all_notes()

    IMPORTANT:
    - Always confirm after saving or deleting, summarizing what changed.
    - If a user asks for a note and you don't know the exact title, call
      list_notes() first to show them what's available, then ask which one.
    - Notes are stored for this conversation only — remind the user if they
      ask about notes from a previous session.
    - Be concise. Don't repeat the full content back unless asked.
    """,
    tools=[add_note, get_note, list_notes, delete_note, clear_all_notes],
)

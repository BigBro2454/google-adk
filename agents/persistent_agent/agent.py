"""
persistent_agent — Demonstrates SQLite-backed persistence and state scoping in Google ADK.

Week 4 — Sessions and State (Project 3.3)

Key concepts:
1. DatabaseSessionService:
   Backs ADK sessions with an SQLite relational database (`sessions.db`).
   Session events, state, user state, and app state are persisted across process restarts.

2. State Scopes:
   - Session-scoped (no prefix): `tasks`, session scratchpad. Persists across turns and restarts for this session_id.
   - User-scoped (`user:` prefix): `user:preferences`. Persists across all sessions for the same user_id.
   - App-scoped (`app:` prefix): `app:stats`. Persists globally across all users.

Run:
    adk run agents/persistent_agent --session_service_uri sqlite:///sessions.db
    python runners/sqlite_session_runner.py --demo
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm

from .tools.persistent_tools import (
    add_task,
    complete_task,
    list_tasks,
    delete_task,
    set_user_preference,
    get_user_preferences,
    get_storage_summary,
)

root_agent = Agent(
    name="persistent_agent",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="A persistent productivity and configuration agent demonstrating SQLite session storage and state scoping (session, user, app).",
    instruction="""
    You are an organized, persistent workspace assistant named Nexus.
    Your superpower is persistence: you retain session tasks, user preferences, and app-wide metrics
    in a relational SQLite database powered by ADK's DatabaseSessionService.

    Core capabilities:
    1. Session Task Management:
       - When the user asks to add or remember a task: call `add_task(task=..., priority=...)`.
       - When the user asks to view or check tasks: call `list_tasks(status=...)` ('all', 'pending', 'completed').
       - When the user completes or finishes a task: call `complete_task(task_id=...)`.
       - When the user deletes a task: call `delete_task(task_id=...)`.

    2. User Preference Management (Cross-Session):
       - When the user sets a personal preference (e.g. theme, code style, role, tone):
         call `set_user_preference(key=..., value=...)`.
       - When the user asks what you know about them or asks for their preferences:
         call `get_user_preferences()`.
       - Remind the user that these preferences use the `user:` scope, meaning they survive even when starting a brand new conversation!

    3. Storage State Inspection:
       - When the user asks to view stored state, examine scopes, or inspect database storage:
         call `get_storage_summary()`.

    Tone & Formatting:
    - Clear, professional, and structured.
    - Format task lists with status checkboxes (- [ ] for pending, - [x] for completed) and IDs.
    - Highlight state scope awareness (Session vs User vs App) when relevant.
    """,
    tools=[
        add_task,
        complete_task,
        list_tasks,
        delete_task,
        set_user_preference,
        get_user_preferences,
        get_storage_summary,
    ],
)

"""
SQLite Session Runner for Google ADK.

Week 4 — Sessions and State (Project 3.3)

Demonstrates:
1. DatabaseSessionService initialized with a local SQLite database (sqlite+aiosqlite).
2. Resuming existing sessions by session_id across runner lifecycles.
3. State prefix scope isolation & persistence:
   - Session-scoped (no prefix): isolated to a specific session_id.
   - User-scoped ('user:' prefix): preserved across all sessions for that user_id.
   - App-scoped ('app:' prefix): preserved globally across all users for that app_name.
4. Direct inspection of SQLite database tables (sessions, events, user_states, app_states).

Usage:
    # Run the comprehensive multi-turn persistence demonstration:
    python runners/sqlite_session_runner.py --demo

    # Run interactive chat with SQLite persistence:
    python runners/sqlite_session_runner.py --interactive
"""

import argparse
import asyncio
import os
import sqlite3
import sys
from typing import Optional

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from agents.persistent_agent.agent import root_agent

DEFAULT_DB_PATH = "data/sessions.db"
APP_NAME = "persistent_agent_app"


async def run_turn(
    runner: Runner,
    user_id: str,
    session_id: str,
    prompt: str,
    print_events: bool = True,
) -> str:
    """Executes a single conversational turn through the ADK Runner."""
    if print_events:
        print(f"\n💬 User [{user_id}] -> Session [{session_id[:8]}...]: {prompt}")

    new_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt)],
    )

    full_response = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=new_message,
    ):
        # Capture model response text
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    full_response.append(part.text)
                    if print_events:
                        print(f"🤖 [persistent_agent]: {part.text}")

        # Highlight tool calls
        if hasattr(event, "get_function_calls"):
            calls = event.get_function_calls()
            if calls and print_events:
                for call in calls:
                    print(f"   ⚙️  [Tool Call]: {call.name}({call.args})")

        # Highlight state updates if present
        if event.actions and event.actions.state_delta and print_events:
            print(f"   💾 [State Delta]: {event.actions.state_delta}")

    return "".join(full_response)


def inspect_sqlite_database(db_file: str) -> None:
    """Directly inspects the SQLite database tables and prints summaries."""
    print("\n" + "=" * 60)
    print(f"🔍 Direct SQLite Database Inspection: {db_file}")
    print("=" * 60)

    if not os.path.exists(db_file):
        print(f"Database file '{db_file}' does not exist.")
        return

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # 1. Sessions table
    cur.execute("SELECT id, app_name, user_id, state, datetime(update_time, 'unixepoch') FROM sessions;")
    sessions = cur.fetchall()
    print(f"\n📂 Table 'sessions' ({len(sessions)} rows):")
    for s_id, app, user, state, updated in sessions:
        print(f"  • ID: {s_id[:12]}... | User: {user} | App: {app} | Updated: {updated}")
        print(f"    State JSON: {state}")

    # 2. User States table
    cur.execute("SELECT app_name, user_id, state FROM user_states;")
    user_states = cur.fetchall()
    print(f"\n👤 Table 'user_states' ({len(user_states)} rows):")
    for app, user, state in user_states:
        print(f"  • App: {app} | User: {user}")
        print(f"    State JSON: {state}")

    # 3. App States table
    cur.execute("SELECT app_name, state FROM app_states;")
    app_states = cur.fetchall()
    print(f"\n🌐 Table 'app_states' ({len(app_states)} rows):")
    for app, state in app_states:
        print(f"  • App: {app}")
        print(f"    State JSON: {state}")

    # 4. Events table count
    cur.execute("SELECT count(*), count(distinct session_id) FROM events;")
    event_count, distinct_sessions = cur.fetchone()
    print(f"\n📜 Table 'events':")
    print(f"  • Total events stored: {event_count} across {distinct_sessions} session(s)")

    conn.close()
    print("=" * 60 + "\n")


async def run_demo(db_path: str) -> None:
    """Automated demonstration of DatabaseSessionService persistence and scoping."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)

    db_url = f"sqlite+aiosqlite:///{db_path}"
    print("\n🚀 Starting ADK SQLite Persistence Demonstration (Project 3.3)")
    print(f"Database URL: {db_url}")

    # -------------------------------------------------------------
    # PHASE 1: Session 1 for user 'ishan' — Set preferences & tasks
    # -------------------------------------------------------------
    print("\n" + "-" * 55)
    print("🔹 Phase 1: Initialize Session 1 (User: ishan)")
    print("-" * 55)

    service_1 = DatabaseSessionService(db_url=db_url)
    session_1 = await service_1.create_session(app_name=APP_NAME, user_id="ishan")
    session_1_id = session_1.id
    print(f"Created Session 1 ID: {session_1_id}")

    runner_1 = Runner(agent=root_agent, session_service=service_1, app_name=APP_NAME)

    await run_turn(
        runner=runner_1,
        user_id="ishan",
        session_id=session_1_id,
        prompt="Remember my preferred theme as 'Nord' and preferred editor as 'Neovim'.",
    )

    await run_turn(
        runner=runner_1,
        user_id="ishan",
        session_id=session_1_id,
        prompt="Add a high-priority task: 'Ship ADK Week 4 DatabaseSessionService'.",
    )

    # Simulate application exit: close service & dispose engine
    await service_1.close()
    print("\n🛑 [Simulated Restart]: Disposed service connection and exited runner.")

    # -------------------------------------------------------------
    # PHASE 2: Reopen Session 1 on a fresh service instance
    # -------------------------------------------------------------
    print("\n" + "-" * 55)
    print("🔹 Phase 2: Resume Session 1 after simulated restart")
    print("-" * 55)

    service_2 = DatabaseSessionService(db_url=db_url)
    runner_2 = Runner(agent=root_agent, session_service=service_2, app_name=APP_NAME)

    # Reconnect to existing session_1
    resumed_session_1 = await service_2.get_session(
        app_name=APP_NAME, user_id="ishan", session_id=session_1_id
    )
    print(f"Successfully reloaded Session 1 from SQLite: {resumed_session_1.id}")
    print(f"Restored session state keys: {list(resumed_session_1.state.keys())}")

    await run_turn(
        runner=runner_2,
        user_id="ishan",
        session_id=session_1_id,
        prompt="What tasks do I have and what are my saved preferences?",
    )

    await service_2.close()

    # -------------------------------------------------------------
    # PHASE 3: Create Session 2 for the SAME user 'ishan'
    # Demonstrates User Scope ('user:'): preferences persist, tasks reset
    # -------------------------------------------------------------
    print("\n" + "-" * 55)
    print("🔹 Phase 3: Create Session 2 for SAME user (Demonstrating 'user:' scope)")
    print("-" * 55)

    service_3 = DatabaseSessionService(db_url=db_url)
    session_2 = await service_3.create_session(app_name=APP_NAME, user_id="ishan")
    session_2_id = session_2.id
    print(f"Created Session 2 ID: {session_2_id}")

    runner_3 = Runner(agent=root_agent, session_service=service_3, app_name=APP_NAME)

    await run_turn(
        runner=runner_3,
        user_id="ishan",
        session_id=session_2_id,
        prompt="Do you remember my editor and theme? Do I have any tasks in this new session?",
    )

    await service_3.close()

    # -------------------------------------------------------------
    # PHASE 4: Create Session 3 for a DIFFERENT user 'alice'
    # Demonstrates App Scope ('app:'): shared app stats, isolated user prefs
    # -------------------------------------------------------------
    print("\n" + "-" * 55)
    print("🔹 Phase 4: Create Session 3 for a DIFFERENT user 'alice' (App vs User scope)")
    print("-" * 55)

    service_4 = DatabaseSessionService(db_url=db_url)
    session_3 = await service_4.create_session(app_name=APP_NAME, user_id="alice")
    session_3_id = session_3.id
    print(f"Created Session 3 for Alice ID: {session_3_id}")

    runner_4 = Runner(agent=root_agent, session_service=service_4, app_name=APP_NAME)

    await run_turn(
        runner=runner_4,
        user_id="alice",
        session_id=session_3_id,
        prompt="Inspect the storage state summary and tell me the app-wide metrics and my preferences.",
    )

    await service_4.close()

    # -------------------------------------------------------------
    # PHASE 5: Inspect SQLite DB on disk
    # -------------------------------------------------------------
    inspect_sqlite_database(db_path)
    print("✅ ADK SQLite Persistence Demonstration completed successfully!")


async def run_interactive(db_path: str, user_id: str, session_id: Optional[str] = None) -> None:
    """Runs an interactive terminal chat backed by SQLite DatabaseSessionService."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    db_url = f"sqlite+aiosqlite:///{db_path}"

    service = DatabaseSessionService(db_url=db_url)
    await service.prepare_tables()

    if session_id:
        try:
            session = await service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
            print(f"Resumed existing session: {session.id}")
        except Exception:
            print(f"Session {session_id} not found. Creating new session...")
            session = await service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    else:
        session = await service.create_session(app_name=APP_NAME, user_id=user_id)
        print(f"Started new session: {session.id}")

    runner = Runner(agent=root_agent, session_service=service, app_name=APP_NAME)

    print(f"\nPersistent Agent Ready! [User: {user_id} | DB: {db_path}]")
    print("Type your message or 'exit'/'quit' to leave. Type '/status' to inspect DB.\n")

    try:
        while True:
            try:
                user_input = input("You > ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                break
            if user_input == "/status":
                inspect_sqlite_database(db_path)
                continue

            await run_turn(runner, user_id=user_id, session_id=session.id, prompt=user_input)
    finally:
        await service.close()
        print("\nSession saved to SQLite. Goodbye!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Google ADK SQLite DatabaseSessionService Runner")
    parser.add_argument("--demo", action="store_true", help="Run the automated persistence & scoping demo")
    parser.add_argument("--interactive", action="store_true", help="Start an interactive chat session")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help=f"Path to SQLite file (default: {DEFAULT_DB_PATH})")
    parser.add_argument("--user-id", default="default_user", help="User ID for the session")
    parser.add_argument("--session-id", default=None, help="Existing session ID to resume")
    args = parser.parse_args()

    if args.demo:
        asyncio.run(run_demo(args.db_path))
    elif args.interactive:
        asyncio.run(run_interactive(args.db_path, args.user_id, args.session_id))
    else:
        # Default to demo if no specific flag passed
        print("No mode specified. Running --demo by default (use --interactive for chat).")
        asyncio.run(run_demo(args.db_path))


if __name__ == "__main__":
    main()

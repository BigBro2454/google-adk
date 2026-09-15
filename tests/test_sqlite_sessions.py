"""
Unit tests for ADK SQLite DatabaseSessionService and state prefix scoping.

Week 4 — Sessions and State (Project 3.3)
"""

import asyncio
import os
import tempfile
import unittest
from google.adk.events import Event, EventActions
from google.adk.sessions import DatabaseSessionService


class TestSqliteDatabaseSessionService(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_sessions.db")
        self.db_url = f"sqlite+aiosqlite:///{self.db_path}"

    async def asyncTearDown(self):
        self.temp_dir.cleanup()

    async def test_schema_and_session_creation(self):
        service = DatabaseSessionService(db_url=self.db_url)
        await service.prepare_tables()
        
        session = await service.create_session(
            app_name="test_app",
            user_id="user_123",
            session_id="sess_abc",
        )
        self.assertEqual(session.id, "sess_abc")
        self.assertEqual(session.user_id, "user_123")
        self.assertEqual(session.app_name, "test_app")
        await service.close()

    async def test_state_prefix_scoping_and_persistence(self):
        """Tests session, user:, app:, and temp: prefix behavior in SQLite."""
        # 1. Connect and write deltas across all scopes
        service1 = DatabaseSessionService(db_url=self.db_url)
        session1 = await service1.create_session(
            app_name="test_app",
            user_id="alice",
            session_id="alice_session_1",
        )

        event1 = Event(
            author="tool",
            actions=EventActions(
                state_delta={
                    "active_task": "Write documentation",  # session-scoped
                    "user:theme": "catppuccin-mocha",      # user-scoped
                    "app:version": "2.5.0",                # app-scoped
                    "temp:ephemeral_calc": 42,             # transient-scoped
                }
            ),
        )
        await service1.append_event(session1, event1)
        await service1.close()

        # 2. Reopen and verify Session 1 retains session, user, and app state, but NOT temp
        service2 = DatabaseSessionService(db_url=self.db_url)
        reloaded_s1 = await service2.get_session(
            app_name="test_app",
            user_id="alice",
            session_id="alice_session_1",
        )
        self.assertEqual(reloaded_s1.state.get("active_task"), "Write documentation")
        self.assertEqual(reloaded_s1.state.get("user:theme"), "catppuccin-mocha")
        self.assertEqual(reloaded_s1.state.get("app:version"), "2.5.0")
        self.assertNotIn("temp:ephemeral_calc", reloaded_s1.state)

        # 3. Create Session 2 for the SAME user 'alice'
        # user:theme should persist, active_task should NOT (new session)
        session2 = await service2.create_session(
            app_name="test_app",
            user_id="alice",
            session_id="alice_session_2",
        )
        reloaded_s2 = await service2.get_session(
            app_name="test_app",
            user_id="alice",
            session_id="alice_session_2",
        )
        self.assertEqual(reloaded_s2.state.get("user:theme"), "catppuccin-mocha")
        self.assertEqual(reloaded_s2.state.get("app:version"), "2.5.0")
        self.assertNotIn("active_task", reloaded_s2.state)

        # 4. Create Session 3 for a DIFFERENT user 'bob'
        # app:version should persist, user:theme and active_task should NOT
        session3 = await service2.create_session(
            app_name="test_app",
            user_id="bob",
            session_id="bob_session_1",
        )
        reloaded_s3 = await service2.get_session(
            app_name="test_app",
            user_id="bob",
            session_id="bob_session_1",
        )
        self.assertEqual(reloaded_s3.state.get("app:version"), "2.5.0")
        self.assertNotIn("user:theme", reloaded_s3.state)
        self.assertNotIn("active_task", reloaded_s3.state)

        await service2.close()


if __name__ == "__main__":
    unittest.main()

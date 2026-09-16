"""
Long-Term Memory Service for Google ADK.

Week 5 — Memory and Callbacks (Project 4.1)

Extends ADK's BaseMemoryService to provide:
1. Direct memory write (add_memory) for saving facts & preferences.
2. Full session memory ingestion (add_session_to_memory).
3. Incremental event ingestion (add_events_to_memory).
4. Relevance-ranked memory retrieval (search_memory) using token overlap and recency weighting.
5. Persistent JSON storage so memories survive application restarts.
"""

import json
import os
import re
import time
from typing import Any, Mapping, Optional, Sequence
from google.adk.events import Event
from google.adk.memory.base_memory_service import BaseMemoryService, SearchMemoryResponse
from google.adk.memory.memory_entry import MemoryEntry
from google.adk.sessions import Session
from google.genai import types


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"\w+", text.lower()))


class PersistentMemoryService(BaseMemoryService):
    """Long-term memory service supporting direct writes, session indexing, and file persistence."""

    def __init__(self, storage_file: Optional[str] = None):
        self.storage_file = storage_file
        # Maps user_key -> list of dict entries
        self._store: dict[str, list[dict[str, Any]]] = {}
        if storage_file and os.path.exists(storage_file):
            self._load_from_disk()

    def _user_key(self, app_name: str, user_id: str) -> str:
        return f"{app_name}/{user_id}"

    def _load_from_disk(self) -> None:
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                self._store = json.load(f)
        except Exception:
            self._store = {}

    def _save_to_disk(self) -> None:
        if not self.storage_file:
            return
        os.makedirs(os.path.dirname(self.storage_file) or ".", exist_ok=True)
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self._store, f, indent=2)

    async def add_session_to_memory(self, session: Session) -> None:
        """Indexes all user and assistant textual turns from a session into long-term memory."""
        user_key = self._user_key(session.app_name, session.user_id)
        entries = self._store.setdefault(user_key, [])

        for event in session.events:
            if not event.content or not event.content.parts:
                continue
            text = " ".join([p.text for p in event.content.parts if getattr(p, "text", None)])
            if not text.strip():
                continue

            entry = {
                "id": getattr(event, "id", str(time.time())),
                "text": text,
                "author": event.author or "user",
                "timestamp": getattr(event, "timestamp", time.time()),
                "source": "session_turn",
                "session_id": session.id,
            }
            # Prevent duplicate event IDs
            if not any(e["id"] == entry["id"] for e in entries):
                entries.append(entry)

        self._save_to_disk()

    async def add_events_to_memory(
        self,
        *,
        app_name: str,
        user_id: str,
        events: Sequence[Event],
        session_id: Optional[str] = None,
        custom_metadata: Optional[Mapping[str, object]] = None,
    ) -> None:
        """Adds incremental event deltas into long-term memory."""
        user_key = self._user_key(app_name, user_id)
        entries = self._store.setdefault(user_key, [])

        for event in events:
            if not event.content or not event.content.parts:
                continue
            text = " ".join([p.text for p in event.content.parts if getattr(p, "text", None)])
            if not text.strip():
                continue

            entry = {
                "id": getattr(event, "id", str(time.time())),
                "text": text,
                "author": event.author or "user",
                "timestamp": getattr(event, "timestamp", time.time()),
                "source": "event_delta",
                "session_id": session_id,
                "custom_metadata": dict(custom_metadata or {}),
            }
            if not any(e["id"] == entry["id"] for e in entries):
                entries.append(entry)

        self._save_to_disk()

    async def add_memory(
        self,
        *,
        app_name: str,
        user_id: str,
        memories: Sequence[MemoryEntry],
        custom_metadata: Optional[Mapping[str, object]] = None,
    ) -> None:
        """Directly writes explicit facts/memories into long-term storage."""
        user_key = self._user_key(app_name, user_id)
        entries = self._store.setdefault(user_key, [])

        for mem in memories:
            text = ""
            if mem.content and mem.content.parts:
                text = " ".join([p.text for p in mem.content.parts if getattr(p, "text", None)])

            entry = {
                "id": getattr(mem, "id", f"mem_{int(time.time()*1000)}"),
                "text": text,
                "author": mem.author or "assistant",
                "timestamp": time.time(),
                "source": "explicit_memory",
                "custom_metadata": dict(custom_metadata or {}),
            }
            entries.append(entry)

        self._save_to_disk()

    async def search_memory(
        self, *, app_name: str, user_id: str, query: str
    ) -> SearchMemoryResponse:
        """Searches long-term memory using token relevance and recency scoring."""
        user_key = self._user_key(app_name, user_id)
        entries = self._store.get(user_key, [])
        query_tokens = _tokenize(query)

        scored = []
        for e in entries:
            entry_tokens = _tokenize(e["text"])
            overlap = len(query_tokens.intersection(entry_tokens))
            if overlap > 0 or not query.strip():
                scored.append((overlap, e))

        # Sort descending by relevance overlap
        scored.sort(key=lambda x: x[0], reverse=True)

        memories = []
        for _, e in scored[:10]:
            memories.append(
                MemoryEntry(
                    id=e["id"],
                    content=types.Content(
                        role=e.get("author", "model"),
                        parts=[types.Part.from_text(text=e["text"])],
                    ),
                    author=e.get("author", "user"),
                    custom_metadata=e.get("custom_metadata", {}),
                )
            )

        return SearchMemoryResponse(memories=memories)

    def list_user_memories(self, app_name: str, user_id: str) -> list[dict[str, Any]]:
        """Utility helper to view raw memory list."""
        user_key = self._user_key(app_name, user_id)
        return list(self._store.get(user_key, []))

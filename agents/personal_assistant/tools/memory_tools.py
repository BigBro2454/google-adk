"""
Long-term memory tools for personal_assistant.

Week 5 — Memory and Callbacks (Project 4.1)

Enables an agent to store and retrieve explicit memories that survive across
separate conversations and sessions using PersistentMemoryService.
"""

import asyncio
from typing import Any, Optional
from google.adk.tools import ToolContext
from google.adk.memory.memory_entry import MemoryEntry
from google.genai import types
from shared.utils.persistent_memory import PersistentMemoryService

# Shared global memory service instance (pointing to data/memories.json)
MEMORY_SERVICE = PersistentMemoryService(storage_file="data/memories.json")
APP_NAME = "personal_assistant_app"


def remember_fact(fact: str, category: str = "general", tool_context: ToolContext = None) -> dict[str, Any]:
    """Stores a long-term fact or preference about the user into persistent memory.

    Args:
        fact: The statement, preference, or fact to remember (e.g. 'I prefer TypeScript over Java').
        category: Category classification ('preference', 'work', 'personal', 'project').
        tool_context: Injected by ADK.

    Returns:
        Confirmation dictionary with memory ID and category.
    """
    user_id = "default_user"
    # Create MemoryEntry
    entry = MemoryEntry(
        content=types.Content(parts=[types.Part.from_text(text=fact)]),
        custom_metadata={"category": category},
        author="user",
    )

    # Ingest into PersistentMemoryService
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Schedule in current running loop
        asyncio.create_task(
            MEMORY_SERVICE.add_memory(
                app_name=APP_NAME,
                user_id=user_id,
                memories=[entry],
                custom_metadata={"category": category},
            )
        )
    else:
        loop.run_until_complete(
            MEMORY_SERVICE.add_memory(
                app_name=APP_NAME,
                user_id=user_id,
                memories=[entry],
                custom_metadata={"category": category},
            )
        )

    return {
        "status": "success",
        "message": f"Saved to long-term memory: '{fact}'",
        "category": category,
    }


def recall_memories(query: str, tool_context: ToolContext = None) -> dict[str, Any]:
    """Searches long-term memory for relevant memories matching a query.

    Args:
        query: Keywords or concept to search for in long-term memory.
        tool_context: Injected by ADK.

    Returns:
        Dictionary containing matched memory entries.
    """
    user_id = "default_user"
    raw_memories = MEMORY_SERVICE.list_user_memories(app_name=APP_NAME, user_id=user_id)
    query_words = set(query.lower().split())

    matches = []
    for mem in raw_memories:
        mem_words = set(mem["text"].lower().split())
        if query_words.intersection(mem_words) or not query.strip():
            matches.append({
                "fact": mem["text"],
                "category": mem.get("custom_metadata", {}).get("category", "general"),
                "timestamp": mem["timestamp"],
            })

    return {
        "status": "success",
        "query": query,
        "count": len(matches),
        "memories": matches,
    }


def list_all_memories(tool_context: ToolContext = None) -> dict[str, Any]:
    """Retrieves all facts stored in long-term memory for the active user.

    Args:
        tool_context: Injected by ADK.

    Returns:
        Dictionary with all saved long-term memories.
    """
    user_id = "default_user"
    memories = MEMORY_SERVICE.list_user_memories(app_name=APP_NAME, user_id=user_id)
    return {
        "status": "success",
        "total_memories": len(memories),
        "memories": [
            {
                "fact": m["text"],
                "category": m.get("custom_metadata", {}).get("category", "general"),
            }
            for m in memories
        ],
    }

"""
Persistent state tools demonstrating ADK session and prefix scoping.

Week 4 — Sessions and State (Project 3.3)

State Scoping Architecture:
    1. Session-Scoped (no prefix):
       - Lives only within this conversation session.
       - Stored in SQLite 'sessions' table under 'state' column.
       - Example: session.state["tasks"]

    2. User-Scoped ('user:' prefix):
       - Persists across ALL sessions belonging to this user_id.
       - Stored in SQLite 'user_states' table.
       - Example: session.state["user:preferences"], session.state["user:profile"]

    3. App-Scoped ('app:' prefix):
       - Persists globally across ALL users and ALL sessions for this app_name.
       - Stored in SQLite 'app_states' table.
       - Example: session.state["app:system_stats"]

    4. Transient-Scoped ('temp:' prefix):
       - Discarded by ADK before persisting to SQLite. Lives only within the turn.
"""

from typing import Any
import uuid
from google.adk.tools import ToolContext


def add_task(task: str, priority: str = "medium", tool_context: ToolContext = None) -> dict[str, Any]:
    """Adds a new task to the current session's persistent task list.

    Args:
        task: Description of the task or action item.
        priority: Task priority ('low', 'medium', 'high', 'urgent').
        tool_context: Injected by ADK to access persistent state.

    Returns:
        Confirmation dictionary with created task details and total count.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    # Defensive copy of session-scoped tasks
    tasks = dict(tool_context.state.get("tasks", {}))
    task_id = f"task_{len(tasks) + 1}_{str(uuid.uuid4())[:4]}"
    
    tasks[task_id] = {
        "id": task_id,
        "description": task,
        "priority": priority.lower(),
        "completed": False,
    }
    tool_context.state["tasks"] = tasks

    # Update app-scoped global task counter
    stats = dict(tool_context.state.get("app:stats", {}))
    stats["total_tasks_created"] = stats.get("total_tasks_created", 0) + 1
    tool_context.state["app:stats"] = stats

    return {
        "status": "success",
        "message": f"Added task '{task}' (ID: {task_id}, Priority: {priority}).",
        "task_id": task_id,
        "total_active_tasks": len([t for t in tasks.values() if not t["completed"]]),
    }


def complete_task(task_id: str, tool_context: ToolContext = None) -> dict[str, Any]:
    """Marks a task as completed in the current session state.

    Args:
        task_id: The identifier of the task to complete.
        tool_context: Injected by ADK to access persistent state.

    Returns:
        Dictionary indicating status and updated task information.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    tasks = dict(tool_context.state.get("tasks", {}))
    if task_id not in tasks:
        return {
            "status": "error",
            "message": f"Task '{task_id}' not found.",
            "available_task_ids": list(tasks.keys()),
        }

    tasks[task_id] = dict(tasks[task_id])
    tasks[task_id]["completed"] = True
    tool_context.state["tasks"] = tasks

    # Update app-scoped completed tasks metric
    stats = dict(tool_context.state.get("app:stats", {}))
    stats["total_tasks_completed"] = stats.get("total_tasks_completed", 0) + 1
    tool_context.state["app:stats"] = stats

    return {
        "status": "success",
        "message": f"Marked task '{task_id}' as completed.",
        "task": tasks[task_id],
    }


def list_tasks(status: str = "all", tool_context: ToolContext = None) -> dict[str, Any]:
    """Lists tasks for this session, optionally filtered by completion status.

    Args:
        status: Filter criteria: 'all', 'pending', or 'completed'.
        tool_context: Injected by ADK to access persistent state.

    Returns:
        Dictionary with list of matching tasks and summary counts.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    tasks = dict(tool_context.state.get("tasks", {}))
    task_list = list(tasks.values())

    if status.lower() == "pending":
        filtered = [t for t in task_list if not t["completed"]]
    elif status.lower() == "completed":
        filtered = [t for t in task_list if t["completed"]]
    else:
        filtered = task_list

    return {
        "status": "success",
        "filter": status,
        "count": len(filtered),
        "total_tasks": len(tasks),
        "tasks": filtered,
    }


def delete_task(task_id: str, tool_context: ToolContext = None) -> dict[str, Any]:
    """Deletes a task from the session.

    Args:
        task_id: The ID of the task to delete.
        tool_context: Injected by ADK to access persistent state.

    Returns:
        Dictionary confirming deletion.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    tasks = dict(tool_context.state.get("tasks", {}))
    if task_id not in tasks:
        return {
            "status": "error",
            "message": f"Task '{task_id}' not found.",
            "available_task_ids": list(tasks.keys()),
        }

    del tasks[task_id]
    tool_context.state["tasks"] = tasks
    return {
        "status": "success",
        "message": f"Deleted task '{task_id}'.",
        "remaining_tasks": len(tasks),
    }


def set_user_preference(key: str, value: str, tool_context: ToolContext = None) -> dict[str, Any]:
    """Sets a persistent user preference scoped across all sessions for this user.

    Uses the 'user:' prefix to ensure data is stored in the database's user_states
    table and remains available whenever this user opens new sessions.

    Args:
        key: The preference key (e.g. 'theme', 'preferred_tone', 'editor', 'role').
        value: The setting value (e.g. 'dark', 'concise', 'neovim', 'software engineer').
        tool_context: Injected by ADK.

    Returns:
        Dictionary confirming the updated user-level preference.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    # Defensive copy of user:preferences dictionary
    prefs = dict(tool_context.state.get("user:preferences", {}))
    prefs[key] = value
    tool_context.state["user:preferences"] = prefs

    return {
        "status": "success",
        "scope": "user (persists across all sessions for this user)",
        "updated_key": key,
        "value": value,
        "all_user_preferences": prefs,
    }


def get_user_preferences(tool_context: ToolContext = None) -> dict[str, Any]:
    """Retrieves all preferences stored for the active user across sessions.

    Args:
        tool_context: Injected by ADK.

    Returns:
        Dictionary containing all user-scoped preferences.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    prefs = dict(tool_context.state.get("user:preferences", {}))
    return {
        "status": "success",
        "scope": "user",
        "preferences": prefs,
        "count": len(prefs),
    }


def get_storage_summary(tool_context: ToolContext = None) -> dict[str, Any]:
    """Inspects all state scopes (session, user-scoped, app-scoped) in the persistent store.

    Args:
        tool_context: Injected by ADK.

    Returns:
        Structured breakdown showing session-scoped, user-scoped, and app-scoped keys.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    session_keys = {}
    user_keys = {}
    app_keys = {}

    state_dict = tool_context.state.to_dict() if hasattr(tool_context.state, "to_dict") else dict(tool_context.state)
    for k, v in state_dict.items():
        if k.startswith("user:"):
            user_keys[k] = v
        elif k.startswith("app:"):
            app_keys[k] = v
        elif not k.startswith("temp:"):
            session_keys[k] = v

    return {
        "status": "success",
        "scopes": {
            "session_scoped (reset on new session)": {
                "keys": list(session_keys.keys()),
                "data": session_keys,
            },
            "user_scoped (persists across all sessions for this user)": {
                "keys": list(user_keys.keys()),
                "data": user_keys,
            },
            "app_scoped (persists globally across all users)": {
                "keys": list(app_keys.keys()),
                "data": app_keys,
            },
        },
    }

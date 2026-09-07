"""
Note-taking tools — read and write to session.state.

Key concept: any tool function that accepts a parameter named `tool_context`
of type ToolContext gets it injected automatically by ADK at call time.
The agent never needs to pass it explicitly.

State layout (session-scoped, resets each new conversation):
    session.state["notes"] = {
        "title": "note content",
        ...
    }
"""

from google.adk.tools import ToolContext


def add_note(title: str, content: str, tool_context: ToolContext) -> dict:
    """Saves a new note (or updates an existing one) with the given title and content.

    Args:
        title: A short title or label for the note (e.g. "grocery list", "meeting").
        content: The full text content of the note.
        tool_context: Injected by ADK — provides access to session state.

    Returns:
        A dict with 'message' confirming the note was saved.
    """
    notes: dict = dict(tool_context.state.get("notes", {}))
    action = "Updated" if title in notes else "Saved"
    notes[title] = content
    tool_context.state["notes"] = notes
    return {"message": f"{action} note '{title}'. You now have {len(notes)} note(s)."}


def get_note(title: str, tool_context: ToolContext) -> dict:
    """Retrieves the content of a specific note by its title.

    Args:
        title: The exact title of the note to retrieve.
        tool_context: Injected by ADK — provides access to session state.

    Returns:
        A dict with 'title' and 'content' if found, or 'error' if not found.
    """
    notes: dict = tool_context.state.get("notes", {})
    if title not in notes:
        all_titles = list(notes.keys())
        return {
            "error": f"No note found with title '{title}'.",
            "available_notes": all_titles,
        }
    return {"title": title, "content": notes[title]}


def list_notes(tool_context: ToolContext) -> dict:
    """Lists all saved notes with their titles and a short preview of each.

    Args:
        tool_context: Injected by ADK — provides access to session state.

    Returns:
        A dict with 'count' and 'notes' list (each entry has title + preview).
    """
    notes: dict = tool_context.state.get("notes", {})
    if not notes:
        return {"count": 0, "notes": [], "message": "No notes saved yet."}

    previews = [
        {
            "title": title,
            "preview": content[:80] + ("..." if len(content) > 80 else ""),
        }
        for title, content in notes.items()
    ]
    return {"count": len(notes), "notes": previews}


def delete_note(title: str, tool_context: ToolContext) -> dict:
    """Deletes a specific note by its title.

    Args:
        title: The exact title of the note to delete.
        tool_context: Injected by ADK — provides access to session state.

    Returns:
        A dict confirming deletion, or 'error' if the note was not found.
    """
    notes: dict = dict(tool_context.state.get("notes", {}))
    if title not in notes:
        return {
            "error": f"No note found with title '{title}'.",
            "available_notes": list(notes.keys()),
        }
    del notes[title]
    tool_context.state["notes"] = notes
    return {
        "message": f"Deleted note '{title}'. {len(notes)} note(s) remaining.",
    }


def clear_all_notes(tool_context: ToolContext) -> dict:
    """Deletes ALL saved notes. This cannot be undone.

    Only call this if the user explicitly asks to clear or delete all notes.

    Args:
        tool_context: Injected by ADK — provides access to session state.

    Returns:
        A dict confirming how many notes were cleared.
    """
    notes: dict = tool_context.state.get("notes", {})
    count = len(notes)
    tool_context.state["notes"] = {}
    return {"message": f"Cleared all {count} note(s). Session is now empty."}

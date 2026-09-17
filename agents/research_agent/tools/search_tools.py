"""
Search tools for the search_agent specialist.

Week 6 — Agent-as-a-Tool and Sub-Agents (Project 5.1)
"""

from typing import Any

# Domain knowledge base
KNOWLEDGE_BASE = {
    "gemini": {
        "title": "Google Gemini 2.5 Flash Architecture",
        "content": "Gemini 2.5 Flash is Google's high-efficiency frontier model optimized for speed, long-context window (1M tokens), and multi-modal tool calling at minimal cost.",
    },
    "adk": {
        "title": "Google Agent Development Kit (ADK 2.5.0)",
        "content": "ADK 2.5 provides a Directed Acyclic Graph (DAG) execution engine, native Human-In-The-Loop checkpoints, DatabaseSessionService persistence, and A2A multi-agent protocols.",
    },
    "mcp": {
        "title": "Model Context Protocol (MCP)",
        "content": "MCP is an open standard created by Anthropic allowing LLMs to securely query external datasources and developer platforms via JSON-RPC over stdio or SSE transports.",
    },
    "a2a": {
        "title": "Agent-to-Agent (A2A) Protocol",
        "content": "A2A defines standardized discovery cards (agent.json) and JSON-RPC 1.0 communication allowing autonomous agents to delegate tasks across microservice boundaries.",
    },
}


def search_knowledge_base(query: str) -> dict[str, Any]:
    """Searches the technical knowledge base for concepts, frameworks, and architecture specs.

    Args:
        query: Keywords to look up (e.g., 'gemini', 'adk', 'mcp', 'a2a').

    Returns:
        Dictionary containing matched technical excerpts and sources.
    """
    q = query.lower()
    matches = []
    for key, item in KNOWLEDGE_BASE.items():
        if key in q or any(word in item["content"].lower() for word in q.split()):
            matches.append(item)

    if not matches:
        return {
            "status": "not_found",
            "query": query,
            "message": f"No direct matches found for '{query}'. Available topics: {list(KNOWLEDGE_BASE.keys())}",
        }

    return {
        "status": "success",
        "query": query,
        "results_count": len(matches),
        "results": matches,
    }

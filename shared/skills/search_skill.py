"""
Reusable Search Skill for Google ADK.

Week 8 — ADK Skills and Token Optimization (Project 7.1)
"""

from typing import Any
from .base_skill import BaseSkill


def query_developer_ecosystem(term: str) -> dict[str, Any]:
    """Queries package registries and developer tools for package stats and releases."""
    return {
        "query": term,
        "results": [
            {"name": term, "source": "PyPI", "version": "2.5.0", "downloads_weekly": 125000},
            {"name": term, "source": "npm", "version": "1.8.2", "downloads_weekly": 84000},
        ],
    }


def query_rfc_specifications(topic: str) -> dict[str, Any]:
    """Retrieves standard Internet Engineering Task Force (IETF) and protocol RFC summaries."""
    return {
        "topic": topic,
        "rfcs": [
            {"rfc": 7231, "title": "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content"},
            {"rfc": 8446, "title": "The Transport Layer Security (TLS) Protocol Version 1.3"},
        ],
    }


search_skill = BaseSkill(
    name="developer_search_skill",
    description="Provides deep querying across developer package registries and official protocol specifications.",
    version="2.1.0",
    instructions="""
    When researching software libraries or protocols:
    - Use query_developer_ecosystem to inspect releases and package adoption.
    - Use query_rfc_specifications to verify underlying internet protocols.
    """,
    tools=[query_developer_ecosystem, query_rfc_specifications],
)

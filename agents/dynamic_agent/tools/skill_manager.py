"""
Skill and persona management tools for dynamic_agent.

Week 8 — ADK Skills and Token Optimization (Project 7.2)
"""

from typing import Any
from google.adk.tools import ToolContext
from shared.skills.search_skill import search_skill

AVAILABLE_SKILLS = {
    "search": search_skill,
}

AVAILABLE_ROLES = {
    "developer": "Focus on implementation details, code correctness, API signatures, and performance.",
    "product_manager": "Focus on user value, prioritization, roadmaps, and business metrics.",
    "executive": "Focus on high-level ROI, strategic risks, timeline impact, and bottom-line summaries.",
    "qa_engineer": "Focus on edge cases, boundary testing, failure modes, and test matrices.",
}


def load_skill(skill_name: str, tool_context: ToolContext = None) -> dict[str, Any]:
    """Dynamically loads a specialized skill into the agent's active context.

    Demonstrates progressive disclosure: skill instructions and tools are only
    activated when requested, keeping default base prompts lightweight.

    Args:
        skill_name: Name of the skill to activate (e.g. 'search').
        tool_context: Injected by ADK.

    Returns:
        Dictionary confirming activation and tools loaded.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    s_name = skill_name.lower().strip()
    if s_name not in AVAILABLE_SKILLS:
        return {
            "status": "not_found",
            "message": f"Skill '{skill_name}' not available. Available: {list(AVAILABLE_SKILLS.keys())}",
        }

    skill = AVAILABLE_SKILLS[s_name]
    active_skills = dict(tool_context.state.get("active_skills", {}))
    active_skills[skill.name] = {
        "version": skill.version,
        "instructions": skill.instructions,
    }
    tool_context.state["active_skills"] = active_skills

    return {
        "status": "success",
        "message": f"Skill '{skill.name}' (v{skill.version}) dynamically loaded into prompt context.",
        "active_skills": list(active_skills.keys()),
    }


def switch_persona(role: str, tool_context: ToolContext = None) -> dict[str, Any]:
    """Switches the agent's active instruction persona based on user role.

    Stores the role under 'user:role' so it persists across turns and sessions.

    Args:
        role: Target role persona ('developer', 'product_manager', 'executive', 'qa_engineer').
        tool_context: Injected by ADK.

    Returns:
        Dictionary confirming the updated persona configuration.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    r_key = role.lower().strip()
    if r_key not in AVAILABLE_ROLES:
        return {
            "status": "error",
            "message": f"Unknown role '{role}'. Available roles: {list(AVAILABLE_ROLES.keys())}",
        }

    tool_context.state["user:role"] = r_key
    return {
        "status": "success",
        "message": f"Active persona dynamically switched to '{r_key}'.",
        "role_guidelines": AVAILABLE_ROLES[r_key],
    }


def get_active_configuration(tool_context: ToolContext = None) -> dict[str, Any]:
    """Inspects active persona and loaded progressive disclosure skills.

    Args:
        tool_context: Injected by ADK.

    Returns:
        Structured breakdown of currently active persona and dynamic skills.
    """
    if tool_context is None:
        return {"error": "ToolContext not provided."}

    role = tool_context.state.get("user:role", "developer")
    active_skills = list(tool_context.state.get("active_skills", {}).keys())

    return {
        "status": "success",
        "active_persona": role,
        "persona_description": AVAILABLE_ROLES.get(role, "Default general assistant."),
        "active_skills": active_skills,
        "progressive_disclosure_active": len(active_skills) > 0,
    }

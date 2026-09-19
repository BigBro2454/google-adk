"""
dynamic_agent — Demonstrates ADK Progressive Disclosure and dynamic role loaders.

Week 8 — ADK Skills and Token Optimization (Project 7.2)

Key innovation:
- Monolithic instructions waste thousands of tokens on every turn.
- Progressive disclosure loads a base prompt (~100 tokens), dynamically injecting
  role personas and specialized skill instructions only when relevant.
"""

from typing import Any
from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm
from shared.skills.search_skill import query_developer_ecosystem, query_rfc_specifications
from .tools.skill_manager import load_skill, switch_persona, get_active_configuration, AVAILABLE_ROLES


def dynamic_instruction_builder(context: Any) -> str:
    """Dynamically compiles system instructions based on active session state."""
    base_prompt = (
        "You are an adaptable AI Assistant utilizing Progressive Disclosure.\n"
        "Your default system prompt is minimal to conserve token budget.\n"
        "You can load specialized skills or adjust your persona using tools.\n"
    )

    if context is None or not hasattr(context, "state") or not context.state:
        return base_prompt

    state = context.state
    # 1. Dynamic Role Persona
    role = state.get("user:role")
    if role and role in AVAILABLE_ROLES:
        base_prompt += f"\n### Active Persona: {role.upper()}\n{AVAILABLE_ROLES[role]}\n"

    # 2. Dynamic Progressive Disclosure Skills
    active_skills = state.get("active_skills", {})
    if active_skills:
        base_prompt += "\n### Dynamically Injected Skills:\n"
        for name, data in active_skills.items():
            base_prompt += f"- **{name}** (v{data.get('version', '1.0')}):\n{data.get('instructions', '')}\n"

    return base_prompt


root_agent = Agent(
    name="dynamic_agent",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="An adaptive agent demonstrating progressive disclosure, dynamic instruction injection, and role personas.",
    instruction=dynamic_instruction_builder,
    tools=[
        load_skill,
        switch_persona,
        get_active_configuration,
        query_developer_ecosystem,
        query_rfc_specifications,
    ],
)

"""
Base Skill specification for Google ADK Progressive Disclosure.

Week 8 — ADK Skills and Token Optimization (Project 7.1)

A Skill packages:
- Name and Description
- Version
- Specific tool functions
- Targeted instructions that are injected on-demand instead of inflating the base prompt.
"""

from typing import Any, Callable
from pydantic import BaseModel, Field


class BaseSkill(BaseModel):
    """Encapsulates a modular, reusable capability with tools and progressive disclosure prompt."""

    name: str
    description: str
    version: str = "1.0.0"
    instructions: str
    tools: list[Any] = Field(default_factory=list)

    def get_prompt_fragment(self) -> str:
        """Returns the targeted instruction fragment to inject when this skill is active."""
        return f"\n### Skill: {self.name} (v{self.version})\n{self.description}\n{self.instructions}\n"

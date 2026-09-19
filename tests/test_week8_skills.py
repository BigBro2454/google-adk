"""
Unit tests for Week 8: ADK Skills and Token Optimization.

Covers:
- Project 7.1: Reusable search_skill in shared/skills/
- Project 7.2: dynamic_agent progressive disclosure and dynamic role loading
"""

import unittest
from shared.skills.search_skill import search_skill, query_developer_ecosystem, query_rfc_specifications
from agents.dynamic_agent.agent import root_agent as dynamic_agent, dynamic_instruction_builder
from agents.dynamic_agent.tools.skill_manager import load_skill, switch_persona, get_active_configuration


class TestWeek8SkillsAndOptimization(unittest.IsolatedAsyncioTestCase):

    async def test_reusable_search_skill_packaging(self):
        """Test Project 7.1: modular skill packaging and tool execution."""
        self.assertEqual(search_skill.name, "developer_search_skill")
        self.assertEqual(search_skill.version, "2.1.0")
        self.assertGreaterEqual(len(search_skill.tools), 2)

        # Test skill tools
        dev_res = query_developer_ecosystem("google-adk")
        self.assertEqual(dev_res["query"], "google-adk")
        self.assertGreaterEqual(len(dev_res["results"]), 1)

        rfc_res = query_rfc_specifications("http")
        self.assertEqual(rfc_res["topic"], "http")
        self.assertGreaterEqual(len(rfc_res["rfcs"]), 1)

    async def test_dynamic_instruction_builder_progressive_disclosure(self):
        """Test Project 7.2: dynamic instruction compilation saves tokens by default."""
        class MockEmptyContext:
            state = {}

        # Default prompt is minimal (< 300 chars)
        base_prompt = dynamic_instruction_builder(MockEmptyContext())
        self.assertIn("Progressive Disclosure", base_prompt)
        self.assertNotIn("developer_search_skill", base_prompt)
        self.assertNotIn("EXECUTIVE", base_prompt)

        # Context with active role
        class MockRoleContext:
            state = {"user:role": "executive"}

        role_prompt = dynamic_instruction_builder(MockRoleContext())
        self.assertIn("Active Persona: EXECUTIVE", role_prompt)
        self.assertIn("ROI", role_prompt)

        # Context with dynamically injected skill
        class MockSkillContext:
            state = {
                "user:role": "developer",
                "active_skills": {
                    "developer_search_skill": {
                        "version": "2.1.0",
                        "instructions": "Use query_developer_ecosystem.",
                    }
                },
            }

        skill_prompt = dynamic_instruction_builder(MockSkillContext())
        self.assertIn("Active Persona: DEVELOPER", skill_prompt)
        self.assertIn("**developer_search_skill** (v2.1.0)", skill_prompt)

    async def test_skill_manager_tools(self):
        """Test Project 7.2: load_skill, switch_persona, get_active_configuration."""
        class MockToolContext:
            def __init__(self):
                self.state = {}

        ctx = MockToolContext()

        # Switch persona
        role_res = switch_persona("qa_engineer", tool_context=ctx)
        self.assertEqual(role_res["status"], "success")
        self.assertEqual(ctx.state["user:role"], "qa_engineer")

        # Load skill
        skill_res = load_skill("search", tool_context=ctx)
        self.assertEqual(skill_res["status"], "success")
        self.assertIn("developer_search_skill", ctx.state["active_skills"])

        # Check configuration
        config = get_active_configuration(tool_context=ctx)
        self.assertEqual(config["active_persona"], "qa_engineer")
        self.assertTrue(config["progressive_disclosure_active"])


if __name__ == "__main__":
    unittest.main()

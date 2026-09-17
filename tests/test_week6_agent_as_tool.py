"""
Unit tests for Week 6: Agent-as-a-Tool and Sub-Agents.

Covers:
- Project 5.1: research_agent delegating to search_specialist via AgentTool
- Project 5.2: editorial_director coordinating Generator + Reviewer sub-agents
"""

import unittest
from google.adk.tools import AgentTool
from agents.research_agent.agent import root_agent as research_orchestrator, search_agent_tool
from agents.research_agent.tools.search_tools import search_knowledge_base
from agents.writer_reviewer.agent import root_agent as editorial_director, generator_tool, reviewer_tool


class TestWeek6AgentAsTool(unittest.IsolatedAsyncioTestCase):

    async def test_search_knowledge_base_tool(self):
        """Test Project 5.1 search tool retrieval."""
        res = search_knowledge_base("gemini")
        self.assertEqual(res["status"], "success")
        self.assertGreaterEqual(res["results_count"], 1)
        self.assertIn("Gemini 2.5 Flash", res["results"][0]["title"])

        # Test fallback / missing query
        missing = search_knowledge_base("quantum_computing_xyz")
        self.assertEqual(missing["status"], "not_found")

    async def test_research_orchestrator_agent_as_tool_wiring(self):
        """Test Project 5.1: research_orchestrator has AgentTool wrapping search_agent."""
        self.assertEqual(research_orchestrator.name, "research_orchestrator")
        self.assertIsInstance(search_agent_tool, AgentTool)
        self.assertEqual(search_agent_tool.agent.name, "search_specialist")
        self.assertIn(search_agent_tool, research_orchestrator.tools)

    async def test_writer_reviewer_generator_reviewer_wiring(self):
        """Test Project 5.2: Generator + Reviewer collaborative pipeline wiring."""
        self.assertEqual(editorial_director.name, "editorial_director")
        self.assertIsInstance(generator_tool, AgentTool)
        self.assertIsInstance(reviewer_tool, AgentTool)
        self.assertEqual(generator_tool.agent.name, "blog_generator")
        self.assertEqual(reviewer_tool.agent.name, "blog_reviewer")
        self.assertEqual(len(editorial_director.tools), 2)
        self.assertEqual(len(editorial_director.sub_agents), 2)


if __name__ == "__main__":
    unittest.main()

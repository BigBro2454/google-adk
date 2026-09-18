"""
Unit tests for Week 7: Orchestration Patterns.

Covers:
- Project 6.1: news_pipeline SequentialAgent
- Project 6.2: parallel_researcher ParallelAgent
- Project 6.3: smart_dispatcher Coordinator / Dispatcher routing
"""

import unittest
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.tools import AgentTool

from agents.news_pipeline.agent import root_agent as news_pipeline
from agents.news_pipeline.agent import fetch_news_feed
from agents.parallel_researcher.agent import root_agent as parallel_research_director, parallel_fanout
from agents.parallel_researcher.agent import fetch_github_trends, fetch_arxiv_preprints, fetch_industry_blogs
from agents.smart_dispatcher.agent import root_agent as smart_dispatcher, compute_expression


class TestWeek7Orchestration(unittest.IsolatedAsyncioTestCase):

    async def test_news_pipeline_sequential_topology(self):
        """Test Project 6.1: SequentialAgent pipeline has 3 ordered stages."""
        self.assertIsInstance(news_pipeline, SequentialAgent)
        self.assertEqual(news_pipeline.name, "news_pipeline")
        self.assertEqual(len(news_pipeline.sub_agents), 3)

        stage_names = [agent.name for agent in news_pipeline.sub_agents]
        self.assertEqual(stage_names, ["news_fetcher", "news_summarizer", "news_formatter"])

        # Verify fetch tool execution
        feed = fetch_news_feed("ai")
        self.assertEqual(feed["status"], "success")
        self.assertGreaterEqual(len(feed["articles"]), 1)

    async def test_parallel_researcher_topology(self):
        """Test Project 6.2: ParallelAgent concurrent fanout."""
        self.assertIsInstance(parallel_fanout, ParallelAgent)
        self.assertEqual(parallel_fanout.name, "parallel_research_collector")
        self.assertEqual(len(parallel_fanout.sub_agents), 3)

        branch_names = [b.name for b in parallel_fanout.sub_agents]
        self.assertEqual(branch_names, ["github_researcher", "arxiv_researcher", "industry_researcher"])

        # Verify parallel tool feeds
        gh = fetch_github_trends("adk")
        self.assertEqual(gh["source"], "GitHub")
        arxiv = fetch_arxiv_preprints("agents")
        self.assertEqual(arxiv["source"], "ArXiv")
        blogs = fetch_industry_blogs("gemini")
        self.assertEqual(blogs["source"], "Industry Blogs")

    async def test_smart_dispatcher_routing_setup(self):
        """Test Project 6.3: Coordinator routing to 3 specialist agents."""
        self.assertEqual(smart_dispatcher.name, "smart_dispatcher")
        self.assertEqual(len(smart_dispatcher.sub_agents), 3)

        specialist_names = [s.name for s in smart_dispatcher.sub_agents]
        self.assertIn("code_specialist", specialist_names)
        self.assertIn("research_specialist", specialist_names)
        self.assertIn("math_specialist", specialist_names)

        # Test tool execution
        math_res = compute_expression("15 * 4 + 10")
        self.assertEqual(math_res["status"], "success")
        self.assertEqual(math_res["result"], 70)


if __name__ == "__main__":
    unittest.main()

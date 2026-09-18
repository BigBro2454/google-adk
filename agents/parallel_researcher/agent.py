"""
parallel_researcher — ParallelAgent multi-source concurrent research pipeline.

Week 7 — Orchestration Patterns (Project 6.2)

Architecture:
    Parallel Fanout:
        - github_researcher  (queries open-source repo trends)
        - arxiv_researcher   (queries academic preprint trends)
        - industry_researcher(queries enterprise adoption trends)
    Followed by synthesis merging all three parallel branches into a single briefing.
"""

from google.adk.agents import Agent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.tools import AgentTool
from shared.utils.fallback_model import FallbackLlm


def fetch_github_trends(query: str = "ai agents") -> dict:
    """Retrieves trending open-source repositories for a topic."""
    return {
        "source": "GitHub",
        "topic": query,
        "trends": [
            {"repo": "google/adk-python", "stars": "14.2k", "desc": "Official Google Agent Development Kit"},
            {"repo": "modelcontextprotocol/servers", "stars": "18.5k", "desc": "Reference MCP protocol servers"},
        ],
    }


def fetch_arxiv_preprints(query: str = "ai agents") -> dict:
    """Retrieves recent academic preprint research papers."""
    return {
        "source": "ArXiv",
        "topic": query,
        "papers": [
            {"title": "DAG-Based Multi-Agent Execution in Production", "authors": "Google DeepMind", "year": 2026},
            {"title": "Resilient Failover Mechanisms for Large Language Models", "authors": "AI Systems Lab", "year": 2026},
        ],
    }


def fetch_industry_blogs(query: str = "ai agents") -> dict:
    """Retrieves enterprise blog and industry engineering perspectives."""
    return {
        "source": "Industry Blogs",
        "topic": query,
        "posts": [
            {"publication": "Google Cloud Blog", "headline": "Enterprise Agentic Workflows with Gemini 2.5"},
            {"publication": "ACM Queue", "headline": "Why A2A Protocols Matter for Autonomous Microservices"},
        ],
    }


# Branch 1: GitHub Researcher
github_researcher = Agent(
    name="github_researcher",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Researches trending open-source repositories.",
    instruction="Call fetch_github_trends and summarize repository activity.",
    tools=[fetch_github_trends],
)

# Branch 2: ArXiv Researcher
arxiv_researcher = Agent(
    name="arxiv_researcher",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Researches academic papers on ArXiv.",
    instruction="Call fetch_arxiv_preprints and summarize academic findings.",
    tools=[fetch_arxiv_preprints],
)

# Branch 3: Industry Researcher
industry_researcher = Agent(
    name="industry_researcher",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Researches enterprise industry engineering blogs.",
    instruction="Call fetch_industry_blogs and summarize enterprise adoption.",
    tools=[fetch_industry_blogs],
)

# Concurrent Parallel Fanout
parallel_fanout = ParallelAgent(
    name="parallel_research_collector",
    description="Executes concurrent multi-source research across GitHub, ArXiv, and Industry blogs.",
    sub_agents=[github_researcher, arxiv_researcher, industry_researcher],
)

parallel_tool = AgentTool(agent=parallel_fanout)

# Orchestrator synthesizing parallel results
root_agent = Agent(
    name="parallel_research_director",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Orchestrates parallel research fanout across 3 simultaneous sources and synthesizes a unified briefing.",
    instruction="""
    You are the Lead Research Synthesizer.
    When asked to research a topic:
    1. Delegate to your `parallel_research_collector` tool to query GitHub, ArXiv, and Industry blogs concurrently.
    2. Synthesize the findings from all three simultaneous sources into a comprehensive 3-pillar intelligence report.
    """,
    tools=[parallel_tool],
    sub_agents=[parallel_fanout],
)

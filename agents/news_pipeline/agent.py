"""
news_pipeline — Sequential Agent pipeline for tech news processing.

Week 7 — Orchestration Patterns (Project 6.1)

Pipeline:
    Step 1: news_fetcher    — Fetches raw technology news updates.
    Step 2: news_summarizer — Distills key architectural takeaways.
    Step 3: news_formatter  — Formats into an executive markdown bulletin.
"""

from google.adk.agents import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from shared.utils.fallback_model import FallbackLlm


def fetch_news_feed(topic: str = "ai") -> dict:
    """Simulates querying a live tech news wire for top stories."""
    return {
        "status": "success",
        "topic": topic,
        "articles": [
            {
                "title": "Google ADK 2.5 GA Released",
                "summary": "Google releases ADK 2.5 with native DAG workflow runtime, A2A protocols, and DatabaseSessionService.",
            },
            {
                "title": "Anthropic Model Context Protocol Surges",
                "summary": "Enterprise adoption of the Model Context Protocol (MCP) expands across developer platforms.",
            },
            {
                "title": "Local LLM Inference on Apple Silicon",
                "summary": "High-throughput Ollama execution of Qwen 2.5 and Gemma 4 achieves sub-50ms token latency.",
            },
        ],
    }


# Stage 1: Fetcher
fetcher_agent = Agent(
    name="news_fetcher",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Fetches raw tech news feeds.",
    instruction="""
    You are Stage 1 of the news pipeline.
    Call `fetch_news_feed()` to retrieve today's top stories and output the raw headlines and article contents clearly.
    """,
    tools=[fetch_news_feed],
)

# Stage 2: Summarizer
summarizer_agent = Agent(
    name="news_summarizer",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Summarizes tech news articles.",
    instruction="""
    You are Stage 2 of the news pipeline.
    Analyze the raw tech news output from Stage 1.
    Extract the key 2-3 strategic takeaways, impact on AI engineering, and technical significance.
    """,
    tools=[],
)

# Stage 3: Formatter
formatter_agent = Agent(
    name="news_formatter",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Formats news into a clean markdown executive bulletin.",
    instruction="""
    You are Stage 3 of the news pipeline.
    Take the summarized technical takeaways from Stage 2 and format them into an executive daily briefing with:
    # 📰 Daily Tech & AI Briefing
    - Bullet points with bold titles
    - Technical impact callouts
    - A 1-sentence 'What to watch next' closing note.
    """,
    tools=[],
)

root_agent = SequentialAgent(
    name="news_pipeline",
    description="Sequential three-stage news pipeline: Fetch -> Summarize -> Format.",
    sub_agents=[fetcher_agent, summarizer_agent, formatter_agent],
)

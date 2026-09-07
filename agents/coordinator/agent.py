import os
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from shared.utils.fallback_model import FallbackLlm

worker_a2a_agent = RemoteA2aAgent(
    name="worker_a2a",
    agent_card=os.path.join(os.path.dirname(__file__), "../worker/agent.json"),
    description="A remote worker agent capable of executing background tasks.",
)

root_agent = Agent(
    name="coordinator",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="A coordinator agent that delegates tasks to a remote A2A worker.",
    instruction="""
    You are the coordinator. When a user asks you to perform a task that requires
    background work, delegate the task to your `worker_a2a` tool.
    """,
    sub_agents=[worker_a2a_agent],
)

"""
ollama_agent — Runs 100% locally using Ollama. No Google API key needed.

This agent is your fallback when:
  - Google API rate limits are hit
  - You want to work offline
  - You want zero cost / zero latency inference
  - You want privacy (data never leaves your Mac Mini)

How it works:
  ADK Agent → LiteLlm (translation layer) → Ollama (localhost:11434) → Local Model

Models already on your machine (ollama list):
  qwen2.5:7b       4.7 GB  ← best tool calling, recommended
  llama3.1:8b      4.9 GB  ← great general purpose
  qwen2.5-coder:7b 4.7 GB  ← best for coding tasks
  qwen3.5:9b       6.6 GB  ← most capable
  gemma4:12b       7.6 GB  ← Google's own model, locally

Swap the MODEL constant below to switch models instantly.
"""

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from agents.hello_world.tools.calculator import add, subtract, multiply

# ── Change this one line to switch local models ──────────────────────────────
MODEL = "ollama_chat/qwen2.5:7b"       # best tool-calling support
# MODEL = "ollama_chat/llama3.1:8b"    # great general purpose
# MODEL = "ollama_chat/qwen3.5:9b"     # most capable, slower
# MODEL = "ollama_chat/qwen2.5-coder:7b" # best for code tasks
# ─────────────────────────────────────────────────────────────────────────────

# Tell LiteLLM where Ollama is running
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"

root_agent = Agent(
    name="ollama_agent",
    model=LiteLlm(model=MODEL),        # ← the only difference from a Gemini agent
    description=(
        "A fully local agent powered by Ollama. "
        "No internet required. No API limits. Runs on your Mac Mini."
    ),
    instruction="""
    You are a helpful local assistant running entirely on the user's machine.
    You have access to calculator tools for arithmetic.
    Be honest that you are a local model (qwen2.5) rather than Gemini.
    Be concise and helpful.
    """,
    tools=[add, subtract, multiply],
)

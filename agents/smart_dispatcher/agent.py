"""
smart_dispatcher — Coordinator & Dispatcher routing pattern.

Week 7 — Orchestration Patterns (Project 6.3)

Architecture:
    A high-level Coordinator Agent that classifies user intent and routes tasks
    dynamically to one of 3 domain specialist agents:
    - code_specialist
    - research_specialist
    - math_specialist
"""

from google.adk.agents import Agent
from google.adk.tools import AgentTool
from shared.utils.fallback_model import FallbackLlm


# Specialist 1: Code Specialist
def execute_python_snippet(code: str) -> dict:
    """Simulates syntax and execution analysis on Python code."""
    return {"status": "success", "language": "python", "syntax_valid": True, "analysis": "Snippet passes PEP 8."}


code_specialist = Agent(
    name="code_specialist",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Specialist in software engineering, debugging, code generation, and Python idioms.",
    instruction="You are a senior software engineer. Answer coding and syntax questions concisely with production-grade code.",
    tools=[execute_python_snippet],
)

# Specialist 2: Research Specialist
def search_whitepapers(query: str) -> dict:
    """Searches technical whitepapers and specifications."""
    return {"status": "success", "query": query, "papers": ["Google ADK Specification 2.5", "A2A Protocol v1.0"]}


research_specialist = Agent(
    name="research_specialist",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Specialist in system architecture, research synthesis, and conceptual explanations.",
    instruction="You are a principal systems researcher. Explain architectural concepts with depth, trade-offs, and diagrams.",
    tools=[search_whitepapers],
)

# Specialist 3: Math Specialist
def compute_expression(expression: str) -> dict:
    """Evaluates mathematical formulas and expressions."""
    try:
        # Safe eval of numbers and arithmetic operators
        allowed = set("0123456789+-*/(). %")
        if not all(c in allowed for c in expression):
            return {"status": "error", "error": "Invalid mathematical characters."}
        res = eval(expression)
        return {"status": "success", "expression": expression, "result": res}
    except Exception as e:
        return {"status": "error", "error": str(e)}


math_specialist = Agent(
    name="math_specialist",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Specialist in mathematics, formula evaluation, statistics, and numeric calculations.",
    instruction="You are an applied mathematician. Use compute_expression to calculate answers with exact numeric rigor.",
    tools=[compute_expression],
)

# Tools wrapping specialists
code_tool = AgentTool(agent=code_specialist)
research_tool = AgentTool(agent=research_specialist)
math_tool = AgentTool(agent=math_specialist)

# Coordinator / Dispatcher root agent
root_agent = Agent(
    name="smart_dispatcher",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Intelligent coordinator that classifies query intent and dynamically dispatches to code, research, or math specialists.",
    instruction="""
    You are the Chief Coordinator and Request Dispatcher.
    Analyze the incoming user prompt to determine its primary domain:
    - If it's a coding, debugging, or syntax question: Delegate to `code_specialist`.
    - If it's a conceptual, architectural, or research question: Delegate to `research_specialist`.
    - If it's an arithmetic, formula, or calculation question: Delegate to `math_specialist`.

    Synthesize the specialist's response with a concise, professional sign-off.
    """,
    tools=[code_tool, research_tool, math_tool],
    sub_agents=[code_specialist, research_specialist, math_specialist],
)

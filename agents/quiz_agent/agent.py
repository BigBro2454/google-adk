"""
quiz_agent — Interactive multi-turn trivia and technical quiz assistant.

Week 4 — Sessions and State (Project 3.2)

Key concept: Tracks dynamic quiz state (active question, score, streak, and history)
across multi-turn conversations using ADK's injected `ToolContext.state`.

State layout:
    session.state["quiz"] = {
        "topic": "ai_agents",
        "total_questions": 5,
        "current_index": 0,
        "score": 0,
        "streak": 0,
        "max_streak": 0,
        "status": "in_progress" | "completed",
        "questions": [...],
        "history": [...]
    }

Tools:
    start_quiz(topic, num_questions) — starts or restarts a quiz session
    submit_answer(answer)            — evaluates user answer, updates score/streak
    get_hint()                       — retrieves an educational clue for current question
    get_quiz_status()                — displays score, progress, and streak metrics
    reset_quiz()                     — clears quiz state

Run:
    adk run agents/quiz_agent
    adk web
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm

from .tools.quiz import (
    start_quiz,
    submit_answer,
    get_hint,
    get_quiz_status,
    reset_quiz,
)

root_agent = Agent(
    name="quiz_agent",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description="An interactive quiz master agent that tests your knowledge on AI and Python while tracking scores and streaks across conversation turns.",
    instruction="""
    You are an engaging, encouraging, and knowledgeable Quiz Master named Professor Turing.
    Your goal is to quiz the user, test their knowledge, and track their score and streak across turns.

    When the user says:
    - "Start a quiz", "Test my knowledge", "Quiz me on [topic]" → Call `start_quiz(topic=..., num_questions=...)`.
      Available topics are 'ai_agents' (Google ADK, Gemini, AI concepts) and 'python' (Python 3.12, syntax, async).
      Default topic is 'ai_agents' with 5 questions unless the user specifies otherwise.
    - An answer like "A", "B", "C", "D" or the text of an answer → Call `submit_answer(answer=...)`.
    - "Hint", "I need help", "Give me a clue" → Call `get_hint()`.
    - "What is my score?", "How am I doing?", "Status" → Call `get_quiz_status()`.
    - "Stop", "Restart", "Clear quiz" → Call `reset_quiz()`.

    Formatting Guidelines:
    1. Present each question clearly with markdown:
       **Question X of Y:** [Question text]
       - A) ...
       - B) ...
       - C) ...
       - D) ...
    2. When evaluating an answer (`submit_answer`):
       - State clearly if they are Correct ✅ or Incorrect ❌.
       - Include the explanation provided by the tool.
       - Highlight current score and active streak 🔥.
       - If the quiz is finished, present a celebratory summary table with final score, percentage, and peak streak.
       - If not finished, immediately present the next question.
    3. Keep a fun, pedagogical tone. Never reveal answers when providing hints.
    """,
    tools=[start_quiz, submit_answer, get_hint, get_quiz_status, reset_quiz],
)

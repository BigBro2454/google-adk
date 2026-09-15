"""
Quiz tools — read and write quiz state to session.state using ToolContext.

Key concept: ToolContext is injected automatically by ADK at runtime.
State persists across all turns in a single user session.

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
"""

import random
from typing import Dict, List, Optional
from google.adk.tools import ToolContext

# Curated multi-topic question bank for deterministic & offline reliability
QUESTION_BANK: Dict[str, List[dict]] = {
    "ai_agents": [
        {
            "id": 1,
            "question": "Which runtime architecture was introduced in Google ADK 2.0 to replace the hierarchical executor?",
            "options": [
                "A) Directed Acyclic Graph (DAG) runtime",
                "B) Finite State Machine (FSM) runtime",
                "C) Event-Driven Microkernel",
                "D) Recursive Black-Box Dispatcher",
            ],
            "correct_option": "A",
            "hint": "Think about graph execution with nodes and conditional edges.",
            "explanation": "ADK 2.0 replaced the old executor with a Directed Acyclic Graph (DAG) engine, enabling deterministic graph-based multi-agent execution.",
        },
        {
            "id": 2,
            "question": "In Google ADK, how do tool functions access persistent session state?",
            "options": [
                "A) Through a global singleton called ADK_SESSION",
                "B) Via ToolContext injected automatically when declared in function parameters",
                "C) By reading and writing to an external Redis URL in environment variables",
                "D) By subclassing BaseStatefulTool and overriding on_invoke()",
            ],
            "correct_option": "B",
            "hint": "It uses dependency injection based on the parameter signature.",
            "explanation": "ADK inspects function signatures and injects ToolContext automatically at runtime when a parameter named tool_context is present.",
        },
        {
            "id": 3,
            "question": "What does MCP stand for in modern AI tooling architectures?",
            "options": [
                "A) Multi-Core Processing",
                "B) Model Context Protocol",
                "C) Managed Cloud Pipeline",
                "D) Master Control Program",
            ],
            "correct_option": "B",
            "hint": "It is an open standard created for LLMs to interface with tools and data sources.",
            "explanation": "MCP stands for Model Context Protocol, an open standard that allows agents to discover and invoke tools over Stdio or SSE.",
        },
        {
            "id": 4,
            "question": "What state prefix scope in Google ADK allows data to persist across all sessions for a specific user?",
            "options": [
                "A) app:",
                "B) temp:",
                "C) user:",
                "D) persistent:",
            ],
            "correct_option": "C",
            "hint": "The prefix clearly indicates user-level isolation.",
            "explanation": "State keys prefixed with 'user:' persist across all conversations for that user, while 'app:' is shared across all users and 'temp:' lives only for a single turn.",
        },
        {
            "id": 5,
            "question": "In the Agent-to-Agent (A2A) protocol, what document defines an agent's capabilities, skills, and RPC endpoint?",
            "options": [
                "A) Agent Card (agent.json)",
                "B) openapi.yaml",
                "C) agent.proto",
                "D) manifest.xml",
            ],
            "correct_option": "A",
            "hint": "Similar to Model Cards, agents publish an Agent Card in JSON format.",
            "explanation": "The A2A standard uses an Agent Card (typically agent.json) containing metadata, capabilities, authentication requirements, and RPC URLs.",
        },
    ],
    "python": [
        {
            "id": 101,
            "question": "In Python 3.12+, which statement about dictionary mutability when accessing ADK state proxies is TRUE?",
            "options": [
                "A) State proxies can be read-only views; copying before mutation avoids serialization errors",
                "B) Dicts in state are immutable tuples by default",
                "C) State can only store primitive strings and integers",
                "D) You must use pickle.dumps() before updating session.state",
            ],
            "correct_option": "A",
            "hint": "Think about defensive copying: dict(tool_context.state.get(...)).",
            "explanation": "ADK session state items can be exposed as read-only proxies. Creating a shallow copy, modifying it, and reassigning triggers clean persistence.",
        },
        {
            "id": 102,
            "question": "What keyword is used in Python to define an asynchronous generator?",
            "options": [
                "A) async yield",
                "B) yield inside an async def function",
                "C) await yield",
                "D) yield from async",
            ],
            "correct_option": "B",
            "hint": "It combines standard yield with async def coroutine syntax.",
            "explanation": "An asynchronous generator is simply an 'async def' function that contains one or more 'yield' statements.",
        },
        {
            "id": 103,
            "question": "Which built-in Python module is standard for structured runtime dataclasses without boilerplate in Python 3.7+?",
            "options": [
                "A) pydantic",
                "B) dataclasses",
                "C) attr",
                "D) namedtuple",
            ],
            "correct_option": "B",
            "hint": "It is included in Python standard library.",
            "explanation": "The `dataclasses` module provides decorators and functions for automatically generating special methods like __init__() and __repr__().",
        },
    ],
}


def start_quiz(topic: str = "ai_agents", num_questions: int = 5, tool_context: Optional[ToolContext] = None) -> dict:
    """Initializes and starts a new multi-turn quiz on the selected topic.

    Args:
        topic: The quiz topic (options: 'ai_agents', 'python'). Defaults to 'ai_agents'.
        num_questions: Total number of questions to attempt (1 to 5). Defaults to 5.
        tool_context: Injected automatically by ADK — provides session state access.

    Returns:
        A dict containing status, topic, total questions, and the first question with options.
    """
    if not tool_context:
        return {"error": "ToolContext was not provided by runtime."}

    # Normalize topic
    selected_topic = topic.lower().strip()
    if selected_topic not in QUESTION_BANK:
        # Default to ai_agents if topic not found
        selected_topic = "ai_agents"

    available = QUESTION_BANK[selected_topic]
    count = max(1, min(num_questions, len(available)))
    questions = available[:count]

    quiz_state = {
        "topic": selected_topic,
        "total_questions": len(questions),
        "current_index": 0,
        "score": 0,
        "streak": 0,
        "max_streak": 0,
        "status": "in_progress",
        "questions": questions,
        "history": [],
    }

    # Persist cleanly into session state
    tool_context.state["quiz"] = quiz_state

    first_q = questions[0]
    return {
        "status": "in_progress",
        "topic": selected_topic,
        "total_questions": len(questions),
        "current_question_number": 1,
        "question": first_q["question"],
        "options": first_q["options"],
        "message": f"Quiz on '{selected_topic}' started! Here is Question 1 of {len(questions)}.",
    }


def submit_answer(answer: str, tool_context: Optional[ToolContext] = None) -> dict:
    """Submits and evaluates the user's answer for the current active quiz question.

    Args:
        answer: The user's answer (e.g. 'A', 'B', 'C', 'D' or full answer text).
        tool_context: Injected automatically by ADK — provides session state access.

    Returns:
        A dict indicating whether the answer was correct, updated score, streak,
        explanation, and either the next question or the final quiz summary.
    """
    if not tool_context:
        return {"error": "ToolContext was not provided by runtime."}

    # Defensive copy from session state
    quiz: dict = dict(tool_context.state.get("quiz", {}))

    if not quiz or quiz.get("status") != "in_progress":
        return {
            "error": "No active quiz in progress. Call start_quiz() first to begin a quiz.",
            "available_topics": list(QUESTION_BANK.keys()),
        }

    questions: List[dict] = quiz.get("questions", [])
    current_idx: int = quiz.get("current_index", 0)

    if current_idx >= len(questions):
        quiz["status"] = "completed"
        tool_context.state["quiz"] = quiz
        return {"message": "Quiz has already ended.", "score": quiz.get("score", 0)}

    current_q = questions[current_idx]
    correct_opt = current_q["correct_option"].strip().upper()

    # Evaluation logic: match letter (A, B, C, D) or option substring
    clean_ans = answer.strip().upper()
    is_correct = False

    if clean_ans == correct_opt or clean_ans.startswith(f"{correct_opt})") or clean_ans.startswith(f"{correct_opt} "):
        is_correct = True
    else:
        # Check if the text matches the correct option's body
        for opt in current_q["options"]:
            if opt.startswith(f"{correct_opt})"):
                body = opt[2:].strip().upper()
                if body in clean_ans or clean_ans in body:
                    is_correct = True
                    break

    # Update scores and streak
    if is_correct:
        quiz["score"] = quiz.get("score", 0) + 1
        quiz["streak"] = quiz.get("streak", 0) + 1
        quiz["max_streak"] = max(quiz.get("max_streak", 0), quiz["streak"])
    else:
        quiz["streak"] = 0

    # Record history
    quiz.setdefault("history", []).append({
        "question_number": current_idx + 1,
        "question": current_q["question"],
        "user_answer": answer,
        "correct_option": correct_opt,
        "is_correct": is_correct,
        "explanation": current_q["explanation"],
    })

    # Advance index
    current_idx += 1
    quiz["current_index"] = current_idx
    total_q = len(questions)

    # Check if quiz is finished
    if current_idx >= total_q:
        quiz["status"] = "completed"
        final_score = quiz["score"]
        pct = round((final_score / total_q) * 100)
        tool_context.state["quiz"] = quiz

        return {
            "quiz_completed": True,
            "is_correct": is_correct,
            "correct_option": correct_opt,
            "explanation": current_q["explanation"],
            "final_score": f"{final_score}/{total_q}",
            "percentage": f"{pct}%",
            "max_streak": quiz["max_streak"],
            "summary": (
                f"Quiz finished! You scored {final_score} out of {total_q} ({pct}%)."
                + (" Flawless victory! 🏆" if pct == 100 else " Well done! 🎉")
            ),
        }

    # Still in progress — prepare next question
    tool_context.state["quiz"] = quiz
    next_q = questions[current_idx]

    return {
        "quiz_completed": False,
        "is_correct": is_correct,
        "correct_option": correct_opt,
        "explanation": current_q["explanation"],
        "current_score": f"{quiz['score']}/{current_idx}",
        "streak": quiz["streak"],
        "next_question_number": current_idx + 1,
        "total_questions": total_q,
        "next_question": next_q["question"],
        "options": next_q["options"],
    }


def get_hint(tool_context: Optional[ToolContext] = None) -> dict:
    """Provides a pedagogical hint for the current question without revealing the answer.

    Args:
        tool_context: Injected automatically by ADK — provides session state access.

    Returns:
        A dict containing the hint for the active question.
    """
    if not tool_context:
        return {"error": "ToolContext was not provided by runtime."}

    quiz: dict = tool_context.state.get("quiz", {})
    if not quiz or quiz.get("status") != "in_progress":
        return {"error": "No active quiz in progress."}

    questions: List[dict] = quiz.get("questions", [])
    current_idx: int = quiz.get("current_index", 0)

    if current_idx >= len(questions):
        return {"error": "Quiz is already completed."}

    current_q = questions[current_idx]
    return {
        "question_number": current_idx + 1,
        "hint": current_q.get("hint", "Consider the core design principles of the framework."),
    }


def get_quiz_status(tool_context: Optional[ToolContext] = None) -> dict:
    """Retrieves the current progress, score, and streak of the ongoing quiz.

    Args:
        tool_context: Injected automatically by ADK — provides session state access.

    Returns:
        A dict summarizing current score, questions answered, remaining, and streak.
    """
    if not tool_context:
        return {"error": "ToolContext was not provided by runtime."}

    quiz: dict = tool_context.state.get("quiz", {})
    if not quiz:
        return {
            "status": "not_started",
            "message": "No quiz has been started yet in this session.",
            "available_topics": list(QUESTION_BANK.keys()),
        }

    total_q = quiz.get("total_questions", 0)
    current_idx = quiz.get("current_index", 0)
    score = quiz.get("score", 0)
    streak = quiz.get("streak", 0)
    status = quiz.get("status", "in_progress")

    return {
        "status": status,
        "topic": quiz.get("topic", "unknown"),
        "score": f"{score}/{current_idx}",
        "questions_completed": current_idx,
        "total_questions": total_q,
        "streak": streak,
        "max_streak": quiz.get("max_streak", 0),
    }


def reset_quiz(tool_context: Optional[ToolContext] = None) -> dict:
    """Resets or cancels the current quiz session.

    Args:
        tool_context: Injected automatically by ADK — provides session state access.

    Returns:
        A dict confirming the quiz was reset.
    """
    if not tool_context:
        return {"error": "ToolContext was not provided by runtime."}

    tool_context.state["quiz"] = {}
    return {"message": "Quiz session reset successfully. You can start a new quiz anytime."}

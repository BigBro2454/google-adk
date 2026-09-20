"""
agents/hitl_agent/agent.py — Banking & Operations Agent with Human-in-the-Loop (HITL) Governance.

Demonstrates ADK 2.0 Human-in-the-Loop approval workflows:
- Safe queries (view balance, list audit logs) run instantly.
- Sensitive queries (money transfers, account deletions) pause execution and require explicit human confirmation.
"""

from google.adk.agents import Agent
from shared.utils.fallback_model import FallbackLlm
from .tools.approval_tools import (
    view_account_tool,
    list_audit_tool,
    transfer_funds_tool,
    delete_account_tool,
)


root_agent = Agent(
    name="hitl_operations_agent",
    model=FallbackLlm(
        primary="gemini-2.5-flash",
        fallback="ollama_chat/qwen2.5:7b",
    ),
    description=(
        "Banking operations assistant governed by ADK Human-in-the-Loop protocols. "
        "Sensitive financial transfers and data deletions strictly require human approval."
    ),
    instruction="""
    You are an enterprise Banking Operations Assistant.
    You assist customers and staff with account queries, balance checks, fund transfers, and account management.

    POLICIES & SAFETY PROTOCOLS:
    1. Read-only actions (viewing account details or audit logs) are safe and should be executed immediately.
    2. High-impact actions (fund transfers or deleting account records) require explicit human approval.
       When executing these tools, ADK will automatically halt and request human confirmation.
    3. Always explain the details of what action is being requested (e.g. transfer amount, accounts involved, or deletion rationale)
       so the human approver has full context.
    4. If an action is rejected by the human, acknowledge the decision politely and do not attempt to re-run it.
    """,
    tools=[
        view_account_tool,
        list_audit_tool,
        transfer_funds_tool,
        delete_account_tool,
    ],
)

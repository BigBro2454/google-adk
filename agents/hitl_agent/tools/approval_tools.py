"""
agents/hitl_agent/tools/approval_tools.py — Tools demonstrating Human-in-the-Loop approval workflows.

Safe read-only tools execute automatically.
Destructive or sensitive financial operations require explicit human approval via
ADK's native ToolConfirmation mechanism.
"""

from __future__ import annotations

import datetime
from typing import Any

from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext


DEFAULT_ACCOUNTS = {
    "ACC-001": {"owner": "Alice Smith", "balance": 15000.0, "status": "ACTIVE"},
    "ACC-002": {"owner": "Bob Jones", "balance": 4500.0, "status": "ACTIVE"},
    "ACC-999": {"owner": "Test User", "balance": 120.0, "status": "PENDING_TERMINATION"},
}


def _ensure_state(tool_context: ToolContext):
    """Ensures account database and audit trails are initialized in state."""
    state_dict = tool_context.state.to_dict()
    if "accounts" not in state_dict:
        tool_context.state["accounts"] = DEFAULT_ACCOUNTS.copy()
    if "audit_trail" not in state_dict:
        tool_context.state["audit_trail"] = []


def view_account_details(account_id: str, tool_context: ToolContext) -> dict[str, Any]:
    """View details, status, and current balance for a bank account. Safe read-only operation.

    Args:
        account_id: The unique account identifier (e.g. 'ACC-001').
    """
    _ensure_state(tool_context)
    accounts = tool_context.state.get("accounts", DEFAULT_ACCOUNTS)
    if account_id not in accounts:
        return {"error": f"Account '{account_id}' not found."}
    return {
        "account_id": account_id,
        "details": accounts[account_id],
        "status": "SUCCESS",
    }


def list_audit_log(tool_context: ToolContext) -> dict[str, Any]:
    """Retrieve the compliance and security audit log of approved transactions. Safe read-only operation."""
    _ensure_state(tool_context)
    audit = tool_context.state.get("audit_trail", [])
    return {
        "audit_trail": audit,
        "total_events": len(audit),
        "status": "SUCCESS",
    }


def transfer_funds(
    from_account: str,
    to_account: str,
    amount: float,
    tool_context: ToolContext,
) -> dict[str, Any]:
    """Transfer funds between two accounts. REQUIRES HUMAN APPROVAL.

    Args:
        from_account: The sending account identifier.
        to_account: The receiving account identifier.
        amount: Dollar amount to transfer (must be positive).
    """
    _ensure_state(tool_context)
    accounts = dict(tool_context.state.get("accounts", DEFAULT_ACCOUNTS))

    if amount <= 0:
        return {"error": "Transfer amount must be positive."}
    if from_account not in accounts:
        return {"error": f"Source account '{from_account}' does not exist."}
    if to_account not in accounts:
        return {"error": f"Destination account '{to_account}' does not exist."}
    if accounts[from_account]["balance"] < amount:
        return {"error": f"Insufficient funds in '{from_account}'. Available: ${accounts[from_account]['balance']:.2f}"}

    # Execute transfer once approved
    accounts[from_account] = dict(accounts[from_account])
    accounts[to_account] = dict(accounts[to_account])
    accounts[from_account]["balance"] -= amount
    accounts[to_account]["balance"] += amount
    tool_context.state["accounts"] = accounts

    # Record in audit trail
    audit_entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "action": "TRANSFER_FUNDS",
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount,
        "approved_by_human": True,
    }
    audit = list(tool_context.state.get("audit_trail", []))
    audit.append(audit_entry)
    tool_context.state["audit_trail"] = audit

    return {
        "status": "TRANSFERRED",
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount,
        "new_balance": accounts[from_account]["balance"],
    }


def delete_account_records(
    account_id: str,
    reason: str,
    tool_context: ToolContext,
) -> dict[str, Any]:
    """Permanently delete an account and its associated records. IRREVERSIBLE ACTION — REQUIRES HUMAN APPROVAL.

    Args:
        account_id: The account identifier to delete.
        reason: Justification for account deletion.
    """
    _ensure_state(tool_context)
    accounts = dict(tool_context.state.get("accounts", DEFAULT_ACCOUNTS))

    if account_id not in accounts:
        return {"error": f"Account '{account_id}' not found."}

    deleted_account = accounts.pop(account_id)
    tool_context.state["accounts"] = accounts

    # Record in audit trail
    audit_entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "action": "DELETE_ACCOUNT",
        "account_id": account_id,
        "reason": reason,
        "deleted_owner": deleted_account.get("owner"),
        "approved_by_human": True,
    }
    audit = list(tool_context.state.get("audit_trail", []))
    audit.append(audit_entry)
    tool_context.state["audit_trail"] = audit

    return {
        "status": "DELETED",
        "account_id": account_id,
        "reason": reason,
        "message": f"Account {account_id} permanently removed from system.",
    }


# Export wrapped FunctionTools with native ADK confirmation configuration
view_account_tool = FunctionTool(view_account_details, require_confirmation=False)
list_audit_tool = FunctionTool(list_audit_log, require_confirmation=False)
transfer_funds_tool = FunctionTool(transfer_funds, require_confirmation=True)
delete_account_tool = FunctionTool(delete_account_records, require_confirmation=True)

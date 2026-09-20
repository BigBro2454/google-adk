"""
runners/hitl_runner.py — Demonstrates ADK Human-in-the-Loop (HITL) workflows.

Simulates:
1. Read-only operation (account balance check) running automatically without confirmation.
2. High-impact financial transaction requesting human approval.
3. Simulating Human Rejection and demonstrating state preservation.
4. Simulating Human Approval and verifying transaction execution and audit logging.
"""

import asyncio
import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.hitl_agent.agent import root_agent
from agents.hitl_agent.tools.approval_tools import (
    transfer_funds_tool,
    delete_account_tool,
    view_account_tool,
    DEFAULT_ACCOUNTS,
)
from google.adk.runners import InMemoryRunner
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.tool_confirmation import ToolConfirmation
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.agents.invocation_context import InvocationContext
from google.genai import types


async def run_hitl_demo():
    print("=" * 70)
    print("🏦 GOOGLE ADK HUMAN-IN-THE-LOOP (HITL) APPROVAL WORKFLOW DEMO")
    print("=" * 70)

    ss = InMemorySessionService()
    session = await ss.create_session(app_name="banking_app", user_id="compliance_officer")
    session.state["accounts"] = DEFAULT_ACCOUNTS.copy()
    session.state["audit_trail"] = []

    print("\n--- Initial Account Balances ---")
    for acc_id, data in session.state["accounts"].items():
        print(f"  • {acc_id} ({data['owner']}): ${data['balance']:.2f} [{data['status']}]")

    # Step 1: Read-only safe operation
    print("\n[Step 1] Safe Read-Only Action: Checking Account Details...")
    inv_ctx = InvocationContext(
        session=session,
        session_service=ss,
        invocation_id="inv_safe",
        agent=root_agent,
        user_content=None,
    )
    safe_ctx = ToolContext(invocation_context=inv_ctx, function_call_id="fc_view")
    view_res = await view_account_tool.run_async(args={"account_id": "ACC-001"}, tool_context=safe_ctx)
    print(f"  Result: {view_res['status']} -> {view_res['details']['owner']} Balance: ${view_res['details']['balance']:.2f}")
    print("  ✓ Safe tool executed without human confirmation prompt.")

    # Step 2: Unapproved attempt
    print("\n[Step 2] High-Impact Action: Transfer $3,000 from ACC-001 to ACC-002...")
    unconf_ctx = ToolContext(invocation_context=inv_ctx, function_call_id="fc_transfer_1")
    unconf_res = await transfer_funds_tool.run_async(
        args={"from_account": "ACC-001", "to_account": "ACC-002", "amount": 3000.0},
        tool_context=unconf_ctx,
    )
    print(f"  Tool Execution Intercepted: {unconf_res}")
    print(f"  Requested Confirmations: {len(unconf_ctx._event_actions.requested_tool_confirmations)} pending approval(s).")
    print("  ⏸️ Workflow paused pending human supervisor review.")

    # Step 3: Human Rejection
    print("\n[Step 3] Supervisor Decision: REJECT Action (e.g. suspicious activity detected)...")
    reject_ctx = ToolContext(
        invocation_context=inv_ctx,
        function_call_id="fc_transfer_1",
        tool_confirmation=ToolConfirmation(confirmed=False, hint="Flagged for manual compliance audit"),
    )
    reject_res = await transfer_funds_tool.run_async(
        args={"from_account": "ACC-001", "to_account": "ACC-002", "amount": 3000.0},
        tool_context=reject_ctx,
    )
    print(f"  Action Result: {reject_res}")
    print(f"  Account ACC-001 Balance Unchanged: ${session.state['accounts']['ACC-001']['balance']:.2f}")
    print("  🛡️ State protected. Zero funds were moved.")

    # Step 4: Human Approval
    print("\n[Step 4] Supervisor Decision: APPROVE Legitimate Action...")
    approve_ctx = ToolContext(
        invocation_context=inv_ctx,
        function_call_id="fc_transfer_2",
        tool_confirmation=ToolConfirmation(confirmed=True),
    )
    approve_res = await transfer_funds_tool.run_async(
        args={"from_account": "ACC-001", "to_account": "ACC-002", "amount": 3000.0},
        tool_context=approve_ctx,
    )
    print(f"  Action Result: {approve_res}")
    print(f"  New ACC-001 Balance: ${session.state['accounts']['ACC-001']['balance']:.2f}")
    print(f"  New ACC-002 Balance: ${session.state['accounts']['ACC-002']['balance']:.2f}")
    print("  ✅ Transaction executed successfully upon human approval.")

    # Step 5: Destructive Action with Approval (Account Deletion)
    print("\n[Step 5] Destructive Action: Permanent Deletion of ACC-999 with Approval...")
    del_ctx = ToolContext(
        invocation_context=inv_ctx,
        function_call_id="fc_delete",
        tool_confirmation=ToolConfirmation(confirmed=True),
    )
    del_res = await delete_account_tool.run_async(
        args={"account_id": "ACC-999", "reason": "Customer requested account closure under GDPR"},
        tool_context=del_ctx,
    )
    print(f"  Action Result: {del_res}")
    print(f"  ACC-999 Present in database: {'ACC-999' in session.state['accounts']}")

    # Step 6: Audit Trail
    print("\n[Step 6] Compliance Audit Trail Log:")
    for idx, entry in enumerate(session.state["audit_trail"], 1):
        print(f"  {idx}. [{entry['timestamp']}] {entry['action']} — Approved by Human: {entry['approved_by_human']}")

    print("\n" + "=" * 70)
    print("🎯 HITL DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_hitl_demo())

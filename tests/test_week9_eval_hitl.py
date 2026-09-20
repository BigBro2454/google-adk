"""
Unit tests for Week 9: Evaluation Suite, Model Benchmarking, and Human-in-the-Loop (HITL) Workflows.
"""

import asyncio
import os
import unittest

from agents.hitl_agent.tools.approval_tools import (
    DEFAULT_ACCOUNTS,
    delete_account_tool,
    list_audit_tool,
    transfer_funds_tool,
    view_account_tool,
)
from evals.evaluator import AgentTrajectoryEvaluator, CaseEvalResult, EvalSummary
from evals.model_benchmark import ModelBenchmarkResult, ModelBenchmarkRunner
from google.adk.agents import Agent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.tools.tool_confirmation import ToolConfirmation
from google.adk.tools.tool_context import ToolContext


class TestWeek9EvalSuite(unittest.TestCase):
    """Tests for Project 8.1: Agent Evaluation Suite and Trajectory Verifier."""

    def setUp(self):
        self.eval_file = os.path.join(
            os.path.dirname(__file__), "..", "evals", "hello_world.test.json"
        )

    def test_eval_set_loading_and_schema(self):
        """Verifies the 10 evaluation test cases load and match the ADK EvalSet schema."""
        self.assertTrue(os.path.exists(self.eval_file), "hello_world.test.json must exist")
        eval_set = AgentTrajectoryEvaluator.load_eval_set_from_file(self.eval_file)

        self.assertEqual(eval_set.eval_set_id, "hello_world_eval_set")
        self.assertEqual(len(eval_set.eval_cases), 10, "Must contain exactly 10 eval cases")

        # Verify tool distribution in the 10 cases
        tools_expected = []
        for case in eval_set.eval_cases:
            self.assertTrue(case.eval_id.startswith("case_"))
            self.assertIsNotNone(case.conversation)
            inv = case.conversation[0]
            if inv.intermediate_data and hasattr(inv.intermediate_data, "tool_uses"):
                for fc in inv.intermediate_data.tool_uses:
                    tools_expected.append(fc.name)

        self.assertIn("add", tools_expected)
        self.assertIn("subtract", tools_expected)
        self.assertIn("multiply", tools_expected)
        # Verify non-tool queries (e.g. greetings, concept explanations) exist
        self.assertGreaterEqual(len(eval_set.eval_cases) - len(tools_expected), 2)

    def test_eval_summary_metrics_and_markdown(self):
        """Tests that EvalSummary computes metrics and formats Markdown tables correctly."""
        results = [
            CaseEvalResult(
                eval_id="case_1",
                prompt="5 + 3",
                passed=True,
                expected_tools=["add"],
                actual_tools=["add"],
                tool_match=True,
                args_match=True,
                actual_response="8",
                duration_ms=45.0,
            ),
            CaseEvalResult(
                eval_id="case_2",
                prompt="Hi",
                passed=True,
                expected_tools=[],
                actual_tools=[],
                tool_match=True,
                args_match=True,
                actual_response="Hello!",
                duration_ms=25.0,
            ),
            CaseEvalResult(
                eval_id="case_3",
                prompt="10 * 2",
                passed=False,
                expected_tools=["multiply"],
                actual_tools=["add"],
                tool_match=False,
                args_match=False,
                actual_response="12",
                duration_ms=60.0,
            ),
        ]

        summary = EvalSummary(
            eval_set_id="test_suite",
            total_cases=3,
            passed_cases=2,
            failed_cases=1,
            pass_rate=2 / 3,
            tool_selection_accuracy=2 / 3,
            argument_accuracy=2 / 3,
            avg_duration_ms=43.33,
            case_results=results,
        )

        md = summary.to_markdown()
        self.assertIn("# ADK Evaluation Report: `test_suite`", md)
        self.assertIn("Passed:** 2 / 3 (66.7%)", md)
        self.assertIn("✅ PASS", md)
        self.assertIn("❌ FAIL", md)

    def test_model_benchmark_table_formatter(self):
        """Tests ModelBenchmarkRunner comparative table formatting."""
        res_flash = ModelBenchmarkResult(
            model_name="gemini-2.5-flash",
            total_queries=10,
            successful_runs=10,
            tool_accuracy=1.0,
            param_accuracy=1.0,
            avg_latency_ms=320.5,
            min_latency_ms=250.0,
            max_latency_ms=410.0,
        )
        res_ollama = ModelBenchmarkResult(
            model_name="ollama_chat/qwen2.5:7b",
            total_queries=10,
            successful_runs=10,
            tool_accuracy=0.9,
            param_accuracy=0.9,
            avg_latency_ms=1850.2,
            min_latency_ms=1400.0,
            max_latency_ms=2300.0,
        )

        table = ModelBenchmarkRunner.format_comparison_table([res_flash, res_ollama])
        self.assertIn("gemini-2.5-flash", table)
        self.assertIn("ollama_chat/qwen2.5:7b", table)
        self.assertIn("320.5 ms", table)
        self.assertIn("100.0%", table)


class TestWeek9HitlWorkflow(unittest.IsolatedAsyncioTestCase):
    """Tests for Project 8.2: Human-in-the-Loop Approval Workflows."""

    async def asyncSetUp(self):
        self.ss = InMemorySessionService()
        self.session = await self.ss.create_session(app_name="hitl_test", user_id="tester")
        self.session.state["accounts"] = DEFAULT_ACCOUNTS.copy()
        self.session.state["audit_trail"] = []
        self.agent = Agent(name="test_agent")
        self.inv_ctx = InvocationContext(
            session=self.session,
            session_service=self.ss,
            invocation_id="inv_test",
            agent=self.agent,
            user_content=None,
        )

    async def test_safe_tools_execute_without_confirmation(self):
        """Verifies that read-only safe tools do not require or request human confirmation."""
        ctx = ToolContext(invocation_context=self.inv_ctx, function_call_id="fc_view")
        res = await view_account_tool.run_async(args={"account_id": "ACC-001"}, tool_context=ctx)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["details"]["owner"], "Alice Smith")
        self.assertEqual(len(ctx._event_actions.requested_tool_confirmations), 0)

        # Audit log read
        res_audit = await list_audit_tool.run_async(args={}, tool_context=ctx)
        self.assertEqual(res_audit["status"], "SUCCESS")
        self.assertEqual(res_audit["total_events"], 0)

    async def test_transfer_unconfirmed_triggers_confirmation_request(self):
        """Verifies sensitive transfer requests trigger confirmation and pause execution."""
        ctx = ToolContext(invocation_context=self.inv_ctx, function_call_id="fc_transfer")
        res = await transfer_funds_tool.run_async(
            args={"from_account": "ACC-001", "to_account": "ACC-002", "amount": 2500.0},
            tool_context=ctx,
        )
        self.assertIn("error", res)
        self.assertIn("requires confirmation", res["error"])
        self.assertEqual(len(ctx._event_actions.requested_tool_confirmations), 1)

        # Verify state balance remains untouched
        self.assertEqual(self.session.state["accounts"]["ACC-001"]["balance"], 15000.0)

    async def test_transfer_rejected_by_human(self):
        """Verifies supervisor rejection halts the operation without modifying state."""
        ctx = ToolContext(
            invocation_context=self.inv_ctx,
            function_call_id="fc_transfer_rej",
            tool_confirmation=ToolConfirmation(confirmed=False, hint="Suspected fraud"),
        )
        res = await transfer_funds_tool.run_async(
            args={"from_account": "ACC-001", "to_account": "ACC-002", "amount": 2500.0},
            tool_context=ctx,
        )
        self.assertIn("error", res)
        self.assertIn("rejected", res["error"])
        self.assertEqual(self.session.state["accounts"]["ACC-001"]["balance"], 15000.0)
        self.assertEqual(len(self.session.state["audit_trail"]), 0)

    async def test_transfer_approved_by_human(self):
        """Verifies human approval completes the transfer and persists an audit entry."""
        ctx = ToolContext(
            invocation_context=self.inv_ctx,
            function_call_id="fc_transfer_app",
            tool_confirmation=ToolConfirmation(confirmed=True),
        )
        res = await transfer_funds_tool.run_async(
            args={"from_account": "ACC-001", "to_account": "ACC-002", "amount": 2500.0},
            tool_context=ctx,
        )
        self.assertEqual(res["status"], "TRANSFERRED")
        self.assertEqual(self.session.state["accounts"]["ACC-001"]["balance"], 12500.0)
        self.assertEqual(self.session.state["accounts"]["ACC-002"]["balance"], 7000.0)

        # Audit trail must have 1 approved event
        self.assertEqual(len(self.session.state["audit_trail"]), 1)
        self.assertTrue(self.session.state["audit_trail"][0]["approved_by_human"])
        self.assertEqual(self.session.state["audit_trail"][0]["action"], "TRANSFER_FUNDS")

    async def test_delete_account_workflow(self):
        """Verifies destructive account deletion requires confirmation and executes when approved."""
        # Unapproved attempt
        ctx_unapproved = ToolContext(invocation_context=self.inv_ctx, function_call_id="fc_del_1")
        res_unapproved = await delete_account_tool.run_async(
            args={"account_id": "ACC-999", "reason": "Cleanup"},
            tool_context=ctx_unapproved,
        )
        self.assertIn("error", res_unapproved)
        self.assertIn("ACC-999", self.session.state["accounts"])

        # Approved attempt
        ctx_approved = ToolContext(
            invocation_context=self.inv_ctx,
            function_call_id="fc_del_2",
            tool_confirmation=ToolConfirmation(confirmed=True),
        )
        res_approved = await delete_account_tool.run_async(
            args={"account_id": "ACC-999", "reason": "Customer request"},
            tool_context=ctx_approved,
        )
        self.assertEqual(res_approved["status"], "DELETED")
        self.assertNotIn("ACC-999", self.session.state["accounts"])
        self.assertEqual(len(self.session.state["audit_trail"]), 1)
        self.assertEqual(self.session.state["audit_trail"][0]["action"], "DELETE_ACCOUNT")


if __name__ == "__main__":
    unittest.main()

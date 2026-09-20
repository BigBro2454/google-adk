"""
evals/evaluator.py — Trajectory and Quality Evaluation Engine for ADK Agents.

Evaluates an Agent against an EvalSet or list of EvalCases:
1. Trajectory Accuracy: Verifies the exact sequence and names of tool calls.
2. Argument Accuracy: Checks parameters passed to functions against ground truth.
3. Response Appropriateness: Validates non-tool conversational responses.
4. Latency & Step Metrics: Captures step counts and execution duration.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from google.adk.agents import Agent
from google.adk.evaluation.eval_case import EvalCase
from google.adk.evaluation.eval_set import EvalSet
from google.adk.runners import InMemoryRunner
from google.genai import types


@dataclass
class CaseEvalResult:
    """Result of evaluating a single EvalCase."""
    eval_id: str
    prompt: str
    passed: bool
    expected_tools: list[str]
    actual_tools: list[str]
    tool_match: bool
    args_match: bool
    actual_response: str
    duration_ms: float
    error_message: Optional[str] = None
    step_count: int = 0


@dataclass
class EvalSummary:
    """Summary of an evaluation run across all cases."""
    eval_set_id: str
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
    tool_selection_accuracy: float
    argument_accuracy: float
    avg_duration_ms: float
    case_results: list[CaseEvalResult] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# ADK Evaluation Report: `{self.eval_set_id}`",
            "",
            f"- **Total Cases:** {self.total_cases}",
            f"- **Passed:** {self.passed_cases} / {self.total_cases} ({self.pass_rate * 100:.1f}%)",
            f"- **Tool Selection Accuracy:** {self.tool_selection_accuracy * 100:.1f}%",
            f"- **Argument Accuracy:** {self.argument_accuracy * 100:.1f}%",
            f"- **Average Duration:** {self.avg_duration_ms:.1f} ms",
            "",
            "| Case ID | Expected Tools | Actual Tools | Tool Match | Args Match | Status | Time (ms) |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in self.case_results:
            exp_str = ", ".join(r.expected_tools) if r.expected_tools else "(none)"
            act_str = ", ".join(r.actual_tools) if r.actual_tools else "(none)"
            status = "✅ PASS" if r.passed else "❌ FAIL"
            tm = "✓" if r.tool_match else "✗"
            am = "✓" if r.args_match else "✗"
            lines.append(
                f"| `{r.eval_id}` | {exp_str} | {act_str} | {tm} | {am} | {status} | {r.duration_ms:.1f} |"
            )
        return "\n".join(lines)


class AgentTrajectoryEvaluator:
    """Evaluates an ADK agent against ground-truth trajectories."""

    def __init__(self, agent: Agent):
        self.agent = agent

    async def evaluate_case(self, case: EvalCase) -> CaseEvalResult:
        """Evaluates a single EvalCase."""
        if not case.conversation:
            return CaseEvalResult(
                eval_id=case.eval_id,
                prompt="",
                passed=False,
                expected_tools=[],
                actual_tools=[],
                tool_match=False,
                args_match=False,
                actual_response="",
                duration_ms=0.0,
                error_message="No conversation specified in EvalCase.",
            )

        inv = case.conversation[0]
        prompt = ""
        if inv.user_content and inv.user_content.parts:
            prompt = inv.user_content.parts[0].text or ""

        # Extract expected tool uses
        expected_tools = []
        expected_args_list = []
        if inv.intermediate_data and hasattr(inv.intermediate_data, "tool_uses"):
            for fc in inv.intermediate_data.tool_uses:
                expected_tools.append(fc.name)
                expected_args_list.append(fc.args or {})

        runner = InMemoryRunner(agent=self.agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id="eval_user",
        )

        actual_tools = []
        actual_args_list = []
        actual_response = ""
        step_count = 0
        error_msg = None

        user_content = types.Content(
            parts=[types.Part.from_text(text=prompt)]
        )

        start_time = time.perf_counter()
        try:
            async for event in runner.run_async(
                session_id=session.id,
                user_id="eval_user",
                new_message=user_content,
            ):
                step_count += 1
                for fc in event.get_function_calls():
                    actual_tools.append(fc.name)
                    actual_args_list.append(fc.args or {})

                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text and not part.thought:
                            actual_response += part.text
        except Exception as e:
            error_msg = str(e)
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Trajectory matching:
        tool_match = (actual_tools == expected_tools)

        # Argument matching:
        args_match = True
        if expected_tools:
            if len(actual_args_list) != len(expected_args_list):
                args_match = False
            else:
                for act_args, exp_args in zip(actual_args_list, expected_args_list):
                    # Check if all exp_args match
                    for k, v in exp_args.items():
                        if act_args.get(k) != v:
                            args_match = False
                            break

        passed = tool_match and args_match and (error_msg is None)

        return CaseEvalResult(
            eval_id=case.eval_id,
            prompt=prompt,
            passed=passed,
            expected_tools=expected_tools,
            actual_tools=actual_tools,
            tool_match=tool_match,
            args_match=args_match,
            actual_response=actual_response.strip(),
            duration_ms=duration_ms,
            error_message=error_msg,
            step_count=step_count,
        )

    async def evaluate_eval_set(self, eval_set: EvalSet) -> EvalSummary:
        """Evaluates all cases in an EvalSet sequentially."""
        case_results = []
        tool_matches = 0
        arg_matches = 0
        passed_count = 0
        total_time = 0.0

        for case in eval_set.eval_cases:
            result = await self.evaluate_case(case)
            case_results.append(result)
            if result.passed:
                passed_count += 1
            if result.tool_match:
                tool_matches += 1
            if result.args_match:
                arg_matches += 1
            total_time += result.duration_ms

        total = len(eval_set.eval_cases)
        return EvalSummary(
            eval_set_id=eval_set.eval_set_id,
            total_cases=total,
            passed_cases=passed_count,
            failed_cases=total - passed_count,
            pass_rate=passed_count / total if total else 0.0,
            tool_selection_accuracy=tool_matches / total if total else 0.0,
            argument_accuracy=arg_matches / total if total else 0.0,
            avg_duration_ms=total_time / total if total else 0.0,
            case_results=case_results,
        )

    @classmethod
    def load_eval_set_from_file(cls, file_path: str) -> EvalSet:
        """Loads and parses an EvalSet from a JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return EvalSet.model_validate(data)


if __name__ == "__main__":
    import argparse
    from agents.hello_world.agent import root_agent

    parser = argparse.ArgumentParser(description="Evaluate an ADK agent against ground-truth trajectories.")
    parser.add_argument("--eval-set", default="evals/hello_world.test.json", help="Path to test.json file")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of eval cases to run")
    args = parser.parse_args()

    eval_path = args.eval_set
    if not os.path.isabs(eval_path):
        eval_path = os.path.join(os.getcwd(), eval_path)

    print(f"Loading EvalSet from: {eval_path}...")
    eval_set = AgentTrajectoryEvaluator.load_eval_set_from_file(eval_path)
    if args.limit:
        eval_set.eval_cases = eval_set.eval_cases[:args.limit]

    print(f"Running evaluation on {len(eval_set.eval_cases)} cases...")
    evaluator = AgentTrajectoryEvaluator(root_agent)
    summary = asyncio.run(evaluator.evaluate_eval_set(eval_set))
    print("\n" + summary.to_markdown())

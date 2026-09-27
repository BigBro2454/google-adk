"""
Script to generate the 10 evaluation test cases for Project 8.1 in ADK standard format.
"""

import json
import os
from google.adk.evaluation.eval_case import EvalCase, Invocation, IntermediateData
from google.adk.evaluation.eval_set import EvalSet
from google.genai import types


def build_test_cases() -> list[EvalCase]:
    cases_data = [
        {
            "id": "case_01_add_basic",
            "prompt": "What is 15 + 27?",
            "expected_tool": "add",
            "expected_args": {"a": 15, "b": 27},
            "expected_result": 42,
        },
        {
            "id": "case_02_subtract_basic",
            "prompt": "Calculate 100 - 45",
            "expected_tool": "subtract",
            "expected_args": {"a": 100, "b": 45},
            "expected_result": 55,
        },
        {
            "id": "case_03_multiply_basic",
            "prompt": "What is 8 times 9?",
            "expected_tool": "multiply",
            "expected_args": {"a": 8, "b": 9},
            "expected_result": 72,
        },
        {
            "id": "case_04_add_negative",
            "prompt": "What is -12 plus 30?",
            "expected_tool": "add",
            "expected_args": {"a": -12, "b": 30},
            "expected_result": 18,
        },
        {
            "id": "case_05_subtract_negative",
            "prompt": "What is 50 minus -25?",
            "expected_tool": "subtract",
            "expected_args": {"a": 50, "b": -25},
            "expected_result": 75,
        },
        {
            "id": "case_06_multiply_zero",
            "prompt": "Compute 42 multiplied by 0",
            "expected_tool": "multiply",
            "expected_args": {"a": 42, "b": 0},
            "expected_result": 0,
        },
        {
            "id": "case_07_add_zero_identity",
            "prompt": "Add 0 and 73",
            "expected_tool": "add",
            "expected_args": {"a": 0, "b": 73},
            "expected_result": 73,
        },
        {
            "id": "case_08_plain_greeting",
            "prompt": "Hello there! How are you today?",
            "expected_tool": None,
            "expected_args": {},
            "expected_result": None,
        },
        {
            "id": "case_09_concept_explanation",
            "prompt": "What is a prime number in mathematics?",
            "expected_tool": None,
            "expected_args": {},
            "expected_result": None,
        },
        {
            "id": "case_10_multiply_large",
            "prompt": "Can you multiply 125 by 4?",
            "expected_tool": "multiply",
            "expected_args": {"a": 125, "b": 4},
            "expected_result": 500,
        },
    ]

    eval_cases = []
    for c in cases_data:
        tool_uses = []
        tool_responses = []
        if c["expected_tool"]:
            tool_uses.append(
                types.FunctionCall(name=c["expected_tool"], args=c["expected_args"])
            )
            tool_responses.append(
                types.FunctionResponse(
                    name=c["expected_tool"],
                    response={"result": c["expected_result"]},
                )
            )

        inv = Invocation(
            invocation_id=f"inv_{c['id']}",
            user_content=types.Content(
                parts=[types.Part.from_text(text=c["prompt"])]
            ),
            intermediate_data=IntermediateData(
                tool_uses=tool_uses,
                tool_responses=tool_responses,
            ),
        )

        eval_case = EvalCase(
            eval_id=c["id"],
            conversation=[inv],
        )
        eval_cases.append(eval_case)

    return eval_cases


def get_default_eval_set() -> EvalSet:
    """Return default Hello World agent EvalSet."""
    eval_cases = build_test_cases()
    return EvalSet(
        eval_set_id="hello_world_eval_set",
        name="Hello World Agent Evaluation Suite",
        description="10 deterministic trajectory evaluation cases testing arithmetic tools and non-tool queries.",
        eval_cases=eval_cases,
    )


def generate():
    eval_set = get_default_eval_set()
    eval_cases = eval_set.eval_cases

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(out_dir, "hello_world.test.json")

    # Serialize to JSON with proper indent
    data = json.loads(eval_set.model_dump_json(by_alias=True, exclude_none=True))
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully generated {len(eval_cases)} eval cases into {out_file}")


if __name__ == "__main__":
    generate()

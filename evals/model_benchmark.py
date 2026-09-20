"""
evals/model_benchmark.py — Model Benchmark & Comparison Suite.

Benchmarks multiple LLMs (e.g. gemini-2.5-flash, gemini-2.5-flash-lite, ollama_chat/qwen2.5:7b)
on key agentic dimensions:
1. Tool Invocation Accuracy: Did the model call the expected tool?
2. Parameter Accuracy: Did the model extract the correct arguments?
3. Latency: Average round-trip time in milliseconds.
4. Error / Availability Rate: Graceful handling of network, quota, or local delays.
"""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from google.adk.agents import Agent
from google.adk.models.base_llm import BaseLlm
from google.adk.runners import InMemoryRunner
from google.genai import types
from agents.hello_world.tools.calculator import add, multiply, subtract
from shared.utils.fallback_model import FallbackLlm


BENCHMARK_PROMPTS = [
    {
        "prompt": "What is 45 + 55?",
        "expected_tool": "add",
        "expected_args": {"a": 45, "b": 55},
    },
    {
        "prompt": "Subtract 32 from 100",
        "expected_tool": "subtract",
        "expected_args": {"a": 100, "b": 32},
    },
    {
        "prompt": "Multiply 14 by 5",
        "expected_tool": "multiply",
        "expected_args": {"a": 14, "b": 5},
    },
    {
        "prompt": "Hello there! Introduce yourself in one sentence.",
        "expected_tool": None,
        "expected_args": {},
    },
]


@dataclass
class ModelBenchmarkResult:
    """Benchmark results for a single model."""
    model_name: str
    total_queries: int
    successful_runs: int
    tool_accuracy: float
    param_accuracy: float
    avg_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    latencies: list[float] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class ModelBenchmarkRunner:
    """Runs standard agent benchmarks across multiple LLM configurations."""

    def __init__(self, models: list[str | BaseLlm]):
        self.models = models

    async def benchmark_model(
        self, model_spec: str | BaseLlm, prompts: list[dict[str, Any]] = BENCHMARK_PROMPTS
    ) -> ModelBenchmarkResult:
        model_name = getattr(model_spec, "model_name", str(model_spec))
        if isinstance(model_spec, FallbackLlm):
            model_name = f"Fallback({model_spec.primary_model_name} -> {model_spec.fallback_model_name})"

        agent = Agent(
            name="benchmark_agent",
            model=model_spec,
            instruction="You are a math helper. Use calculator tools for math calculations.",
            tools=[add, subtract, multiply],
        )

        runner = InMemoryRunner(agent=agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id="bench_user",
        )

        latencies = []
        tool_matches = 0
        param_matches = 0
        successful_runs = 0
        errors = []

        for p in prompts:
            prompt_text = p["prompt"]
            expected_tool = p["expected_tool"]
            expected_args = p["expected_args"]

            actual_tools = []
            actual_args_list = []
            start = time.perf_counter()
            try:
                user_msg = types.Content(parts=[types.Part.from_text(text=prompt_text)])
                async for event in runner.run_async(
                    session_id=session.id,
                    user_id="bench_user",
                    new_message=user_msg,
                ):
                    for fc in event.get_function_calls():
                        actual_tools.append(fc.name)
                        actual_args_list.append(fc.args or {})
                duration = (time.perf_counter() - start) * 1000
                latencies.append(duration)
                successful_runs += 1

                # Check tool selection
                expected_list = [expected_tool] if expected_tool else []
                if actual_tools == expected_list:
                    tool_matches += 1

                # Check arguments
                if expected_tool:
                    if actual_args_list and all(
                        actual_args_list[0].get(k) == v for k, v in expected_args.items()
                    ):
                        param_matches += 1
                else:
                    if not actual_tools:
                        param_matches += 1
            except Exception as e:
                duration = (time.perf_counter() - start) * 1000
                latencies.append(duration)
                errors.append(f"{prompt_text}: {str(e)}")

        total = len(prompts)
        avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
        min_lat = min(latencies) if latencies else 0.0
        max_lat = max(latencies) if latencies else 0.0

        return ModelBenchmarkResult(
            model_name=model_name,
            total_queries=total,
            successful_runs=successful_runs,
            tool_accuracy=tool_matches / total if total else 0.0,
            param_accuracy=param_matches / total if total else 0.0,
            avg_latency_ms=avg_lat,
            min_latency_ms=min_lat,
            max_latency_ms=max_lat,
            latencies=latencies,
            errors=errors,
        )

    async def run_all(
        self, prompts: list[dict[str, Any]] = BENCHMARK_PROMPTS
    ) -> list[ModelBenchmarkResult]:
        results = []
        for m in self.models:
            res = await self.benchmark_model(m, prompts=prompts)
            results.append(res)
        return results

    @staticmethod
    def format_comparison_table(results: list[ModelBenchmarkResult]) -> str:
        lines = [
            "# Model Benchmark Comparison",
            "",
            "| Model Architecture | Avg Latency (ms) | Min / Max Latency | Tool Accuracy | Param Accuracy | Success Rate |",
            "|---|---|---|---|---|---|",
        ]
        for r in results:
            succ = f"{r.successful_runs}/{r.total_queries}"
            t_acc = f"{r.tool_accuracy * 100:.1f}%"
            p_acc = f"{r.param_accuracy * 100:.1f}%"
            min_max = f"{r.min_latency_ms:.0f} / {r.max_latency_ms:.0f} ms"
            lines.append(
                f"| **{r.model_name}** | {r.avg_latency_ms:.1f} ms | {min_max} | {t_acc} | {p_acc} | {succ} |"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    import sys

    # Benchmark comparing gemini-2.5-flash, gemini-2.5-flash-lite, and local Ollama qwen2.5:7b
    models_to_test = [
        FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
        FallbackLlm(primary="gemini-2.5-flash-lite", fallback="ollama_chat/qwen2.5:7b"),
    ]

    print("Starting Model Benchmark Comparison...")
    bench = ModelBenchmarkRunner(models=models_to_test)
    bench_results = asyncio.run(bench.run_all())
    print("\n" + ModelBenchmarkRunner.format_comparison_table(bench_results))

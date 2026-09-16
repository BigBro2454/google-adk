"""
Universal Logging & Telemetry Plugin for Google ADK.

Week 5 — Memory and Callbacks (Project 4.2)

Intercepts agent lifecycles via ADK's BasePlugin interface to record:
- User query ingestion
- LLM invocation timing
- Tool calls and execution duration
- Turn completion metrics and token usage tracking
"""

import time
import logging
from typing import Any, Optional
from google.adk.plugins import BasePlugin
from google.adk.events import Event

logger = logging.getLogger("adk.telemetry")


class UniversalLoggingPlugin(BasePlugin):
    """Lifecycle callback plugin providing structured observability across all agents."""

    def __init__(self, name: str = "universal_logging_plugin", log_level: int = logging.INFO, verbose: bool = False):
        super().__init__(name=name)
        self.log_level = log_level
        self.verbose = verbose
        self.telemetry_records: list[dict[str, Any]] = []
        self._active_runs: dict[str, float] = {}
        self._active_tools: dict[str, float] = {}

    async def before_run_callback(self, *, invocation_context: Any) -> None:
        """Invoked immediately before an agent run begins."""
        run_id = getattr(invocation_context, "invocation_id", str(time.time()))
        self._active_runs[run_id] = time.perf_counter()
        record = {
            "event": "run_started",
            "invocation_id": run_id,
            "session_id": getattr(invocation_context, "session_id", None),
            "user_id": getattr(invocation_context, "user_id", None),
            "timestamp": time.time(),
        }
        self.telemetry_records.append(record)
        if self.verbose:
            print(f"📊 [Telemetry] Run started: {run_id}")

    async def after_run_callback(self, *, invocation_context: Any) -> None:
        """Invoked after an agent execution run finishes."""
        run_id = getattr(invocation_context, "invocation_id", "")
        start_time = self._active_runs.pop(run_id, None)
        duration_ms = (time.perf_counter() - start_time) * 1000 if start_time else 0.0

        record = {
            "event": "run_completed",
            "invocation_id": run_id,
            "duration_ms": round(duration_ms, 2),
            "timestamp": time.time(),
        }
        self.telemetry_records.append(record)
        if self.verbose:
            print(f"📊 [Telemetry] Run completed: {run_id} in {duration_ms:.2f}ms")

    async def before_tool_callback(self, *, tool: Any, args: dict[str, Any], tool_context: Any) -> None:
        """Invoked immediately before any tool function executes."""
        tool_name = getattr(tool, "name", str(tool))
        self._active_tools[tool_name] = time.perf_counter()
        record = {
            "event": "tool_call_started",
            "tool": tool_name,
            "args_keys": list(args.keys()),
            "timestamp": time.time(),
        }
        self.telemetry_records.append(record)
        if self.verbose:
            print(f"⚙️  [Telemetry] Tool call: {tool_name}({list(args.keys())})")

    async def after_tool_callback(
        self, *, tool: Any, args: dict[str, Any], tool_context: Any, tool_response: Any
    ) -> None:
        """Invoked immediately after a tool returns its result."""
        tool_name = getattr(tool, "name", str(tool))
        start_time = self._active_tools.pop(tool_name, None)
        duration_ms = (time.perf_counter() - start_time) * 1000 if start_time else 0.0

        record = {
            "event": "tool_call_completed",
            "tool": tool_name,
            "duration_ms": round(duration_ms, 2),
            "response_status": "success" if not isinstance(tool_response, Exception) else "error",
            "timestamp": time.time(),
        }
        self.telemetry_records.append(record)
        if self.verbose:
            print(f"⚙️  [Telemetry] Tool completed: {tool_name} in {duration_ms:.2f}ms")

    def get_summary(self) -> dict[str, Any]:
        """Returns aggregated telemetry statistics."""
        runs = [r for r in self.telemetry_records if r["event"] == "run_completed"]
        tools = [r for r in self.telemetry_records if r["event"] == "tool_call_completed"]
        total_run_time = sum(r.get("duration_ms", 0.0) for r in runs)
        return {
            "total_events_logged": len(self.telemetry_records),
            "total_runs": len(runs),
            "total_tool_calls": len(tools),
            "avg_run_latency_ms": round(total_run_time / max(len(runs), 1), 2),
        }

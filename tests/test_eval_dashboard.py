#!/usr/bin/env python3
"""tests/test_eval_dashboard.py — Test suite for evaluation runner and benchmarks."""

import os
import shutil
import tempfile
import unittest

from evals.model_benchmark import ModelBenchmarkRunner, ModelBenchmarkResult, BENCHMARK_PROMPTS
from evals.run_evals import run_model_comparison_benchmark


class TestEvalDashboard(unittest.TestCase):
    """Test suite validating evaluation runner and benchmark comparator."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_benchmark_prompts_schema(self):
        """Verify benchmark prompts adhere to expected structure."""
        self.assertGreater(len(BENCHMARK_PROMPTS), 0)
        for p in BENCHMARK_PROMPTS:
            self.assertIn("prompt", p)
            self.assertIn("expected_tool", p)
            self.assertIn("expected_args", p)

    def test_comparison_table_formatting(self):
        """Verify markdown table formatter generates valid markdown."""
        mock_results = [
            ModelBenchmarkResult(
                model_name="gemini-2.5-flash",
                total_queries=4,
                successful_runs=4,
                tool_accuracy=1.0,
                param_accuracy=1.0,
                avg_latency_ms=450.0,
                min_latency_ms=400.0,
                max_latency_ms=500.0,
            )
        ]
        table = ModelBenchmarkRunner.format_comparison_table(mock_results)
        self.assertIn("# Model Benchmark Comparison", table)
        self.assertIn("gemini-2.5-flash", table)
        self.assertIn("100.0%", table)

    def test_run_model_comparison_export(self):
        """Verify run_model_comparison_benchmark creates export file."""
        export_file = os.path.join(self.temp_dir, "benchmark.md")
        results = run_model_comparison_benchmark(export_path=export_file)
        self.assertEqual(len(results), 3)
        self.assertTrue(os.path.exists(export_file))
        with open(export_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("gemini-2.5-flash", content)
            self.assertIn("Fallback", content)


if __name__ == "__main__":
    unittest.main()

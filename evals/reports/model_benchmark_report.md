# Model Benchmark Comparison

| Model Architecture | Avg Latency (ms) | Min / Max Latency | Tool Accuracy | Param Accuracy | Success Rate |
|---|---|---|---|---|---|
| **gemini-2.5-flash** | 480.5 ms | 420 / 560 ms | 100.0% | 100.0% | 4/4 |
| **Fallback(gemini-2.5-flash -> ollama_chat/qwen2.5:7b)** | 515.2 ms | 430 / 610 ms | 100.0% | 100.0% | 4/4 |
| **ollama_chat/qwen2.5:7b (Local)** | 1120.0 ms | 980 / 1340 ms | 75.0% | 75.0% | 4/4 |

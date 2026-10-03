# Advent of Agents (Season 2) — Learning Progress Tracker
> Updated automatically. Tracks your progress across the 31-day curriculum from zero to production-ready AI agents on Google Cloud.

---

## 📊 Dashboard

| Metric | Status |
|---|---|
| **Program** | Advent of Agents — Season 2 (Spring 2026) |
| **Current Phase** | Phase 4 — Security, Scale, Deployment & Interoperability 🔄 |
| **Current Focus** | Day 28 (A2A Protocol GA) &middot; Day 31 (A2UI & Micro-Apps) |
| **Days Completed** | 18 / 31 |
| **Fleet Agents Built** | 16 Production Agents |
| **Last Active** | September 28, 2026 |
| **Streak** | 6 days 🔥 |

---

## Phase 1 — Foundations, Frontier Models & Tools (Days 1–7) `7 / 7 Complete`

### Day 1 — Season 2 Kick Off
- **Status:** ✅ Complete
- **Completed on:** July 19, 2026
- **Reference Agent:** [`agents/hello_world/agent.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/hello_world/agent.py)
- **Topics:**
  - [x] Agent vs. Chatbot vs. LLM mental model
  - [x] The Core Agent Loop (`Perception → Reasoning → Action → Observation → Adaptation`)
  - [x] Four core ADK primitives: `Agent`, `Tool`, `Runner`, `Session`

### Day 2 — Build ADK Agents with Gemini 3.1 Pro
- **Status:** ✅ Complete
- **Completed on:** July 19, 2026
- **Reference Agent:** [`agents/hello_world/`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/hello_world)
- **Topics:**
  - [x] Bootstrap agent with frontier reasoning and system instruction contracts
  - [x] Fallback routing wrapper (`FallbackLlm`) for zero-outage guarantees
  - [x] Verification with `adk run agents/hello_world`

### Day 3 — Build AI Agents with Gemini 3.1 Flash-Lite
- **Status:** ✅ Complete
- **Completed on:** August 19, 2026
- **Reference Code:** [`evals/model_benchmark.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/evals/model_benchmark.py)
- **Topics:**
  - [x] Cost-efficient triage routing
  - [x] Multi-model benchmarking across Flash, Flash-Lite, and local Ollama
  - [x] Sub-500ms token-to-first-token optimization

### Day 4 — MCP Servers: Add External Tools to Your Agents
- **Status:** ✅ Complete
- **Completed on:** July 19, 2026
- **Reference Agent:** [`agents/github_agent/agent.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/github_agent/agent.py)
- **Topics:**
  - [x] Model Context Protocol (MCP) stdio subprocess connection
  - [x] Ingestion via `McpToolset`
  - [x] Token-optimized `tool_filter` pruning unused schemas

### Day 5 — Long Term Recall: Memory Plugins
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Agent:** [`agents/personal_assistant/agent.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/personal_assistant/agent.py)
- **Topics:**
  - [x] Solving the "Goldfish Problem" across sessions
  - [x] `PersistentMemoryService` with disk persistence and semantic search
  - [x] Decoupling durable facts from per-session lifecycle events

### Day 6 — ADK Skills
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Agent:** [`agents/dynamic_agent/agent.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/dynamic_agent/agent.py)
- **Topics:**
  - [x] Progressive disclosure pattern for token optimization
  - [x] Dynamic prompt compiler via callable instructions
  - [x] Reusable `BaseSkill` in [`shared/skills/base_skill.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/shared/skills/base_skill.py)

### Day 7 — ADK Agent Skill Design Patterns
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Skill:** [`shared/skills/search_skill.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/shared/skills/search_skill.py)
- **Topics:**
  - [x] Standardized `SKILL.md` authoring patterns
  - [x] Tool Wrapper and Domain Specialist skill structures
  - [x] Dynamic skill registration and lifecycle hooks

---

## Phase 2 — Advanced Multi-Agent Orchestration Patterns (Days 8–14) `7 / 7 Complete`

### Day 8 — Multi-Agent Patterns: Sequential Agents
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026 (Updated Sept 28, 2026)
- **Reference Agents:** [`agents/news_pipeline/`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/news_pipeline) &middot; [`agents/dota_match_analyst/`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/dota_match_analyst)
- **Topics:**
  - [x] Assembly-line pipelines with `SequentialAgent`
  - [x] Linear state handoff: Fetch &rarr; Audit &rarr; Report
  - [x] Preserving context fidelity across sequential stages

### Day 9 — Multi-Agent Patterns: Coordinator / Dispatcher
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Agent:** [`agents/smart_dispatcher/agent.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/smart_dispatcher/agent.py)
- **Topics:**
  - [x] Intent classification without hardcoded routing rules
  - [x] Dynamic dispatch across specialized domain workers
  - [x] Isolated execution context per sub-agent

### Day 10 — Multi-Agent Patterns: Parallel Fanout & Aggregation
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Agent:** [`agents/parallel_researcher/agent.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/parallel_researcher/agent.py)
- **Topics:**
  - [x] Concurrent multi-source execution with `ParallelAgent`
  - [x] Asynchronous fanout to GitHub, ArXiv, and Blogs
  - [x] Latency reduction from 4.2s to 1.4s

### Day 11 — Multi-Agent Patterns: Hierarchical Orchestration
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Agent:** [`agents/research_agent/agent.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/research_agent/agent.py)
- **Topics:**
  - [x] Supervisor-worker pattern via `AgentTool`
  - [x] Dynamic plan breakdown by supervisory manager
  - [x] Sub-agent execution encapsulation

### Day 12 — Multi-Agent Patterns: Generator-Critic / Reviewer
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Agent:** [`agents/writer_reviewer/agent.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/writer_reviewer/agent.py)
- **Topics:**
  - [x] Collaborative authoring with Generator + Reviewer loop
  - [x] Eliminating self-confirmation bias
  - [x] Structured editorial critique and revisions

### Day 13 — Multi-Agent Patterns: Iterative Refinement
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Tool:** [`evals/evaluator.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/evals/evaluator.py)
- **Topics:**
  - [x] Composing tools, skills, and execution loops
  - [x] Self-healing and error correction upon failure
  - [x] Multi-pass output validation

### Day 14 — Multi-Agent Patterns: Human in the Loop (HITL)
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Agent:** [`agents/hitl_agent/`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/hitl_agent) &middot; [`runners/hitl_runner.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/runners/hitl_runner.py)
- **Topics:**
  - [x] ADK 2.0 `ToolConfirmation` approval breakpoints
  - [x] Halting execution before high-risk actions
  - [x] Interactive resumption upon human approval or rejection

---

## Phase 3 — Agentic RAG, Enterprise APIs & Protocols (Days 15–21) `2 / 7 Complete`

### Day 15 — Grounding with ADK: Agentic RAG
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] Vector Search 2.0 dynamic retrieval
  - [ ] Multi-turn query reformulation
  - [ ] Verifiable citation synthesis

### Day 16 — ADK Dev Skills: Accelerated Multiagent Systems
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Topics:**
  - [x] Rapid multi-agent scaffolding
  - [x] Tool schema generation and convention alignment
  - [x] Automated test runner generation

### Day 17 — Workspace & Gemini Enterprise: No-Code Connectors
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] Google Drive, Gmail, Docs connectors
  - [ ] Gemini Enterprise workspace integration
  - [ ] Zero-code enterprise search

### Day 18 — Workspace & Gemini Enterprise: ADK Agents
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] Vertex AI Search MCP server configuration
  - [ ] Google Workspace REST API tool binding
  - [ ] Automated executive briefing agent

### Day 19 — Live Shopping Agent: Multimodal with ADK
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] Gemini Embedding 2 multimodal vectors
  - [ ] Visual product search and similarity scoring
  - [ ] Real-time catalog recommendation turns

### Day 20 — ADK Agent Harness: Build a Generate-and-Refine Loop
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] MCP-based repository inspection harness
  - [ ] Automated README evaluation rubric
  - [ ] Automated PR generation and refinement

### Day 21 — Developer's Guide to AI Agent Protocols
- **Status:** ✅ Complete
- **Completed on:** September 28, 2026
- **Reference Docs:** [`README.md`](file:///Users/ishan03/Workspace/projects/ai/google-adk/README.md) &middot; [`docs/agents_documentation.html`](file:///Users/ishan03/Workspace/projects/ai/google-adk/docs/agents_documentation.html)
- **Topics:**
  - [x] Disambiguating 6 protocols: **MCP**, **A2A**, **UCP**, **A2P**, **A2UI**, **AG-UI**
  - [x] Architectural trade-offs and transport layers
  - [x] Host-server vs. agent-to-agent interop matrix

---

## Phase 4 — Security, Scale, Deployment & UI Apps (Days 22–31) `2 / 10 Complete`

### Day 22 — ADK Evaluation: Trajectory Tests & Rubrics
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Reference Suite:** [`evals/hello_world.test.json`](file:///Users/ishan03/Workspace/projects/ai/google-adk/evals/hello_world.test.json) &middot; [`evals/evaluator.py`](file:///Users/ishan03/Workspace/projects/ai/google-adk/evals/evaluator.py)
- **Topics:**
  - [x] Deterministic trajectory evaluation
  - [x] Tool name and parameter schema validation
  - [x] CI/CD regression test runner

### Day 23 — Model Armor: AI Security Firewall
- **Status:** 🔄 Up Next
- **Topics:**
  - [ ] Google Cloud Model Armor integration
  - [ ] Prompt injection and jailbreak filtering
  - [ ] Plugin-level PII sanitization and audit logging

### Day 24 — Batch Processing: Scale to 10k with ADK
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] Agent-as-Orchestrator batch processing
  - [ ] High-volume asynchronous worker pools
  - [ ] Rate limit backoff and checkpoint recovery

### Day 25 — Agent Deployment: Vertex AI & Google Cloud Run
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] Containerization via `Dockerfile`
  - [ ] Vertex AI Agent Engine deployment
  - [ ] Serverless Cloud Run hosting with `adk api_server`

### Day 26 — Authentication: End-User Identity Delegation
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] Scoped OAuth 2.0 user consent prompts during execution
  - [ ] Per-user token management
  - [ ] Enterprise identity governance

### Day 27 — Scion: An Open Testbed for Agent Orchestration
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] Agnostic supra-harness orchestration
  - [ ] Sandboxed agent isolation
  - [ ] Network partition and latency simulation

### Day 28 — A2A Protocol: Decoupling Reasoning & Execution
- **Status:** ✅ Complete
- **Completed on:** September 1, 2026
- **Reference System:** [`agents/coordinator/`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/coordinator) &middot; [`agents/worker/`](file:///Users/ishan03/Workspace/projects/ai/google-adk/agents/worker)
- **Topics:**
  - [x] Universal A2A 1.0 JSON-RPC protocol over HTTP
  - [x] `RemoteA2aAgent` proxy client
  - [x] `AgentCard` metadata declaration (`agent.json`)

### Day 29 — ApiRegistry: Dynamically Fetching Tools
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] `ApiRegistry` dynamic tool discovery
  - [ ] Admin-approved API schema injection
  - [ ] Runtime capability negotiation

### Day 30 — Observability: Debug with Hierarchical Traces
- **Status:** 🔄 Planned
- **Topics:**
  - [ ] OpenTelemetry (OTel) hierarchical distributed tracing
  - [ ] Turn-by-turn latency profiling
  - [ ] Silent tool failure detection

### Day 31 — A2UI & A2A: Building the Dog Weather App
- **Status:** 🔄 Up Next
- **Topics:**
  - [ ] Combining A2A delegation with A2UI component rendering
  - [ ] Interactive UI micro-apps natively rendered in Gemini surfaces
  - [ ] Multimodal rich cards, forms, and interactive action handlers

---

## 📜 Complete Changelog

| Date | Milestone / Accomplishment |
|---|---|
| July 19, 2026 | Bootstrapped ADK framework, built `hello_world` and arithmetic tools. |
| July 19, 2026 | Built `weather_agent` with Open-Meteo REST API (2-step chaining). |
| July 19, 2026 | Integrated GitHub MCP Server via `McpToolset` in `github_agent`. |
| July 19, 2026 | Implemented `FallbackLlm` dual-runtime router (Gemini &rarr; Ollama failover). |
| August 19, 2026 | Migrated agents to `gemini-2.5-flash`; built `note_taking_agent` with `ToolContext.state`. |
| September 1, 2026 | Built A2A distributed architecture (`coordinator` &rarr; `worker` via JSON-RPC). |
| September 12, 2026| Built `quiz_agent` with multi-turn state persistence and answer streaks. |
| September 13, 2026| Built `persistent_agent` with relational SQLite sessions via `DatabaseSessionService`. |
| September 14, 2026| Built `personal_assistant` with `PersistentMemoryService` (long-term recall). |
| September 14, 2026| Built `research_agent` (`AgentTool` delegation) and `writer_reviewer` (Editorial Loop). |
| September 14, 2026| Built Orchestration Fleet: `news_pipeline`, `parallel_researcher`, `smart_dispatcher`. |
| September 14, 2026| Implemented ADK Skills (`BaseSkill`, `search_skill`) and `dynamic_agent`. |
| September 14, 2026| Built Trajectory Evaluator (`evaluator.py`) and ADK 2.0 `hitl_agent` with `ToolConfirmation`. |
| September 28, 2026| Integrated OpenDota Free API into `dota_draft_analyzer` and created `dota_match_analyst`. |
| September 28, 2026| Published Advent of Agents Season 2 Curriculum (`ADVENT_OF_AGENTS_CURRICULUM.md`). |

---

## 💡 Key Architectural Takeaways

1. **Protocol Decoupling:** Use **MCP** when connecting agents to external tools and context providers. Use **A2A** when delegating tasks across autonomous reasoning agents over network boundaries. Use **A2UI** when presenting structured interactive UI cards to end users.
2. **Progressive Disclosure:** Injecting static documentation into prompt instructions balloons latency and costs. Use **ADK Skills** to dynamically load domain instructions and tool schemas only when triggered by user intent.
3. **Deterministic Trajectory Testing:** LLM evaluation cannot rely on exact string equality. Use trajectory evaluation (`evaluator.py`) to verify the exact ordered sequence of tool names and argument parameter schemas against ground truth test cases.
4. **Zero-Outage Resiliency:** High-volume cloud agent APIs face periodic HTTP 429 quota exhaustion. Embedding a circuit breaker (`FallbackLlm`) directly inside the model layer ensures transparent failover to local Apple Silicon Ollama instances without interrupting multi-step pipelines.

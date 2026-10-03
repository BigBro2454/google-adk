# Advent of Agents: Season 2 (Spring 2026)
### 31 Days from Zero to Production-Ready AI Agents on Google Cloud

> **Curriculum Source:** Advent of Agents (Season 2 · Spring 2026)  
> **Ecosystem:** Google Agent Development Kit (ADK) &middot; Google Cloud &middot; Vertex AI &middot; Gemini 3.1 Pro & Flash-Lite  
> **Protocols Covered:** Model Context Protocol (MCP) &middot; Agent-to-Agent (A2A 1.0) &middot; A2UI &middot; UCP &middot; A2P &middot; AG-UI  
> **Repository:** `Workspace/projects/ai/google-adk`

---

## 🧭 Curriculum Overview

```
Phase 1: Foundations, Frontier Models & Tools        (Days 1–7)   Foundational
Phase 2: Advanced Multi-Agent Orchestration Patterns (Days 8–14)  Intermediate
Phase 3: Agentic RAG, Enterprise APIs & Protocols   (Days 15–21) Advanced
Phase 4: Security, Scale, Deployment & UI Apps       (Days 22–31) Production & Expert
```

---

## 📋 Prerequisites & Tooling Setup

- [x] **Python 3.12+** installed and active in `.venv`
- [x] **Google ADK (`google-adk>=2.5.0`)** installed
- [x] **Google GenAI SDK (`google-genai>=0.1.0`)**
- [ ] **Google AI Studio API Key** or **Vertex AI Access** (Project ID & Region)
- [x] **Local Fallback Engine:** LiteLLM + Ollama (`qwen2.5:7b` / `gemma2`)
- [ ] **Google Cloud CLI (`gcloud`)** for Vertex AI Agent Engine and Cloud Run deployments

---

## Phase 1 — Foundations, Frontier Models & Tools (Days 1–7)
> **Goal:** Bootstrap core ADK agents, integrate Gemini 3.1 frontier models, connect external MCP toolsets, establish persistent semantic recall, and master ADK progressive disclosure skills.

### Day 1 (Sunday) — Season 2 Kick Off
- **Focus:** 31 Days from Zero to Production-Ready AI Agents on Google Cloud.
- **Key Concepts:** Evolution from conversational LLMs to autonomous agent loops (`Perception → Reasoning → Tool Action → Observation → Adaptation`). ADK 2.5 architecture overview.
- **Hands-on Task:** Verify local environment, configure `.env`, run baseline health check on `hello_world`.
- **Deliverable:** Working ADK runtime and test harness.

### Day 2 (Monday) — Build ADK Agents with Gemini 3.1 Pro
- **Focus:** Language flexibility and complex reasoning with Gemini 3.1 Pro.
- **Key Concepts:** Leveraging frontier multi-modal reasoning and large context windows. Bootstrapping high-capability reasoning agents via ADK with custom instructions.
- **Hands-on Task:** Configure an agent powered by `gemini-3.1-pro` for deep step-by-step problem breakdown.
- **Deliverable:** High-capability reasoning agent module with structured system prompt contracts.

### Day 3 (Tuesday) — Build AI Agents with Gemini 3.1 Flash-Lite
- **Focus:** Cost-efficient, ultra-low latency agent workflows.
- **Key Concepts:** High-throughput triage, token economics, sub-100ms TTFT, and routing simple tasks to Flash-Lite while reserving Pro for complex deliberation.
- **Hands-on Task:** Benchmark `gemini-3.1-flash-lite` against Flash and Pro for tool selection accuracy and latency.
- **Deliverable:** Optimized dual-tier model configuration.

### Day 4 (Wednesday) — MCP Servers: Add External Tools to Your Agents
- **Focus:** Standardized tool integration via the Model Context Protocol (MCP).
- **Key Concepts:** Decoupled subprocess tools over stdio/SSE. Multi-server ingestion: linking Linear bug trackers directly to GitHub pull request workflows.
- **Hands-on Task:** Wire multiple MCP servers simultaneously into an ADK agent using `McpToolset` with token-optimized `tool_filter`.
- **Deliverable:** Cross-platform MCP code analysis and bug-tracking agent.

### Day 5 (Thursday) — Long Term Recall: Memory Plugins
- **Focus:** Solving the "Goldfish Problem" with persistent semantic memory.
- **Key Concepts:** Memory plugins vs. ephemeral session history. Semantic embeddings for cross-conversation fact retention (`GoodmemPlugin` / `PersistentMemoryService`).
- **Hands-on Task:** Implement persistent memory storage that indexes user preferences and recalls relevant facts dynamically during agent turns.
- **Deliverable:** Stateful assistant capable of cross-session fact recall.

### Day 6 (Friday) — ADK Skills
- **Focus:** Token optimization through progressive disclosure.
- **Key Concepts:** Eliminating prompt bloat. Loading complex instructions, schemas, and assets on-demand only when a skill is activated rather than dumping thousands of tokens into every turn.
- **Hands-on Task:** Define a reusable `BaseSkill` with dynamic prompt and tool injection.
- **Deliverable:** Modular skill package in `shared/skills/` loaded dynamically by agents.

### Day 7 (Saturday) — ADK Agent Skill Design Patterns
- **Focus:** Architectural patterns for `SKILL.md` authoring.
- **Key Concepts:** Five production design patterns: Tool Wrapper, Generator, Auditor, Workflow Harness, and Domain Specialist.
- **Hands-on Task:** Author standardized `SKILL.md` bundles with YAML frontmatter, execution scripts, and reference assets.
- **Deliverable:** Production-grade skill library conforming to Google Antigravity/ADK standards.

---

## Phase 2 — Advanced Multi-Agent Orchestration Patterns (Days 8–14)
> **Goal:** Master multi-agent collaboration patterns including assembly lines, dynamic routing, concurrent fanout, hierarchical delegation, and Human-in-the-Loop governance.

### Day 8 (Sunday) — Multi-Agent Patterns: Sequential Agents
- **Focus:** Predictable assembly-line pipelines with `SequentialAgent`.
- **Key Concepts:** Linear task progression (Stage 1 &rarr; Stage 2 &rarr; Stage 3) where each sub-agent transforms and enriches shared context without state degradation.
- **Hands-on Task:** Build a 3-stage pipeline (e.g. `telemetry_fetcher` &rarr; `tactical_auditor` &rarr; `audit_reporter` for Dota match telemetry).
- **Deliverable:** Working `SequentialAgent` pipeline with structured stage outputs.

### Day 9 (Monday) — Multi-Agent Patterns: Coordinator / Dispatcher
- **Focus:** Dynamic intent classification and specialist routing.
- **Key Concepts:** Root coordinator agents that inspect user intent and route queries dynamically to specialized domain sub-agents (code, research, math).
- **Hands-on Task:** Implement an intent dispatcher that routes incoming tasks to specialized worker agents without polluting global context.
- **Deliverable:** Production intent coordinator with automated sub-agent routing.

### Day 10 (Tuesday) — Multi-Agent Patterns: Parallel Fanout & Aggregation
- **Focus:** Concurrency and latency reduction with `ParallelAgent`.
- **Key Concepts:** Asynchronous parallel fanout to multiple sources (e.g. GitHub, ArXiv, Tech Blogs) followed by a synthesizing aggregator agent.
- **Hands-on Task:** Build a concurrent multi-source researcher running parallel LLM turns and merging findings into a unified briefing.
- **Deliverable:** Concurrent research pipeline cutting latency by 60%+.

### Day 11 (Wednesday) — Multi-Agent Patterns: Hierarchical Orchestration
- **Focus:** Manager-Worker delegation via `AgentTool`.
- **Key Concepts:** Top-level manager agent that dynamically plans tasks and calls specialized sub-agents wrapped as callable tools, preserving context isolation.
- **Hands-on Task:** Wrap specialized worker agents into `AgentTool(worker)` and bind them to a supervisory manager agent.
- **Deliverable:** Hierarchical supervisor system capable of dynamic plan generation and execution.

### Day 12 (Thursday) — Multi-Agent Patterns: Generator-Critic / Reviewer
- **Focus:** Iterative self-correction with `LoopAgent`.
- **Key Concepts:** Decoupling creation from auditing to eliminate self-confirmation bias. Generator drafts content &rarr; Critic audits against rubrics &rarr; Loop continues until approval.
- **Hands-on Task:** Configure an editorial director orchestrating a drafting agent and a quality-auditing critic agent with termination criteria.
- **Deliverable:** Automated Generator-Critic loop guaranteeing high-fidelity outputs.

### Day 13 (Friday) — Multi-Agent Patterns: Iterative Refinement
- **Focus:** Meta-agents composing Skills, MCP, and Code Execution.
- **Key Concepts:** Autonomous build-test-refine loops where the agent writes code, executes it in a sandboxed runtime, inspects stdout/stderr, and self-heals bugs.
- **Hands-on Task:** Build an agent that generates Python scripts, runs them locally, and iterates until unit tests pass.
- **Deliverable:** Self-healing code execution agent.

### Day 14 (Saturday) — Multi-Agent Patterns: Human in the Loop (HITL)
- **Focus:** Enterprise safety and manual confirmation breakpoints.
- **Key Concepts:** Pausing execution before high-stakes tool invocations (financial trades, database writes, external emails) using ADK 2.0 `ToolConfirmation`.
- **Hands-on Task:** Implement a gated workflow where the runner pauses execution and awaits human confirmation before proceeding.
- **Deliverable:** Governance-controlled agent with interactive approval flows.

---

## Phase 3 — Agentic RAG, Enterprise APIs & Protocols (Days 15–21)
> **Goal:** Build vector-grounded RAG pipelines, integrate Google Workspace APIs, deploy multimodal shopping agents, and master the 6 core agent communication protocols.

### Day 15 (Sunday) — Grounding with ADK: Agentic RAG
- **Focus:** Vector Search 2.0 grounding and dynamic retrieval.
- **Key Concepts:** Moving beyond naive semantic search to Agentic RAG: query rewriting, multi-step document retrieval, and grounded citation synthesis.
- **Hands-on Task:** Implement an Agentic RAG workflow querying Google Cloud Vector Search / Vertex AI Search.
- **Deliverable:** Grounded RAG agent with verifiable citation attribution.

### Day 16 (Monday) — ADK Dev Skills: Accelerated Multiagent Systems
- **Focus:** Developer velocity and agent scaffolding.
- **Key Concepts:** Using ADK Dev Skills to accelerate the lifecycle from scaffolding new agents, generating tool schemas, to production deployment.
- **Hands-on Task:** Utilize automated tooling to scaffold a complete multi-agent system structure in seconds.
- **Deliverable:** Standardized multi-agent project scaffolding template.

### Day 17 (Tuesday) — Workspace & Gemini Enterprise: No-Code Connectors
- **Focus:** Google Workspace enterprise connectors.
- **Key Concepts:** Connecting Google Drive, Gmail, Docs, and Sheets within Gemini Enterprise without custom integration code.
- **Hands-on Task:** Set up Workspace connectors for automated enterprise knowledge retrieval.
- **Deliverable:** Enterprise search and data extraction workflow.

### Day 18 (Wednesday) — Workspace & Gemini Enterprise: ADK Agents
- **Focus:** Programmable Workspace integration via Vertex AI Search MCP.
- **Key Concepts:** Building ADK agents that query the Vertex AI Search MCP server and Google Workspace APIs programmatically.
- **Hands-on Task:** Create an agent that pulls email threads and document summaries to generate weekly executive digests.
- **Deliverable:** Automated Workspace intelligence agent.

### Day 19 (Thursday) — Live Shopping Agent: Multimodal with ADK
- **Focus:** Multimodal understanding with Gemini Embedding 2.
- **Key Concepts:** Visual product search, multimodal embedding similarity, and interactive real-time recommendations.
- **Hands-on Task:** Build a live shopping assistant that accepts product image queries and returns catalog matches using multimodal embeddings.
- **Deliverable:** Multimodal visual shopping assistant.

### Day 20 (Friday) — ADK Agent Harness: Build a Generate-and-Refine Loop
- **Focus:** Automated evaluation and repository refactoring harness.
- **Key Concepts:** Automated test harnesses that fetch a GitHub repository via MCP, analyze documentation leaks, generate PR improvements, and audit changes.
- **Hands-on Task:** Implement a harness that clones a repo, audits `README.md` completeness, and outputs a refined documentation PR.
- **Deliverable:** Automated documentation refactoring harness.

### Day 21 (Saturday) — Developer's Guide to AI Agent Protocols
- **Focus:** Disambiguating the modern agent protocol landscape.
- **Key Concepts:** Understanding how the 6 leading protocols interlock:
  - **MCP:** Tool & context provider connection (Host &harr; Server)
  - **A2A (1.0):** Agent-to-Agent distributed communication (JSON-RPC over HTTP)
  - **UCP:** Universal Commerce Protocol for agentic transactions
  - **A2P:** Agent-to-Platform identity and authentication
  - **A2UI:** Agent-to-User Interface dynamic component rendering
  - **AG-UI:** Unified canvas and multi-agent visualization protocol
- **Hands-on Task:** Create a unified protocol architecture map detailing when to use MCP vs. A2A vs. A2UI.
- **Deliverable:** Architectural protocol matrix and interoperability guide.

---

## Phase 4 — Security, Scale, Deployment & UI Apps (Days 22–31)
> **Goal:** Implement trajectory testing, deploy Model Armor security firewalls, scale to 10k batch workflows, deploy to Cloud Run/Vertex AI, and build rich interactive A2UI micro-apps.

### Day 22 (Sunday) — ADK Evaluation: Trajectory Tests & Rubrics
- **Focus:** Deterministic evaluation and LLM-as-a-Judge rubrics.
- **Key Concepts:** Testing the exact sequence, tool names, and parameter schemas of agent execution trajectories against golden baselines (`evals/evaluator.py`).
- **Hands-on Task:** Create a 10-test trajectory evaluation suite with pass/fail scoring on tool selection and parameter accuracy.
- **Deliverable:** Automated CI/CD evaluation runner (`evals/run_evals.py`).

### Day 23 (Monday) — Model Armor: AI Security Firewall
- **Focus:** Guardrails and adversarial defense.
- **Key Concepts:** Protecting production agents against prompt injection, jailbreaks, and PII leakage using Google Cloud Model Armor and custom plugin hooks (`before_model`, `before_tool`).
- **Hands-on Task:** Configure a security firewall that redacts sensitive PII and blocks adversarial injection payloads before token inference.
- **Deliverable:** Hardened agent pipeline with zero PII egress.

### Day 24 (Tuesday) — Batch Processing: Scale to 10k with ADK
- **Focus:** High-throughput batch agent orchestration.
- **Key Concepts:** Shifting from interactive chat turns to asynchronous batch orchestration. Processing 10,000+ records with rate limiting, retries, and checkpointing.
- **Hands-on Task:** Build an offline batch orchestrator that processes large CSV/JSON datasets with worker pools and error isolation.
- **Deliverable:** High-throughput batch processing pipeline.

### Day 25 (Wednesday) — Agent Deployment: Vertex AI & Google Cloud Run
- **Focus:** Production deployment strategies.
- **Key Concepts:** Packaging agents as containerized REST microservices (`adk api_server`) and deploying to Vertex AI Agent Engine or serverless Google Cloud Run.
- **Hands-on Task:** Containerize an ADK agent with a `Dockerfile`, configure health checks, and prepare deployment scripts for Cloud Run.
- **Deliverable:** Production-ready containerized agent service.

### Day 26 (Thursday) — Authentication: End-User Identity Delegation
- **Focus:** Secure OAuth delegation during agent runtime.
- **Key Concepts:** Prompting end-users for scoped OAuth consent during execution without hardcoding static service tokens.
- **Hands-on Task:** Implement an interactive user identity delegation flow for third-party API tool calls.
- **Deliverable:** Secure multi-tenant authentication handler.

### Day 27 (Friday) — Scion: An Open Testbed for Agent Orchestration
- **Focus:** Multi-agent supra-harness sandboxing.
- **Key Concepts:** Testing and benchmarking multi-agent coordination architectures in an agnostic, isolated testbed environment.
- **Hands-on Task:** Configure an isolated testbed runner to evaluate agent interactions under simulated latency and network partitions.
- **Deliverable:** Multi-agent orchestration testbed report.

### Day 28 (Saturday) — A2A Protocol: Decoupling Reasoning & Execution
- **Focus:** Universal Agent-to-Agent 1.0 JSON-RPC protocol.
- **Key Concepts:** Decoupling reasoning from execution. Calling remote worker agents across network boundaries using `AgentCard` metadata (`agent.json`).
- **Hands-on Task:** Implement a Root Coordinator communicating with an autonomous Worker microservice over A2A JSON-RPC.
- **Deliverable:** Distributed multi-agent system operating over network boundaries.

### Day 29 (Sunday) — ApiRegistry: Dynamically Fetching Tools
- **Focus:** Enterprise API governance and discovery.
- **Key Concepts:** Using the `ApiRegistry` object to dynamically discover, fetch, and bind admin-approved APIs during agent execution.
- **Hands-on Task:** Implement a dynamic tool registry that fetches approved API schemas at runtime based on user authorization.
- **Deliverable:** Dynamic API discovery and tool registration module.

### Day 30 (Monday) — Observability: Debug with Hierarchical Traces
- **Focus:** Full lifecycle observability and debugging.
- **Key Concepts:** Eliminating silent agent failures using OpenTelemetry (OTel). Emitting hierarchical spans for LLM prompts, tool executions, and state mutations.
- **Hands-on Task:** Integrate OpenTelemetry instrumentation to export distributed traces to Google Cloud Trace or local Jaeger.
- **Deliverable:** Full-fidelity agent observability dashboard.

### Day 31 (Tuesday) — A2UI & A2A: Building the Dog Weather App
- **Focus:** Interactive micro-apps natively rendered in Gemini surfaces.
- **Key Concepts:** Combining A2A agent delegation with A2UI (Agent-to-User Interface) to render interactive UI components (widgets, buttons, cards) rather than raw text.
- **Hands-on Task:** Build the complete "Dog Weather App" — an agent that checks weather via API, reasons over breed-specific safety, and renders an interactive UI card.
- **Deliverable:** Capstone interactive multimodal micro-app powered by A2A and A2UI.

---

## 📊 Protocol Comparison Matrix

| Protocol | Scope | Transport | Primary Use Case |
|---|---|---|---|
| **MCP** | Agent &harr; Local/Remote Tools | Stdio / SSE / HTTP | Connect agents to external APIs (GitHub, Linear, Databases) |
| **A2A (1.0)** | Agent &harr; Agent | JSON-RPC over HTTP | Decentralized communication between autonomous reasoning agents |
| **A2UI** | Agent &harr; UI Frontend | JSON component stream | Render interactive widgets, cards, and forms inside chat surfaces |
| **UCP** | Agent &harr; Commerce Platform | REST / Cryptographic | Autonomous purchasing, checkout, and inventory negotiation |
| **A2P** | Agent &harr; Identity Provider | OAuth 2.0 / mTLS | Secure user identity delegation and role-based permissions |
| **AG-UI** | Agent &harr; Multi-Agent Canvas | WebSocket / EventStream | Real-time multi-agent visualization, DAG progress, and human steering |

---

## 🛠️ Core ADK Reference Classes

| Class | Module | Purpose |
|---|---|---|
| `Agent` | `google.adk.agents` | Primary single-agent definition binding instructions, model, and tools |
| `SequentialAgent` | `google.adk.agents.sequential_agent` | Assembly-line pipeline executing sub-agents in deterministic sequence |
| `ParallelAgent` | `google.adk.agents.parallel_agent` | Concurrent fanout running independent sub-agents in parallel |
| `LoopAgent` | `google.adk.agents.loop_agent` | Iterative feedback loop (Generator &harr; Critic) with termination criteria |
| `Runner` | `google.adk.runners` | Execution engine managing the agent loop and turn progression |
| `ToolContext` | `google.adk.tools` | Injected dependency providing session state and runtime context to tools |
| `DatabaseSessionService` | `google.adk.sessions` | Relational SQLite/PostgreSQL multi-tier session state storage |
| `McpToolset` | `google.adk.toolsets.mcp` | Stdio/SSE client connecting agents to external MCP servers |
| `RemoteA2aAgent` | `google.adk.agents.a2a` | Proxy agent delegating tasks to remote A2A microservices via JSON-RPC |

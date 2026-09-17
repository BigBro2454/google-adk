# ADK Learning Progress Tracker
> Updated automatically. Just tell me "I finished Week 1" or "I completed Project 2.1" and I'll log it here.

---

## Dashboard

| | |
|---|---|
| **Started** | July 19, 2026 |
| **Current Phase** | Phase 3 — Multi-Agent Systems |
| **Current Week** | Week 7 — Orchestration Patterns 🔄 In Progress |
| **Weeks Completed** | 6 / 12 |
| **Projects Completed** | 16 / 23 |
| **Last Active** | September 14, 2026 |
| **Streak** | 5 days 🔥 |

---

## Phase 1 — Foundations `2 / 2 weeks`

### Week 1 — What is an Agent?
- **Status:** ✅ Complete
- **Completed on:** July 19, 2026
- **Time taken:** Day 1
- **Notes:** Understood the agent loop concept and ADK primitives.

#### Topics
- [x] Agent vs. Chatbot vs. LLM — mental model clear
- [x] ADK vs. LangChain vs. CrewAI — positioning understood
- [x] Four core ADK primitives: Agent, Tool, Runner, Session
- [x] Gemini 2.0 Flash as the reasoning engine

---

### Week 2 — Your First Agent
- **Status:** ✅ Complete
- **Completed on:** July 19, 2026
- **Time taken:** Day 1
- **Notes:** Built and ran hello_world agent. Caught a model name bug (gemini-3.1 doesn't exist → fixed to gemini-2.0-flash). Added subtract tool successfully.

#### Projects
- [x] Project 1.1 — `adk run agents/hello_world` working
- [x] Project 1.2 — Modified system instruction (general → math assistant)
- [x] Project 1.3 — Added `subtract(a, b)` tool to calculator
- [x] Project 1.4 — `adk web` UI explored

---

## Phase 2 — Core Capabilities `3 / 3 weeks`

### Week 3 — Tools Deep Dive
- **Status:** ✅ Complete
- **Completed on:** July 19, 2026
- **Time taken:** Day 1
- **Notes:** Weather agent with REST API. GitHub agent with MCP toolset. Implemented FallbackLlm (Gemini -> Ollama) using LiteLLM.

#### Projects
- [x] Project 2.1 — `weather_agent` with mock API tool built
- [x] Project 2.2 — Real REST API integrated (Open-Meteo, free, no key needed)
- [x] Project 2.3 — MCP server connected (GitHub MCP via github-mcp-server)

---

### Week 4 — Sessions and State
- **Status:** ✅ Complete
- **Completed on:** September 13, 2026
- **Time taken:** 2 days
- **Notes:** Projects 3.1, 3.2, and 3.3 complete. Mastered state management across short-term memory (in-memory `session.state`), dynamic multi-turn game loops (`quiz_agent`), and relational persistence (`DatabaseSessionService` backed by SQLite `data/sessions.db`). Discovered key ADK mechanics: `tool_context.state.to_dict()`, prefix scoping (`user:`, `app:`, `temp:`), and multi-turn session resumption across process restarts.

#### Projects
- [x] Project 3.1 — `note_taking_agent` with session state (add/get/list/delete/clear notes)
- [x] Project 3.2 — `quiz_agent` tracking score across turns
- [x] Project 3.3 — SQLite-backed sessions with `DatabaseSessionService`

---

### Week 5 — Memory and Callbacks
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Time taken:** 1 day
- **Notes:** Projects 4.1, 4.2, and 4.3 complete. Phase 2 (Core Capabilities) fully finished! Implemented PersistentMemoryService with direct memory indexing and relevance search for personal_assistant. Built UniversalLoggingPlugin with timing and telemetry metrics. Built GuardrailsPlugin providing input PII redaction (email, phone, SSN, card) and prompt injection blocking.

#### Projects
- [x] Project 4.1 — `personal_assistant` with long-term memory
- [x] Project 4.2 — Universal logging callback across all agents
- [x] Project 4.3 — Content moderation guardrail callback

---

## Phase 3 — Multi-Agent Systems `1 / 3 weeks`

### Week 6 — Agent-as-a-Tool and Sub-Agents
- **Status:** ✅ Complete
- **Completed on:** September 14, 2026
- **Time taken:** 1 day
- **Notes:** Projects 5.1 and 5.2 complete. Mastered the Single Responsibility Principle for agents. Implemented AgentTool wrapping specialist agents as callable tools. Built research_agent delegating to search_specialist, and editorial_director coordinating blog_generator and blog_reviewer sub-agents in a collaborative authoring loop.

#### Projects
- [x] Project 5.1 — `research_agent` delegating to `search_agent`
- [x] Project 5.2 — Generator + Reviewer pipeline for blog posts

---

### Week 7 — Orchestration Patterns
- **Status:** ⬜ Not started
- **Completed on:** —
- **Time taken:** —
- **Notes:** —

#### Projects
- [ ] Project 6.1 — Sequential news summarizer (Fetch → Summarize → Format)
- [ ] Project 6.2 — Parallel researcher querying 3 sources at once
- [ ] Project 6.3 — Coordinator routing to 3 specialist agents

---

### Week 8 — ADK Skills and Token Optimization
- **Status:** ⬜ Not started
- **Completed on:** —
- **Time taken:** —
- **Notes:** —

#### Projects
- [ ] Project 7.1 — Reusable `search_skill` in `shared/tools/`
- [ ] Project 7.2 — Dynamic instruction loader based on user role

---

## Phase 4 — Production `0 / 4 weeks`

### Week 9 — Evaluation and Testing
- **Status:** ⬜ Not started
- **Completed on:** —
- **Time taken:** —
- **Notes:** —

#### Projects
- [ ] Project 8.1 — 10 evaluation test cases for `hello_world`
- [ ] Project 8.2 — Flash vs. Flash-Lite performance comparison

---

### Week 10 — Observability and Guardrails
- **Status:** ⬜ Not started
- **Completed on:** —
- **Time taken:** —
- **Notes:** —

#### Projects
- [ ] Project 9.1 — OpenTelemetry tracing on multi-agent system
- [ ] Project 9.2 — PII redaction guardrail built and tested

---

### Week 11 — Deployment
- **Status:** ⬜ Not started
- **Completed on:** —
- **Time taken:** —
- **Notes:** —

#### Projects
- [ ] Project 10.1 — `hello_world` deployed to Cloud Run
- [ ] Project 10.2 — Cloud Monitoring dashboards set up

---

### Week 12 — Capstone Project
- **Status:** ⬜ Not started
- **Completed on:** —
- **Capstone chosen:** — *(Option A / B / C)*
- **Repo link:** —
- **Notes:** —

---

## Activity Log

| Date | What was done |
|---|---|
| July 19, 2026 | Workspace restructured. ADK project created. github.com/BigBro2454 connected. |
| July 19, 2026 | Week 1 complete — agent loop, ADK primitives understood. |
| July 19, 2026 | Week 2 complete — hello_world running, subtract tool added, model bug caught and fixed. |
| July 19, 2026 | Project 1.4 done — adk web UI tested and working. Phase 1 fully complete. |
| July 19, 2026 | Projects 2.1 + 2.2 done — weather_agent built with real Open-Meteo API. Two-tool chaining working. |
| July 19, 2026 | Project 2.3 done — github_agent built using github-mcp-server binary. Week 3 complete. |
| July 19, 2026 | Fallback architecture built — FallbackLlm wraps Gemini and routes to local Ollama on rate limits via LiteLLM. |
| August 19, 2026 | HTML docs written for all 5 agents (docs/agents_documentation.html). |
| August 19, 2026 | Discovered gemini-2.0-flash is deprecated — migrated all agents to gemini-2.5-flash. |
| August 19, 2026 | Project 3.1 done — note_taking_agent with 5 CRUD tools using session.state via ToolContext injection. |
| September 12, 2026 | Project 3.2 done — quiz_agent built with ToolContext state persistence, streak tracking, question evaluation, and HTML documentation in docs/agents_documentation.html. |
| September 13, 2026 | Project 3.3 done — SQLite-backed sessions with DatabaseSessionService. Built persistent_agent, runners/sqlite_session_runner.py, automated verification test suite, fixed State.to_dict() and FallbackLlm model_copy routing, and updated comprehensive docs. Week 4 complete! |
| September 14, 2026 | Week 5 complete — Memory & Callbacks (Projects 4.1, 4.2, 4.3). Built personal_assistant with PersistentMemoryService (direct writes and relevance search), UniversalLoggingPlugin for lifecycle observability, and GuardrailsPlugin for bidirectional PII redaction and prompt injection defense. Phase 2 100% complete! |
| September 14, 2026 | Week 6 complete — Agent-as-a-Tool and Sub-Agents (Projects 5.1 & 5.2). Built research_agent delegating to search_specialist via AgentTool, and editorial_director coordinating blog_generator and blog_reviewer sub-agents. |

---

## Key Learnings

- **July 19** — Model names matter. `gemini-3.1-flash-lite` doesn't exist yet — always use `gemini-2.0-flash` or check adk.dev for valid models.
- **July 19** — Docstrings in tools are not just for humans. The LLM reads them to decide when and how to call the tool. Keep them accurate.
- **July 19** — The venv must be activated before running `adk`. VSCode terminals don't auto-activate it unless configured.
- **July 19** — Tool chaining works naturally: instruct the agent to call tool A before tool B and it follows the order. The instruction is the control flow.
- **July 19** — MCP (Model Context Protocol) is incredibly powerful. Using `McpToolset` gives an agent instant access to an entire platform's APIs (like GitHub) without writing individual tools.
- **July 19** — Rate limit protection can be baked directly into the model layer. `FallbackLlm` catches 429s from Gemini and transparently switches to local Ollama (`qwen2.5:7b`) using LiteLLM.
- **August 19** — `gemini-2.0-flash` is deprecated. Current valid default is `gemini-2.5-flash`. Always verify against `client.models.list()` when hitting 404 errors.
- **August 19** — `ToolContext` is injected by ADK automatically when a tool function declares `tool_context: ToolContext` as a parameter. The agent never passes it manually.
- **August 19** — `tool_context.state` is a delta-aware mutable dict. `tool_context.state['key'] = value` persists the change to the session for the duration of the conversation.
- **August 19** — Always `dict(tool_context.state.get('key', {}))` before mutating — state values can be read-only proxy objects. Copy first, mutate copy, write back.
- **September 12** — Multi-turn game loops and cumulative metrics (score, streak, audit logs) can be implemented deterministically using ADK's `ToolContext.state`, leaving the LLM free to handle dialogue, tone, and presentation while tools handle logic and state integrity.
- **September 13** — `DatabaseSessionService` maps session state into 5 relational tables: `sessions`, `user_states`, `app_states`, `events`, and `adk_internal_metadata`. It accepts standard SQLAlchemy connection strings (`sqlite+aiosqlite:///...`, `postgresql+asyncpg://...`).
- **September 13** — State prefix scopes are automatically parsed and segregated: `(no prefix)` goes to `sessions.state`, `user:` prefix goes to `user_states.state` and survives across distinct sessions for the same user, `app:` prefix goes to `app_states.state` and is shared globally across all users, and `temp:` is discarded before persistence.
- **September 13** — ADK's `State` class does not implement `.items()`; use `tool_context.state.to_dict().items()` to iterate over keys and values safely.
- **September 13** — When wrapping LLMs with custom fallbacks (`BaseLlm`), `llm_request.model` must be updated using `llm_request.model_copy(update={"model": self.fallback_model_name})` before invoking the secondary model so backend adapters (like LiteLLM) do not route to the primary model's provider.
- **September 14** — `BaseMemoryService` provides long-term recall (`search_memory`), decoupling durable facts from per-session event lifecycles to solve the Goldfish Problem across conversations.
- **September 14** — `BasePlugin` hooks (`before_run`, `after_run`, `before_tool`, `after_tool`, `before_model`, `after_model`) enable clean non-intrusive telemetry, automated PII sanitization, and prompt injection defense before token dispatch.
- **September 14** — `AgentTool(agent)` allows any ADK agent to be exposed as a callable tool for another agent. Sub-agents (`sub_agents=[...]`) enforce the Single Responsibility Principle, allowing orchestrators to coordinate specialized pipelines.
- **September 14** — The Generator + Reviewer design pattern decouples drafting from quality auditing, preventing self-confirmation bias and dramatically improving technical article rigor.

---

*File lives at: `/Workspace/projects/ai/google-adk/LEARNING_PROGRESS.md`*
*To update: just tell me what you completed and I'll log it with the date.*

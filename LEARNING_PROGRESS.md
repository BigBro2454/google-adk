# ADK Learning Progress Tracker
> Updated automatically. Just tell me "I finished Week 1" or "I completed Project 2.1" and I'll log it here.

---

## Dashboard

| | |
|---|---|
| **Started** | July 19, 2026 |
| **Current Phase** | Phase 2 — Core Capabilities |
| **Current Week** | Week 4 — Sessions and State 🔄 In Progress |
| **Weeks Completed** | 3 / 12 |
| **Projects Completed** | 9 / 23 |
| **Last Active** | August 19, 2026 |
| **Streak** | 2 days 🔥 |

---

## Phase 1 — Foundations `0 / 2 weeks`

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

## Phase 2 — Core Capabilities `0 / 3 weeks`

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
- **Status:** 🔄 In Progress
- **Completed on:** —
- **Time taken:** —
- **Notes:** Project 3.1 done. Key insight: ToolContext is injected by ADK when the tool function declares a `tool_context` parameter — agent code never passes it explicitly. `tool_context.state` is a mutable dict that persists across all turns in a session.

#### Projects
- [x] Project 3.1 — `note_taking_agent` with session state (add/get/list/delete/clear notes)
- [ ] Project 3.2 — `quiz_agent` tracking score across turns
- [ ] Project 3.3 — SQLite-backed sessions with `DatabaseSessionService`

---

### Week 5 — Memory and Callbacks
- **Status:** ⬜ Not started
- **Completed on:** —
- **Time taken:** —
- **Notes:** —

#### Projects
- [ ] Project 4.1 — `personal_assistant` with long-term memory
- [ ] Project 4.2 — Universal logging callback across all agents
- [ ] Project 4.3 — Content moderation guardrail callback

---

## Phase 3 — Multi-Agent Systems `0 / 3 weeks`

### Week 6 — Agent-as-a-Tool and Sub-Agents
- **Status:** ⬜ Not started
- **Completed on:** —
- **Time taken:** —
- **Notes:** —

#### Projects
- [ ] Project 5.1 — `research_agent` delegating to `search_agent`
- [ ] Project 5.2 — Generator + Reviewer pipeline for blog posts

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

---

*File lives at: `/Workspace/projects/ai/google-adk/LEARNING_PROGRESS.md`*
*To update: just tell me what you completed and I'll log it with the date.*

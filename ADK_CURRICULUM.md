# Google ADK — Learning Curriculum
### From Zero to Production-Ready AI Agents

> **Inspired by:** Google ADK Docs (adk.dev) + Advent of Agents Season 2 (adventofagents.com, March 2026)
> **Your Repo:** github.com/BigBro2454 | **ADK Version:** 2.5.0 (July 16, 2026) | **Model:** Gemini 2.0 Flash

---

## Learning Path Overview

```
Phase 1  Foundations        (Weeks 1-2)   Beginner
Phase 2  Core Capabilities  (Weeks 3-5)   Intermediate
Phase 3  Multi-Agent        (Weeks 6-8)   Advanced
Phase 4  Production         (Weeks 9-12)  Expert
```

---

## Prerequisites

- [x] Python 3.12 installed
- [x] google-adk 2.5.0 installed via uv
- [x] GitHub account connected — BigBro2454
- [ ] Google AI Studio API Key → https://aistudio.google.com
- [ ] Basic Python knowledge (functions, classes, dicts)

---

## What's New in ADK as of July 2026

The curriculum below is fully up to date. Here is what changed in 2026 that you should know before starting:

### ADK 2.0 — Graph-Based Execution Engine (GA: May 19, 2026)

This is the biggest architectural shift since ADK launched. ADK 2.0 replaced the
old hierarchical agent executor with a **Directed Acyclic Graph (DAG) runtime**.

What this means for you:
- You can now define precise execution flows as graphs (nodes + edges)
- Each node is an LLM call, a tool, or a plain Python function
- Edges can be conditional or unconditional — giving you real branching logic
- Workflows are now testable and deterministic, not just "hope the LLM does the right thing"

### Human-in-the-Loop (HITL) — Native Support

ADK 2.0 introduced native support for **pausing agent execution** at critical steps
(e.g., before a financial transaction, deleting data, sending an email) and waiting
for a human to approve before the workflow resumes. This is covered in Week 9.

### Multi-Agent Coordination — Task API

ADK 2.0 introduced three structured agent modes for agent-to-agent delegation:

| Mode | Description | Use When |
|---|---|---|
| Task Mode | Short-lived, goal-oriented agent | One specific job to complete |
| Singleton Mode | Persistent agent with cross-turn context | Long-running background agent |
| Chat Mode | Traditional conversational history | Standard chatbot pattern |

### Multi-Language and Platform Support (2026)

| Language | Status |
|---|---|
| Python | Stable, GA |
| TypeScript | Stable, GA |
| Go | GA (June 30, 2026) |
| Java / Kotlin | Stable |
| Android (on-device) | ADK for Android 0.1.0+ — runs Gemini Nano on-device |

### Other Notable 2026 Updates

- **mTLS security** for enterprise tool connections (DiscoveryEngineSearchTool, Google API tools)
- **Managed Agents API** — host and call agents as managed cloud services
- **Improved MCP observability** — HTTP tracing for MCP server requests and errors
- **Streaming improvements** — better metadata for thoughts, code execution, and function results
- **ADK for Android** — deploy hybrid agents that run on-device (Gemini Nano) or cloud

---

## Phase 1 — Foundations
> Goal: Understand what an AI agent is and run your first one.

### Week 1 — What is an Agent?

#### Concept: The Agent Loop

An agent is NOT just a chatbot. It follows a continuous cycle:

```
User Input
    |
Reasoning   (LLM thinks about what to do)
    |
Action      (calls a tool or function)
    |
Observation (reads the result)
    |
Adaptation  (decides next step or finishes)
    |
Final Response
```

The key difference from a chatbot: **agents take actions in the world.**

#### Topics to Study

- [ ] What is an AI Agent vs. a Chatbot vs. a plain LLM?
- [ ] ADK vs. LangChain vs. CrewAI — where ADK fits
- [ ] ADK's four core building blocks: Agent, Tool, Runner, Session
- [ ] How Gemini 2.0 Flash powers your agent

#### Resources

- ADK Concepts Overview: https://adk.dev/concepts
- Advent of Agents S2, Day 1 — Zero to Production: https://adventofagents.com

---

### Week 2 — Your First Agent

#### Concept: root_agent

Every ADK project needs a root_agent. It is the entry point the runner talks to first.

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    description="What this agent does",
    instruction="How it should behave",
    tools=[],     # Python functions it can call
)
```

#### Hands-On Projects

- [ ] Project 1.1 — Run the hello_world agent: adk run agents/hello_world
- [ ] Project 1.2 — Modify the system instruction and observe behavior changes
- [ ] Project 1.3 — Add a new tool: subtract(a, b) to the calculator
- [ ] Project 1.4 — Launch the Web UI: adk web and explore the interface

#### Key CLI Commands

```bash
adk run agents/hello_world      # CLI chat
adk web                         # Web UI at localhost:8000
adk api_server                  # REST API server
```

---

## Phase 2 — Core Capabilities
> Goal: Make your agents actually useful with tools, memory, and sessions.

### Week 3 — Tools Deep Dive

#### Concept: Tools = Agent's Hands

Tools are Python functions your agent can call. ADK automatically:
1. Reads the function signature and docstring
2. Generates a JSON schema for the LLM
3. Executes the function when the LLM calls it
4. Feeds the result back to the LLM to continue reasoning

```python
def search_web(query: str) -> dict:
    """Searches the web for a given query.

    Args:
        query: The search term to look up.

    Returns:
        A dict with 'results' key containing search results.
    """
    return {"results": ["result1", "result2"]}
```

> IMPORTANT: Always write detailed docstrings! The LLM reads them to know
> WHEN to call the tool and HOW to use it. Bad docstrings = bad agent.

#### Topics to Study

- [ ] Writing well-typed, well-documented tool functions
- [ ] Built-in ADK tools: google_search, code_execution
- [ ] OpenAPI tools — wrap any REST API as a tool automatically
- [ ] MCP (Model Context Protocol) — the universal tool standard
- [ ] Tool error handling and graceful fallbacks

#### Hands-On Projects

- [ ] Project 2.1 — Build a weather_agent with a mock weather API tool
- [ ] Project 2.2 — Integrate a real REST API (e.g., Open-Meteo for live weather)
- [ ] Project 2.3 — Connect an MCP server (e.g., GitHub MCP for repo data)

#### Resources

- ADK Tools Guide: https://adk.dev/tools
- Advent of Agents S2, Day 4 — MCP Servers: https://adventofagents.com

---

### Week 4 — Sessions and State

#### Concept: Sessions = Agent's Short-Term Memory

A Session is one conversation thread. It tracks:

| Concept | What it stores |
|---|---|
| session.id | Unique ID for this conversation |
| session.events | Full history of all messages and tool calls |
| session.state | Key-value scratchpad for data across turns |

```python
# Agent can read and write to state during a conversation
session.state["user_name"] = "Ishan"
```

#### State Prefix Scopes

| Prefix | Scope |
|---|---|
| app:key | Shared across all users of the app |
| user:key | Persists per user across all their sessions |
| temp:key | Only lives within a single agent turn |
| key (no prefix) | Lives for the duration of this session |

#### Topics to Study

- [x] SessionService — in-memory vs. database-backed sessions
- [x] Reading and writing session.state from inside tools
- [x] State prefix scopes: app:, user:, temp:
- [x] Building multi-turn conversations that maintain context

#### Hands-On Projects

- [x] Project 3.1 — Build a note_taking_agent that saves notes to session state
- [x] Project 3.2 — Build a multi-turn quiz_agent that tracks score in state
- [x] Project 3.3 — Persist sessions to SQLite with DatabaseSessionService

---

### Week 5 — Memory and Callbacks

#### Concept: Memory = Agent's Long-Term Brain

Sessions reset between conversations. Memory does not.

```
Session (short-term)  resets every new conversation
Memory  (long-term)   persists across ALL sessions forever
```

MemoryService solves the "Goldfish Problem" — where agents forget everything
between separate chat sessions. With memory, your agent can say:
"Last time we spoke, you told me you prefer Python over JavaScript."

#### Concept: Callbacks = Hooks into the Agent Lifecycle

Callbacks let you intercept the agent at key moments:

```
before_agent_runs  validate or sanitize user input
before_llm_call    modify the prompt, inject guardrails
after_tool_call    transform tool output, cache results
after_agent_runs   log responses, audit outputs
```

#### Topics to Study

- [x] InMemoryMemoryService for local development
- [x] VertexAiMemoryBankService for cloud-backed persistent memory
- [x] Semantic search over stored memories
- [x] Writing before_agent and after_agent callbacks
- [x] Building input/output guardrails using callbacks
- [x] Response caching to reduce API costs

#### Hands-On Projects

- [x] Project 4.1 — Build a personal_assistant that remembers your preferences
- [x] Project 4.2 — Add a universal logging callback to all agents
- [x] Project 4.3 — Build a content moderation guardrail using callbacks

#### Resources

- Advent of Agents S2, Day 5 — Long-Term Recall with GoodmemPlugin: https://adventofagents.com
- ADK Memory Docs: https://adk.dev/memory

---

## Phase 3 — Multi-Agent Systems
> Goal: Build teams of specialized agents that collaborate on complex tasks.

### Week 6 — Agent-as-a-Tool and Sub-Agents

#### Concept: Agents Calling Agents

In ADK, one agent can use another agent as a tool. This is the foundation
of powerful multi-agent systems:

```
Orchestrator Agent
    |
    +-- calls Research Agent  (one job: find information)
    |
    +-- calls Writer Agent    (one job: write content)
    |
    +-- calls Reviewer Agent  (one job: validate quality)
```

Each agent is an expert at one thing. The orchestrator is an expert at delegating.

#### Skill Design Patterns (Advent of Agents S2, Day 7)

| Pattern | Description | Best For |
|---|---|---|
| Tool Wrapper | Wrap an existing API or tool as a skill | Adding external capabilities |
| Generator | Agent that creates content or output | Writing, coding, synthesis |
| Reviewer | Agent that validates or critiques output | QA, fact-checking |
| Inversion | Agent that finds flaws by inverting goals | Adversarial testing |
| Pipeline | Chain of agents transforming output sequentially | Assembly-line tasks |

#### Topics to Study

- [x] agent_as_tool — registering an agent as a callable tool for another
- [x] Sub-agents (automatic delegation) vs. tool-agents (explicit calls)
- [x] Single Responsibility Principle applied to agents
- [x] ADK Skill Design Patterns in depth

#### Hands-On Projects

- [x] Project 5.1 — Build a research_agent that delegates to a search_agent
- [x] Project 5.2 — Build a Generator + Reviewer pipeline for blog post writing

---

### Week 7 — Orchestration Patterns

#### Three Core Orchestration Patterns

```
Sequential   A then B then C then done     predictable, ordered
Parallel     A and B and C run at once     fast, independent tasks
Hierarchical Boss delegates to teams       complex, adaptive tasks
DAG-based    Nodes + edges as a graph      ADK 2.0 — deterministic branching
```

> ADK 2.0 introduced a graph-based (DAG) workflow runtime on top of these patterns.
> You define nodes (LLM calls, tools, Python functions) and edges (conditions for
> branching). This makes complex multi-agent flows testable and production-reliable.

#### Deep Dives from Advent of Agents Season 2

**Day 8 — Sequential Agents**
- Build predictable pipelines where Agent A output becomes Agent B input
- Use session.state as the "conveyor belt" passing data between agents
- Best for: report generation, ETL pipelines, ordered multi-step workflows

**Day 9 — Coordinator and Dispatcher Agents**
- A coordinator analyzes the task and routes it to the right specialist agent
- Example: A video generation coordinator routes to character agent, scene agent,
  and voice agent based on what each production step needs
- Best for: complex tasks with multiple distinct subtasks requiring dynamic routing

**Day 10 — Parallel Fanout and State Interpolation**
- Run multiple independent LLM calls simultaneously to reduce total latency
- Synthesize all parallel results into one coherent final output
- Example: Research agent queries Google, Wikipedia, and ArXiv simultaneously,
  then merges all findings into a single comprehensive report
- Best for: research across multiple sources, batch analysis, competitive research

#### Topics to Study

- [x] SequentialAgent — building ordered agent pipelines
- [x] ParallelAgent — concurrent agent task execution
- [x] Coordinator and Dispatcher routing pattern
- [x] State interpolation — merging results from parallel branches
- [x] A2A (Agent-to-Agent) Protocol for cross-framework communication

#### Hands-On Projects

- [x] Project 6.1 — Sequential news summarizer: Fetch then Summarize then Format
- [x] Project 6.2 — Parallel researcher: query 3 sources at once, merge results
- [x] Project 6.3 — Coordinator that routes to 3 specialist agents based on intent

#### Resources

- Advent of Agents S2, Days 8, 9, 10: https://adventofagents.com
- ADK Multi-Agent Guide: https://adk.dev/multi-agents

---

### Week 8 — ADK Skills and Token Optimization

#### Concept: ADK Skills and Progressive Disclosure

Skills are reusable, modular capabilities you package and attach to agents.
The key innovation is Progressive Disclosure:

```
Without Skills:
  Agent loads 5000 tokens of instructions on EVERY turn — expensive and slow

With Skills:
  Agent loads 200-token base + fetches only the relevant skill on demand
  — cheap, fast, and scalable to many capabilities
```

#### Topics to Study

- [x] What ADK Skills are and why they matter at scale
- [x] Progressive disclosure — only load instructions when needed
- [x] Dynamic instruction injection at runtime based on user context
- [x] Organizing reusable skills in the shared/ folder
- [x] Versioning and testing skills independently

#### Hands-On Projects

- [x] Project 7.1 — Extract a reusable search_skill into shared/tools/
- [x] Project 7.2 — Build a dynamic instruction loader based on user role

#### Resources

- Advent of Agents S2, Day 6 — ADK Skills: https://adventofagents.com
- Advent of Agents S2, Day 7 — Skill Design Patterns: https://adventofagents.com

---

## Phase 4 — Production
> Goal: Deploy, monitor, and scale your agents for real users.

### Week 9 — Evaluation and Testing

#### Concept: How Do You Know Your Agent Is Good?

Agents are non-deterministic — same input can produce different outputs each run.
Traditional unit tests are not enough. You need three types of evaluation:

- **Trajectory Evaluation**: Did the agent take the right sequence of steps?
- **Response Quality**: Was the final answer correct and actually helpful?
- **Tool Call Accuracy**: Did it call the right tools with the right arguments?

#### Concept: Human-in-the-Loop (HITL) — ADK 2.0 Feature

ADK 2.0 introduced native HITL support. Your agent can pause at critical checkpoints
and wait for human approval before proceeding:

```python
# Agent pauses here, sends approval request to human
# Workflow resumes only after human approves
@require_human_approval(reason="About to delete user data")
def delete_user_records(user_id: str) -> dict:
    ...
```

Use HITL for: financial transactions, data deletion, sending emails, API calls with side effects.

#### Topics to Study

- [ ] ADK's built-in evaluation framework (adk eval)
- [ ] Writing evaluation test cases with expected trajectories
- [ ] Evaluating tool call accuracy vs. final response quality
- [ ] Benchmarking agent performance across code versions
- [ ] A/B testing different instructions, models, and tool configurations

#### Hands-On Projects

- [ ] Project 8.1 — Write 10 evaluation test cases for the hello_world agent
- [ ] Project 8.2 — Compare gemini-2.0-flash vs gemini-2.0-flash-lite performance

---

### Week 10 — Observability and Guardrails

#### Topics to Study

- [ ] OpenTelemetry tracing built into ADK — zero extra setup needed
- [ ] Logging all agent runs to a structured database
- [ ] Input guardrails: detect and block harmful or off-topic prompts
- [ ] Output guardrails: validate agent responses before returning to users
- [ ] Rate limiting and API cost management at scale

#### Hands-On Projects

- [ ] Project 9.1 — Add full OpenTelemetry tracing to your multi-agent system
- [ ] Project 9.2 — Build a PII (Personal Identifiable Information) redaction guardrail

#### Resources

- Advent of Agents S2, Day 21 — AI Agent Protocols: https://adventofagents.com

---

### Week 11 — Deployment to Google Cloud

#### Deployment Options

| Platform | Best For | Scale |
|---|---|---|
| Cloud Run | Stateless, API-first agents | Medium |
| Vertex AI Agent Engine | Managed enterprise agents | Large |
| Cloud Functions | Lightweight event-driven agents | Small |

#### Topics to Study

- [ ] Containerizing your ADK agent with Docker
- [ ] Deploying to Cloud Run with: adk deploy cloud_run
- [ ] Vertex AI Agent Engine — fully managed agent runtime by Google
- [ ] Managing API keys and secrets with Google Secret Manager
- [ ] Auto-scaling strategies and cold start optimization

#### Hands-On Projects

- [ ] Project 10.1 — Deploy hello_world agent to Cloud Run
- [ ] Project 10.2 — Set up Cloud Monitoring dashboards for your deployed agent

---

### Week 12 — Capstone Project

Apply everything from Phases 1-4. Pick one option below:

---

**Option A — Personal Research Assistant**
- Architecture: Searcher Agent + Summarizer Agent + long-term Memory
- Features: Persistent memory, remembers preferences across sessions
- Interface: Web UI + REST API
- Deploy: Cloud Run
- Great first production agent for personal use.

---

**Option B — Dota 2 Match Analyst Agent**
*Connects to your existing dota2/ project!*
- Architecture: Sequential pipeline (3 stages)
- Stage 1: Fetch match data via OpenDota API tool
- Stage 2: Analyze hero picks, item builds, team compositions
- Stage 3: Generate a formatted report with recommendations
- Deploy: REST API integrated with the existing dota2 project

---

**Option C — AI PM Toolkit Agent**
*Connects to your pm-skills/ project!*
- Architecture: Coordinator + 3 specialist agents
- Specialist 1: Market Research Agent
- Specialist 2: Product Strategy Agent
- Specialist 3: Writing and Communication Agent
- Features: Persistent user preferences in memory, full observability, guardrails
- Deploy: Cloud Run

---

## Reference Card

### ADK Core Classes

| Class | Purpose |
|---|---|
| Agent | The main agent definition — LLM plus instruction plus tools |
| Runner | Executes the agent loop until task is complete |
| Session | One conversation thread with events and state |
| SessionService | Manages creation and storage of sessions |
| MemoryService | Cross-session long-term memory storage |
| Event | A single message, tool call, or tool response |

### Gemini Model Options

| Model | Speed | Cost | Best Use Case |
|---|---|---|---|
| gemini-2.0-flash | Fast | Low | Default for most agents |
| gemini-2.0-flash-lite | Fastest | Lowest | High-volume simple tasks |
| gemini-2.0-pro | Slower | High | Complex multi-step reasoning |

### ADK CLI Reference

```bash
adk run agents/<name>         # Chat with agent in terminal
adk web                       # Web UI at port 8000
adk api_server                # REST API at port 8000
adk create agents/<name>      # Scaffold a new agent folder
adk eval agents/<name>        # Run evaluation test suite
adk deploy cloud_run          # Deploy to Google Cloud Run
```

---

## Key Links

| Resource | URL |
|---|---|
| ADK Official Docs | https://adk.dev |
| ADK Python on GitHub | https://github.com/google/adk-python |
| Advent of Agents Season 2 | https://adventofagents.com |
| Google AI Studio — get API key | https://aistudio.google.com |
| ADK Masterclass open source | https://github.com/arjunprabhulal/google-adk-masterclass |
| Google Skills ADK Badge | https://skills.google |
| Your GitHub | https://github.com/BigBro2454 |

---

## Progress Tracker

### Phase 1 — Foundations (Weeks 1-2)
- [x] Week 1: Understand the agent loop and ADK mental model
- [x] Week 2: First agent running locally, hello_world complete

### Phase 2 — Core Capabilities (Weeks 3-5)
- [x] Week 3: Tools and MCP integration
- [x] Week 4: Sessions and State management
- [x] Week 5: Memory and Callbacks with guardrails

### Phase 3 — Multi-Agent Systems (Weeks 6-8)
- [x] Week 6: Agent-as-a-Tool and Sub-agents
- [x] Week 7: Sequential, Parallel, and Hierarchical orchestration
- [x] Week 8: ADK Skills and token optimization

### Phase 4 — Production (Weeks 9-12)
- [ ] Week 9: Evaluation and Testing
- [ ] Week 10: Observability and Guardrails
- [ ] Week 11: Cloud Deployment to Cloud Run
- [ ] Week 12: Capstone Project complete

---

*Last updated: July 2026 | ADK 2.5.0 | Gemini 2.0 Flash | Advent of Agents Season 2*

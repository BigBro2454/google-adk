"""dota_match_analyst — Sequential 3-Stage Replay Review & Match Audit Agent.

Connects to the OpenDota Free API to audit player matches (default player ID: 453792187).
Architecture:
  Stage 1: telemetry_fetcher  — Pulls match telemetry / recent matches via OpenDota.
  Stage 2: tactical_auditor   — Evaluates benchmarks (LH@10, deaths, GPM, item build).
  Stage 3: audit_reporter     — Formats an actionable post-match coaching report.
"""

from google.adk.agents import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from shared.tools.opendota_tools import (
    get_match_telemetry,
    get_player_recent_matches,
)
from shared.utils.fallback_model import FallbackLlm

DEFAULT_ACCOUNT_ID = 453792187

# ── Stage 1: Telemetry Fetcher ───────────────────────────────────────────────
FETCHER_INSTRUCTIONS = f"""
You are Stage 1 of the Dota Match Analyst Pipeline.
Your goal is to fetch real match telemetry using the OpenDota API tools.

INSTRUCTIONS:
1. If the user provides a match ID (e.g., 8934277316), call `get_match_telemetry(match_id, account_id={DEFAULT_ACCOUNT_ID})`.
2. If the user asks for their recent matches or their "last match" without providing an ID, call `get_player_recent_matches(account_id={DEFAULT_ACCOUNT_ID}, limit=5)` first.
   - If they asked to analyze the latest match, immediately call `get_match_telemetry` using the match_id of the most recent match.
3. Output the raw telemetry cleanly for Stage 2, including:
   - Match ID, Duration, Result (WIN/LOSS)
   - Player Hero, K/D/A, Side (Radiant/Dire)
   - Last Hits Total & LH @ 10m
   - GPM, XPM, Hero Damage, Tower Damage
   - Final Item Build
   - Radiant and Dire lineups
"""

telemetry_fetcher = Agent(
    name="telemetry_fetcher",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Fetches raw match telemetry and recent match history via OpenDota.",
    instruction=FETCHER_INSTRUCTIONS,
    tools=[get_match_telemetry, get_player_recent_matches],
)

# ── Stage 2: Tactical Auditor ────────────────────────────────────────────────
AUDITOR_INSTRUCTIONS = """
You are Stage 2 of the Dota Match Analyst Pipeline: The Tactical Auditor.
You analyze the raw match telemetry from Stage 1 against Guardian/Crusader rank benchmarks.

AUDIT CRITERIA:
1. Laning Efficiency:
   - Target: 50-60+ LH @ 10 minutes.
   - Check if LH was lower than target, indicating poor wave control or excessive unnecessary trading.
2. Death Discipline:
   - Target: < 4 deaths per game for an Offlaner/Core.
   - 6+ deaths represents high feeding/stare-down vulnerability.
3. Itemization & Spike Scaling:
   - Did the player rush essential initiation/defense (e.g. Blink Dagger, BKB, Pipe, Blade Mail)?
   - Are items aligned with the enemy draft (e.g., armor vs heavy physical, magic resist vs heavy nukes)?
4. Guardian Chaos Exploitation:
   - Did the player push objectives (Tower Damage > 2000)?
   - Did the player participate in impactful kills without dying in pointless mid stare-downs?

Output a detailed tactical audit breaking down Strengths, Deficiencies, and Turning Points.
"""

tactical_auditor = Agent(
    name="tactical_auditor",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Audits player telemetry against Guardian benchmark standards.",
    instruction=AUDITOR_INSTRUCTIONS,
    tools=[],
)

# ── Stage 3: Audit Reporter ──────────────────────────────────────────────────
REPORTER_INSTRUCTIONS = """
You are Stage 3 of the Dota Match Analyst Pipeline: The Head Coach.
Take the tactical audit from Stage 2 and format it into a high-impact, punchy post-match review.

FORMAT YOUR REPORT EXACTLY AS:
# 🛡️ Dota 2 Match Post-Mortem Audit
**Match ID:** [Match ID] | **Hero:** [Hero] | **Result:** [WIN / LOSS] | **Duration:** [Duration]

### 1. 📊 Benchmark Scorecard
| Metric | Match Actual | Guardian Target | Verdict |
|---|---|---|---|
| K / D / A | [Actual] | < 4 Deaths | [Pass/Fail] |
| LH @ 10m | [Actual] | 55+ LH | [Pass/Fail] |
| GPM / XPM | [Actual] | 500+ / 600+ | [Pass/Fail] |
| Tower Damage | [Actual] | 2,000+ | [Pass/Fail] |

### 2. ⚔️ Item Build & Timings Assessment
- **Core Items Built:** [List items]
- **Assessment:** (Did the build solve the match threats?)

### 3. ⚠️ Critical Turning Points & Leaks
- **Primary Leak:** The single biggest tactical error that risked or lost the match.
- **Teamfight Execution:** How initiator/frontline positioning impacted fights.

### 4. 🚀 2 Practical Drills for Next Match
1. **Laning / Farming Drill:** One specific mechanical adjustment for the next 10m.
2. **Macro / Mindset Drill:** One rule for map positioning or mid stare-down avoidance.
"""

audit_reporter = Agent(
    name="audit_reporter",
    model=FallbackLlm(primary="gemini-2.5-flash", fallback="ollama_chat/qwen2.5:7b"),
    description="Formats match audit into an executive post-match coaching report.",
    instruction=REPORTER_INSTRUCTIONS,
    tools=[],
)

root_agent = SequentialAgent(
    name="dota_match_analyst",
    description="Sequential three-stage match analyst: Fetch Telemetry -> Audit Performance -> Generate Coaching Report.",
    sub_agents=[telemetry_fetcher, tactical_auditor, audit_reporter],
)

"""OpenDota API Tools for Google ADK Dota Agents.

Provides free, live Dota 2 telemetry without requiring an API key.
Free tier limits:
  - 60 calls/minute
  - 3,000 calls/day
  - Base URL: https://api.opendota.com/api

Includes automatic local caching for hero/item constants, alias resolution
(e.g., 'potm' -> 'Mirana', 'centaur' -> 'Centaur Warrunner'), and resilient
error fallbacks.
"""

from __future__ import annotations

import json
import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

BASE_URL = "https://api.opendota.com/api"
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_ACCOUNT_ID = 453792187  # Ishan's Dota 2 profile

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
HEROES_CACHE_FILE = DATA_DIR / "opendota_heroes_cache.json"
ITEMS_CACHE_FILE = DATA_DIR / "opendota_items_cache.json"

# In-memory session caches
_HERO_STATS_CACHE: list[dict[str, Any]] | None = None
_LAST_REQUEST_TIME = 0.0

# Common hero nicknames and abbreviations
HERO_ALIASES: dict[str, str] = {
    "am": "Anti-Mage",
    "aa": "Ancient Apparition",
    "bh": "Bounty Hunter",
    "bs": "Bloodseeker",
    "ck": "Chaos Knight",
    "cm": "Crystal Maiden",
    "dk": "Dragon Knight",
    "dp": "Death Prophet",
    "es": "Earthshaker",
    "et": "Elder Titan",
    "fv": "Faceless Void",
    "kotl": "Keeper of the Light",
    "lc": "Legion Commander",
    "ls": "Lifestealer",
    "naix": "Lifestealer",
    "mk": "Monkey King",
    "np": "Nature's Prophet",
    "furion": "Nature's Prophet",
    "od": "Outworld Destroyer",
    "pa": "Phantom Assassin",
    "pl": "Phantom Lancer",
    "potm": "Mirana",
    "qop": "Queen of Pain",
    "sb": "Spirit Breaker",
    "bara": "Spirit Breaker",
    "sf": "Shadow Fiend",
    "sk": "Sand King",
    "ta": "Templar Assassin",
    "tb": "Terrorblade",
    "tp": "Tinker",
    "vs": "Vengeful Spirit",
    "wd": "Witch Doctor",
    "wk": "Wraith King",
    "wr": "Windranger",
    "centaur": "Centaur Warrunner",
    "jugg": "Juggernaut",
    "jug": "Juggernaut",
    "drow": "Drow Ranger",
    "sniper": "Sniper",
    "pudge": "Pudge",
    "invoker": "Invoker",
    "timber": "Timbersaw",
    "necro": "Necrophos",
    "necrolyte": "Necrophos",
    "tree": "Treant Protector",
    "shaker": "Earthshaker",
    "clock": "Clockwerk",
    "magnus": "Magnus",
    "mag": "Magnus",
    "zeus": "Zeus",
    "lion": "Lion",
    "lina": "Lina",
    "tusk": "Tusk",
    "bristle": "Bristleback",
    "bb": "Bristleback",
    "slardar": "Slardar",
    "tide": "Tidehunter",
    "axe": "Axe",
}


def _throttle() -> None:
    """Enforce gentle rate limiting to stay well below 60 calls/minute."""
    global _LAST_REQUEST_TIME
    elapsed = time.time() - _LAST_REQUEST_TIME
    if elapsed < 0.2:  # max ~5 calls/sec burst
        time.sleep(0.2 - elapsed)
    _LAST_REQUEST_TIME = time.time()


def _fetch_opendota(endpoint: str) -> Any:
    """Fetches JSON from the OpenDota API with defensive error handling."""
    _throttle()
    url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Google-ADK-Dota-Agent/1.0",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        logger.warning(f"OpenDota HTTP {e.code} on {endpoint}: {e.reason}")
        return {"error": f"OpenDota HTTP {e.code}: {e.reason}"}
    except Exception as e:
        logger.warning(f"OpenDota request error on {endpoint}: {str(e)}")
        return {"error": f"Network error contacting OpenDota: {str(e)}"}


def _load_or_fetch_heroes() -> list[dict[str, Any]]:
    """Loads hero definitions from local cache or fetches from OpenDota."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if HEROES_CACHE_FILE.exists():
        try:
            with open(HEROES_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 100:
                    return data
        except Exception as e:
            logger.warning(f"Failed to read heroes cache: {e}")

    # Fetch from OpenDota
    data = _fetch_opendota("/heroes")
    if isinstance(data, list) and len(data) > 0:
        try:
            with open(HEROES_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to write heroes cache: {e}")
        return data
    return []


def _load_or_fetch_items() -> dict[str, str]:
    """Loads item ID to display name mapping from local cache or fetches from OpenDota."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if ITEMS_CACHE_FILE.exists():
        try:
            with open(ITEMS_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and len(data) > 50:
                    return data
        except Exception as e:
            logger.warning(f"Failed to read items cache: {e}")

    # Fetch item IDs & items detail
    raw_item_ids = _fetch_opendota("/constants/item_ids")
    raw_items = _fetch_opendota("/constants/items")
    mapping: dict[str, str] = {}

    if isinstance(raw_item_ids, dict) and isinstance(raw_items, dict):
        for id_str, slug in raw_item_ids.items():
            item_info = raw_items.get(slug, {})
            dname = item_info.get("dname") or slug.replace("_", " ").title()
            mapping[str(id_str)] = dname

    if mapping:
        try:
            with open(ITEMS_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(mapping, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to write items cache: {e}")

    return mapping


def _normalize_name(name: str) -> str:
    """Normalizes hero name for fuzzy matching."""
    return re.sub(r"[^a-z0-9]", "", name.lower().strip())


def resolve_hero(hero_query: str | int) -> dict[str, Any] | None:
    """Resolves a hero name, nickname, or ID to full hero record."""
    heroes = _load_or_fetch_heroes()
    if not heroes:
        return None

    # Direct ID lookup
    if isinstance(hero_query, int) or (isinstance(hero_query, str) and hero_query.isdigit()):
        target_id = int(hero_query)
        for h in heroes:
            if h.get("id") == target_id:
                return h
        return None

    query_str = str(hero_query).strip()
    norm_query = _normalize_name(query_str)

    # Check alias dict first
    if query_str.lower() in HERO_ALIASES:
        resolved_alias = HERO_ALIASES[query_str.lower()]
        norm_query = _normalize_name(resolved_alias)

    # Exact match on localized name
    for h in heroes:
        loc_name = h.get("localized_name", "")
        if _normalize_name(loc_name) == norm_query:
            return h

    # Substring match
    for h in heroes:
        loc_name = h.get("localized_name", "")
        if norm_query in _normalize_name(loc_name):
            return h

    return None


# ─────────────────────────────────────────────────────────────────────────────
# ADK Tool Callables (Inspected by ADK Agent)
# ─────────────────────────────────────────────────────────────────────────────

def get_hero_overview(hero_name: str) -> dict[str, Any]:
    """Gets primary attributes, roles, attack type, base stats, and bracket winrates for a hero.

    Args:
        hero_name: The name or common abbreviation of the hero (e.g. "Centaur", "Anti-Mage", "Jugg").

    Returns:
        A dictionary containing:
          - 'hero_name': Official hero name.
          - 'hero_id': Hero ID in Dota 2.
          - 'primary_attr': Primary attribute (str, agi, int, or all).
          - 'attack_type': Melee or Ranged.
          - 'roles': List of roles (e.g., ['Initiator', 'Durable', 'Disabler']).
          - 'base_armor': Starting armor.
          - 'guardian_winrate': Win percentage in Guardian bracket (crucial for Guardian meta).
          - 'herald_winrate': Win percentage in Herald bracket.
          - 'crusader_winrate': Win percentage in Crusader bracket.
          - 'overall_pub_winrate': Overall public match win percentage.
    """
    hero = resolve_hero(hero_name)
    if not hero:
        return {"error": f"Hero '{hero_name}' not found. Please verify spelling."}

    hero_id = hero["id"]
    localized_name = hero["localized_name"]

    global _HERO_STATS_CACHE
    if not _HERO_STATS_CACHE:
        stats_data = _fetch_opendota("/heroStats")
        if isinstance(stats_data, list):
            _HERO_STATS_CACHE = stats_data

    stats = None
    if _HERO_STATS_CACHE:
        stats = next((s for s in _HERO_STATS_CACHE if s.get("id") == hero_id), None)

    overview: dict[str, Any] = {
        "hero_name": localized_name,
        "hero_id": hero_id,
        "primary_attr": hero.get("primary_attr"),
        "attack_type": hero.get("attack_type"),
        "roles": hero.get("roles", []),
    }

    if stats:
        overview["base_armor"] = stats.get("base_armor")
        overview["base_attack_min"] = stats.get("base_attack_min")
        overview["base_attack_max"] = stats.get("base_attack_max")
        overview["move_speed"] = stats.get("move_speed")

        # Herald (1)
        h_pick = stats.get("1_pick", 0)
        h_win = stats.get("1_win", 0)
        overview["herald_winrate"] = round((h_win / h_pick) * 100, 2) if h_pick > 0 else None

        # Guardian (2)
        g_pick = stats.get("2_pick", 0)
        g_win = stats.get("2_win", 0)
        overview["guardian_winrate"] = round((g_win / g_pick) * 100, 2) if g_pick > 0 else None

        # Crusader (3)
        c_pick = stats.get("3_pick", 0)
        c_win = stats.get("3_win", 0)
        overview["crusader_winrate"] = round((c_win / c_pick) * 100, 2) if c_pick > 0 else None

        # Overall Pub
        pub_pick = stats.get("pub_pick", 0)
        pub_win = stats.get("pub_win", 0)
        overview["overall_pub_winrate"] = round((pub_win / pub_pick) * 100, 2) if pub_pick > 0 else None

    return overview


def get_hero_matchups(hero_name: str, enemy_heroes: list[str]) -> dict[str, Any]:
    """Retrieves empirical win rates and matchup statistics for a hero against specific enemy heroes.

    Call this tool during pre-match draft analysis to calculate exact statistical
    advantages or counter threats based on real Dota 2 match history from OpenDota.

    Args:
        hero_name: The user's hero (e.g. "Centaur Warrunner", "Slardar").
        enemy_heroes: List of enemy hero names (e.g. ["Juggernaut", "Lion", "Sniper", "Axe", "Pudge"]).

    Returns:
        A dict with:
          - 'hero': Name of the user's hero.
          - 'matchups': List of matchup analysis dicts per enemy hero, including:
              * 'enemy_hero': Enemy hero name.
              * 'winrate_vs_enemy': Percentage winrate against this enemy.
              * 'games_analyzed': Sample size of games.
              * 'verdict': 'Advantage', 'Disadvantage' (counter threat), or 'Neutral'.
          - 'biggest_counter': The enemy hero with the highest threat/disadvantage.
          - 'easiest_matchup': The enemy hero easiest to exploit.
    """
    user_hero = resolve_hero(hero_name)
    if not user_hero:
        return {"error": f"Hero '{hero_name}' not found."}

    user_id = user_hero["id"]
    matchups_data = _fetch_opendota(f"/heroes/{user_id}/matchups")
    if isinstance(matchups_data, dict) and "error" in matchups_data:
        return matchups_data

    matchup_by_id = {m.get("hero_id"): m for m in matchups_data if isinstance(m, dict)}
    results: list[dict[str, Any]] = []

    for enemy_name in enemy_heroes:
        enemy_hero = resolve_hero(enemy_name)
        if not enemy_hero:
            results.append({
                "enemy_hero": enemy_name,
                "error": "Hero unrecognized by OpenDota",
            })
            continue

        enemy_id = enemy_hero["id"]
        stats = matchup_by_id.get(enemy_id)
        if not stats or stats.get("games_played", 0) == 0:
            results.append({
                "enemy_hero": enemy_hero["localized_name"],
                "winrate_vs_enemy": 50.0,
                "games_analyzed": 0,
                "verdict": "Neutral (insufficient sample)",
            })
            continue

        games = stats["games_played"]
        wins = stats["wins"]
        winrate = round((wins / games) * 100, 2)

        if winrate >= 53.0:
            verdict = "Advantage (Favorable)"
        elif winrate <= 47.0:
            verdict = "Disadvantage (Threat / Counter)"
        else:
            verdict = "Neutral"

        results.append({
            "enemy_hero": enemy_hero["localized_name"],
            "winrate_vs_enemy": winrate,
            "games_analyzed": games,
            "verdict": verdict,
        })

    valid_matchups = [m for m in results if "winrate_vs_enemy" in m]
    biggest_counter = min(valid_matchups, key=lambda x: x["winrate_vs_enemy"])["enemy_hero"] if valid_matchups else None
    easiest_matchup = max(valid_matchups, key=lambda x: x["winrate_vs_enemy"])["enemy_hero"] if valid_matchups else None

    return {
        "hero": user_hero["localized_name"],
        "matchups": results,
        "biggest_counter": biggest_counter,
        "easiest_matchup": easiest_matchup,
    }


def get_hero_meta_items(hero_name: str) -> dict[str, Any]:
    """Fetches high-winrate and popular item builds from OpenDota for a hero.

    Args:
        hero_name: Hero name or abbreviation (e.g. "Centaur", "Axe", "Bristleback").

    Returns:
        A dict with top meta items across game phases:
          - 'start_game_items': Top starting items (0-5m).
          - 'early_game_items': Top early game items (5-15m).
          - 'mid_game_items': Top core mid game items (15-25m).
          - 'late_game_items': Top late game / luxury items (25m+).
    """
    hero = resolve_hero(hero_name)
    if not hero:
        return {"error": f"Hero '{hero_name}' not found."}

    hero_id = hero["id"]
    pop_data = _fetch_opendota(f"/heroes/{hero_id}/itemPopularity")
    if isinstance(pop_data, dict) and "error" in pop_data:
        return pop_data

    item_names = _load_or_fetch_items()

    def format_phase(phase_dict: dict[str, Any]) -> list[str]:
        if not isinstance(phase_dict, dict):
            return []
        # Sort items by frequency count descending, take top 5
        sorted_items = sorted(phase_dict.items(), key=lambda kv: kv[1], reverse=True)[:5]
        return [item_names.get(str(item_id), f"Item {item_id}") for item_id, _ in sorted_items]

    return {
        "hero": hero["localized_name"],
        "start_game_items": format_phase(pop_data.get("start_game_items", {})),
        "early_game_items": format_phase(pop_data.get("early_game_items", {})),
        "mid_game_items": format_phase(pop_data.get("mid_game_items", {})),
        "late_game_items": format_phase(pop_data.get("late_game_items", {})),
    }


def get_player_recent_matches(account_id: int = DEFAULT_ACCOUNT_ID, limit: int = 5) -> dict[str, Any]:
    """Fetches the latest matches played by a player from OpenDota.

    Use this to inspect recent performance or select a match ID to audit.

    Args:
        account_id: Dota 2 32-bit player account ID (default: 453792187).
        limit: Number of recent matches to return (default: 5, max: 20).

    Returns:
        A dict containing a list of recent matches with match_id, hero, result, KDA, and duration.
    """
    matches_raw = _fetch_opendota(f"/players/{account_id}/recentMatches")
    if isinstance(matches_raw, dict) and "error" in matches_raw:
        return matches_raw

    if not isinstance(matches_raw, list):
        return {"error": "Invalid response format from OpenDota."}

    heroes = {h["id"]: h["localized_name"] for h in _load_or_fetch_heroes()}
    parsed_matches = []

    for m in matches_raw[: min(limit, 20)]:
        player_slot = m.get("player_slot", 0)
        is_radiant = player_slot < 128
        radiant_win = bool(m.get("radiant_win"))
        won = (is_radiant and radiant_win) or (not is_radiant and not radiant_win)

        parsed_matches.append({
            "match_id": m.get("match_id"),
            "hero": heroes.get(m.get("hero_id"), f"Hero {m.get('hero_id')}"),
            "result": "WIN" if won else "LOSS",
            "kills": m.get("kills"),
            "deaths": m.get("deaths"),
            "assists": m.get("assists"),
            "duration_minutes": round(m.get("duration", 0) / 60, 1),
            "lobby_type": "Ranked" if m.get("lobby_type") == 7 else "Normal/Turbo",
        })

    return {
        "account_id": account_id,
        "recent_matches": parsed_matches,
    }


def get_match_telemetry(match_id: int, account_id: int = DEFAULT_ACCOUNT_ID) -> dict[str, Any]:
    """Retrieves full post-match telemetry for an in-depth replay and audit review.

    Extracts benchmark metrics (LH@10, KDA, GPM/XPM, lane outcome, items built, damage dealt)
    for the target player and the match outcome.

    Args:
        match_id: Dota 2 Match ID to audit.
        account_id: Dota 2 player ID to focus the audit on (default: 453792187).

    Returns:
        A detailed audit dictionary with player stats, team rosters, and performance benchmarks.
    """
    data = _fetch_opendota(f"/matches/{match_id}")
    if isinstance(data, dict) and "error" in data:
        return data

    if not isinstance(data, dict) or "players" not in data:
        return {"error": f"Failed to retrieve match {match_id} data."}

    heroes = {h["id"]: h["localized_name"] for h in _load_or_fetch_heroes()}
    items_map = _load_or_fetch_items()

    players = data.get("players", [])
    target_player = next((p for p in players if p.get("account_id") == account_id), None)
    if not target_player:
        # Fallback to the first player if account_id is not in match
        target_player = players[0] if players else {}

    target_slot = target_player.get("player_slot", 0)
    target_is_radiant = target_slot < 128
    radiant_win = bool(data.get("radiant_win"))
    match_won = (target_is_radiant and radiant_win) or (not target_is_radiant and not radiant_win)

    # Final items
    player_items = []
    for i in range(6):
        item_id = target_player.get(f"item_{i}")
        if item_id and item_id > 0:
            player_items.append(items_map.get(str(item_id), f"Item {item_id}"))

    # LH at 10 minutes
    lh_t = target_player.get("lh_t", [])
    lh_10m = lh_t[10] if isinstance(lh_t, list) and len(lh_t) > 10 else None

    # Lineups
    radiant_team = [heroes.get(p.get("hero_id"), f"Hero {p.get('hero_id')}") for p in players if p.get("player_slot", 0) < 128]
    dire_team = [heroes.get(p.get("hero_id"), f"Hero {p.get('hero_id')}") for p in players if p.get("player_slot", 0) >= 128]

    duration_sec = data.get("duration", 0)

    return {
        "match_id": match_id,
        "duration_minutes": round(duration_sec / 60, 1),
        "result": "WIN" if match_won else "LOSS",
        "player_side": "Radiant" if target_is_radiant else "Dire",
        "player_hero": heroes.get(target_player.get("hero_id"), f"Hero {target_player.get('hero_id')}"),
        "kda": f"{target_player.get('kills', 0)}/{target_player.get('deaths', 0)}/{target_player.get('assists', 0)}",
        "last_hits_total": target_player.get("last_hits", 0),
        "last_hits_10m": lh_10m if lh_10m is not None else "N/A (Turbo/Untracked)",
        "denies": target_player.get("denies", 0),
        "gpm": target_player.get("gold_per_min", 0),
        "xpm": target_player.get("xp_per_min", 0),
        "hero_damage": target_player.get("hero_damage", 0),
        "tower_damage": target_player.get("tower_damage", 0),
        "final_items": player_items,
        "radiant_lineup": radiant_team,
        "dire_lineup": dire_team,
    }

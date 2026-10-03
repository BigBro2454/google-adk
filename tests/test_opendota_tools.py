"""Tests for OpenDota tools and hero/item resolution."""

import unittest
from shared.tools.opendota_tools import (
    resolve_hero,
    get_hero_overview,
    get_hero_matchups,
    get_hero_meta_items,
    get_player_recent_matches,
    get_match_telemetry,
)


class TestOpenDotaTools(unittest.TestCase):

    def test_resolve_hero_aliases(self):
        """Verify hero aliases resolve to official hero records."""
        potm = resolve_hero("potm")
        self.assertIsNotNone(potm)
        self.assertEqual(potm["localized_name"], "Mirana")

        centaur = resolve_hero("centaur")
        self.assertIsNotNone(centaur)
        self.assertEqual(centaur["id"], 96)
        self.assertEqual(centaur["localized_name"], "Centaur Warrunner")

        jugg = resolve_hero("jugg")
        self.assertIsNotNone(jugg)
        self.assertEqual(jugg["localized_name"], "Juggernaut")

    def test_get_hero_overview(self):
        """Verify hero stats and Guardian winrate extraction."""
        overview = get_hero_overview("Centaur Warrunner")
        self.assertIn("hero_id", overview)
        self.assertEqual(overview["hero_id"], 96)
        self.assertIn("guardian_winrate", overview)
        self.assertIsNotNone(overview["guardian_winrate"])
        self.assertIn("base_armor", overview)

    def test_get_hero_matchups(self):
        """Verify matchup calculation against enemy heroes."""
        matchups = get_hero_matchups("Centaur Warrunner", ["Timbersaw", "Lion"])
        self.assertEqual(matchups["hero"], "Centaur Warrunner")
        self.assertTrue(len(matchups["matchups"]) >= 2)
        # Check that Timbersaw is evaluated as a disadvantage/counter
        timber = next(m for m in matchups["matchups"] if m["enemy_hero"] == "Timbersaw")
        self.assertIn("winrate_vs_enemy", timber)
        self.assertTrue(timber["winrate_vs_enemy"] < 50.0)

    def test_get_hero_meta_items(self):
        """Verify meta item popularity parsing."""
        items = get_hero_meta_items("Centaur")
        self.assertEqual(items["hero"], "Centaur Warrunner")
        self.assertTrue(len(items["start_game_items"]) > 0)
        self.assertTrue(len(items["mid_game_items"]) > 0)

    def test_get_player_recent_matches(self):
        """Verify fetching recent matches for profile 453792187."""
        recent = get_player_recent_matches(453792187, limit=3)
        self.assertEqual(recent["account_id"], 453792187)
        self.assertTrue(len(recent["recent_matches"]) > 0)
        first_match = recent["recent_matches"][0]
        self.assertIn("match_id", first_match)
        self.assertIn("hero", first_match)
        self.assertIn("result", first_match)

    def test_get_match_telemetry(self):
        """Verify parsing match telemetry for match 8934277316."""
        telemetry = get_match_telemetry(8934277316, 453792187)
        self.assertEqual(telemetry["match_id"], 8934277316)
        self.assertEqual(telemetry["player_hero"], "Centaur Warrunner")
        self.assertEqual(telemetry["result"], "WIN")
        self.assertIn("kda", telemetry)
        self.assertTrue(len(telemetry["final_items"]) > 0)


if __name__ == "__main__":
    unittest.main()

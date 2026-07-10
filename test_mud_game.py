import os
import unittest

from mud_game import (
    Player,
    gain_experience,
    can_use_skill,
    equip_item,
    move_player,
    explore_area,
    add_item,
    show_inventory,
    get_map,
    start_combat,
    buy_item,
    save_game,
    load_game,
)


class MudGameTests(unittest.TestCase):
    def test_leveling_grants_stat_points(self):
        player = Player(name="Ada", job="warrior")
        gain_experience(player, 100)

        self.assertEqual(player.level, 2)
        self.assertEqual(player.stat_points, 5)

    def test_warrior_skill_unlocks_with_strength(self):
        player = Player(name="Ada", job="warrior")
        player.stats["str"] = 4
        self.assertFalse(can_use_skill(player, "slash"))

        player.stats["str"] = 5
        self.assertTrue(can_use_skill(player, "slash"))

        player.stats["str"] = 10
        self.assertTrue(can_use_skill(player, "shield_bash"))

    def test_equipment_requires_matching_stats(self):
        player = Player(name="Ada", job="warrior")
        player.stats["str"] = 4
        self.assertFalse(equip_item(player, "iron_sword"))

        player.stats["str"] = 5
        self.assertTrue(equip_item(player, "iron_sword"))
        self.assertEqual(player.equipment["weapon"], "iron_sword")

    def test_move_player_between_areas(self):
        player = Player(name="Ada", job="warrior")
        self.assertTrue(move_player(player, "east"))
        self.assertEqual(player.location, "beginner_hunt")
        self.assertFalse(move_player(player, "north"))

    def test_explore_area_grants_experience(self):
        player = Player(name="Ada", job="warrior", location="beginner_hunt")
        result = explore_area(player)
        self.assertIn("사냥터", result)
        self.assertGreater(player.exp, 0)

    def test_inventory_and_map_helpers(self):
        player = Player(name="Ada", job="warrior")
        add_item(player, "healing_potion")
        self.assertIn("healing_potion", player.inventory)
        self.assertIn("마을", get_map())
        self.assertIn("인벤토리", show_inventory(player))

    def test_combat_and_shop_and_save_load(self):
        player = Player(name="Ada", job="warrior")
        result = start_combat(player)
        self.assertIn("전투", result)

        self.assertTrue(buy_item(player, "healing_potion"))
        self.assertIn("healing_potion", player.inventory)

        save_path = "test_save.json"
        save_game(player, save_path)
        self.assertTrue(os.path.exists(save_path))

        loaded = load_game(save_path)
        self.assertEqual(loaded.name, player.name)
        self.assertEqual(loaded.location, player.location)

        os.remove(save_path)


if __name__ == "__main__":
    unittest.main()

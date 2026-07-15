import random
import sys


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"

    @staticmethod
    def disable():
        for attr in dir(Color):
            if attr.isupper() and not attr.startswith("BG"):
                setattr(Color, attr, "")
        for attr in ["BG_RED", "BG_GREEN", "BG_YELLOW", "BG_BLUE"]:
            setattr(Color, attr, "")


def cprint(text, color=Color.WHITE, end="\n"):
    print(f"{color}{text}{Color.RESET}", end=end)


def cinput(text, color=Color.CYAN):
    return input(f"{color}{text}{Color.RESET}")


class Skill:
    def __init__(self, name, description, mp_cost, skill_type, power, stat_req=None):
        self.name = name
        self.description = description
        self.mp_cost = mp_cost
        self.skill_type = skill_type
        self.power = power
        self.stat_req = stat_req or {}

    def can_learn(self, character):
        for stat, req in self.stat_req.items():
            if character.get_stat(stat) < req:
                return False, f"Requires {stat.upper()} {req}"
        return True, "OK"


class Character:
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.gold = 50

        self.stats = {
            "str": 5,
            "dex": 5,
            "int": 5,
            "con": 5,
            "luck": 5
        }

        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }

        self.inventory = []
        self.equipped_items = []
        self.skills = []

    def get_stat(self, stat_name):
        base = self.stats.get(stat_name, 0)
        bonus = 0
        for item in self.equipped_items:
            if hasattr(item, 'stat_bonus'):
                bonus += item.stat_bonus.get(stat_name, 0)
        return base + bonus

    def get_attack(self):
        weapon_bonus = 0
        if self.equipment["weapon"]:
            weapon_bonus = self.equipment["weapon"].attack
        return self.get_stat("str") * 2 + weapon_bonus

    def get_magic_attack(self):
        return self.get_stat("int") * 3

    def get_defense(self):
        armor_bonus = 0
        if self.equipment["armor"]:
            armor_bonus = self.equipment["armor"].defense
        return self.get_stat("con") + armor_bonus

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.max_hp += 10
        self.max_mp += 5
        self.hp = self.max_hp
        self.mp = self.max_mp

        cprint(f"\n{'='*50}", Color.YELLOW)
        cprint(f"  {self.name} leveled up to Level {self.level}!", Color.YELLOW + Color.BOLD)
        cprint(f"{'='*50}", Color.YELLOW)
        cprint("Distribute 5 stat points:", Color.WHITE)

        points = 5
        while points > 0:
            cprint(f"\n  Points remaining: {points}", Color.GREEN)
            cprint("  1. STR - Attack damage", Color.WHITE)
            cprint("  2. DEX - Dodge chance", Color.WHITE)
            cprint("  3. INT - Magic damage", Color.WHITE)
            cprint("  4. CON - HP and defense", Color.WHITE)
            cprint("  5. LUCK - Crit chance and drops", Color.WHITE)

            choice = cinput("  Choose stat (1-5): ")
            if choice in ["1", "2", "3", "4", "5"]:
                stat_map = {"1": "str", "2": "dex", "3": "int", "4": "con", "5": "luck"}
                stat = stat_map[choice]
                self.stats[stat] += 1
                points -= 1
                cprint(f"  {stat.upper()} increased to {self.stats[stat]}!", Color.GREEN)
            else:
                cprint("  Invalid choice!", Color.RED)

        self.check_new_skills()

    def check_new_skills(self):
        all_skills = SkillLibrary.get_all()
        new_skills = [s for s in all_skills if s not in self.skills and s.can_learn(self)[0]]
        if new_skills:
            cprint(f"\n  New skills learned!", Color.MAGENTA + Color.BOLD)
            for skill in new_skills:
                self.skills.append(skill)
                cprint(f"    >> {skill.name}: {skill.description}", Color.MAGENTA)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.get_defense() // 2)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def use_mp(self, amount):
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False

    def display_status(self):
        cprint(f"\n{'='*50}", Color.BLUE)
        cprint(f"  {self.name} the {self.class_type}", Color.BLUE + Color.BOLD)
        cprint(f"  Level: {self.level} | Exp: {self.exp}/{self.exp_to_level}", Color.WHITE)
        cprint(f"{'='*50}", Color.BLUE)
        cprint(f"  HP: {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp}", Color.GREEN)
        cprint(f"  Gold: {self.gold}", Color.YELLOW)
        cprint(f"\n  Stats:", Color.WHITE + Color.BOLD)
        cprint(f"    STR: {self.get_stat('str')} | DEX: {self.get_stat('dex')} | INT: {self.get_stat('int')}", Color.WHITE)
        cprint(f"    CON: {self.get_stat('con')} | LCK: {self.get_stat('luck')}", Color.WHITE)
        cprint(f"\n  Equipment:", Color.WHITE + Color.BOLD)
        for slot, item in self.equipment.items():
            if item:
                cprint(f"    {slot.capitalize()}: {item.name}", Color.CYAN)
            else:
                cprint(f"    {slot.capitalize()}: Empty", Color.DIM)
        if self.skills:
            cprint(f"\n  Skills:", Color.WHITE + Color.BOLD)
            for skill in self.skills:
                cprint(f"    - {skill.name} ({skill.mp_cost} MP): {skill.description}", Color.MAGENTA)
        cprint(f"{'='*50}", Color.BLUE)


class Item:
    def __init__(self, name, description, item_type, **kwargs):
        self.name = name
        self.description = description
        self.item_type = item_type
        self.attack = kwargs.get("attack", 0)
        self.defense = kwargs.get("defense", 0)
        self.stat_bonus = kwargs.get("stat_bonus", {})
        self.requirements = kwargs.get("requirements", {})
        self.heal_amount = kwargs.get("heal_amount", 0)
        self.mp_amount = kwargs.get("mp_amount", 0)
        self.value = kwargs.get("value", 10)

    def can_equip(self, character):
        for stat, req_value in self.requirements.items():
            if character.get_stat(stat) < req_value:
                return False, f"Requires {stat.upper()} {req_value}"
        return True, "OK"

    def use(self, character):
        if self.item_type == "consumable":
            healed = False
            if self.heal_amount > 0:
                character.heal(self.heal_amount)
                cprint(f"  Used {self.name}. Healed {self.heal_amount} HP!", Color.GREEN)
                healed = True
            if self.mp_amount > 0:
                character.mp = min(character.max_mp, character.mp + self.mp_amount)
                cprint(f"  Used {self.name}. Restored {self.mp_amount} MP!", Color.BLUE)
                healed = True
            return healed
        return False


class Enemy:
    def __init__(self, name, level, hp, attack, defense, exp_reward, gold_reward, loot=None, skills=None):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.loot = loot or []
        self.skills = skills or []

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense // 2)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def is_alive(self):
        return self.hp > 0


class Quest:
    def __init__(self, name, description, quest_type, target, reward_exp, reward_gold, reward_item=None, target_count=1):
        self.name = name
        self.description = description
        self.quest_type = quest_type
        self.target = target
        self.target_count = target_count
        self.reward_exp = reward_exp
        self.reward_gold = reward_gold
        self.reward_item = reward_item
        self.progress = 0
        self.completed = False
        self.active = False

    def check_completion(self, character):
        if self.quest_type == "kill":
            if self.progress >= self.target_count:
                self.completed = True
                return True
        elif self.quest_type == "collect":
            count = sum(1 for item in character.inventory if item.name == self.target)
            self.progress = count
            if count >= self.target_count:
                self.completed = True
                return True
        return False


class NPC:
    def __init__(self, name, dialogue, quests=None, shop_items=None, inn=False):
        self.name = name
        self.dialogue = dialogue
        self.quests = quests or []
        self.shop_items = shop_items or []
        self.inn = inn

    def interact(self, player, quests):
        cprint(f"\n  {self.name}: \"{self.dialogue}\"", Color.CYAN + Color.BOLD)

        if self.inn:
            cprint(f"\n  [Inn] Rest and recover your strength.", Color.YELLOW)
            cprint(f"  Cost: 10 Gold | Restores full HP and MP", Color.YELLOW)
            choice = cinput("  Stay at inn? (y/n): ")
            if choice.lower() == "y":
                if player.gold >= 10:
                    player.gold -= 10
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                    cprint("  You rest peacefully. HP and MP fully restored!", Color.GREEN)
                else:
                    cprint("  Not enough gold!", Color.RED)

        available_quests = [q for q in self.quests if not q.completed and not q.active]
        active_quests = [q for q in self.quests if q.active and not q.completed]

        if active_quests:
            cprint("\n  Quest Updates:", Color.YELLOW)
            for quest in active_quests:
                quest.check_completion(player)
                if quest.completed:
                    cprint(f"    Quest completed: {quest.name}!", Color.GREEN + Color.BOLD)
                    player.exp += quest.reward_exp
                    player.gold += quest.reward_gold
                    if quest.reward_item:
                        player.inventory.append(quest.reward_item)
                        cprint(f"    Received: {quest.reward_item.name}", Color.MAGENTA)
                    cprint(f"    Rewards: {quest.reward_exp} EXP, {quest.reward_gold} Gold", Color.YELLOW)
                else:
                    cprint(f"    {quest.name}: {quest.progress}/{quest.target_count}", Color.WHITE)

        if available_quests:
            cprint("\n  Available Quests:", Color.YELLOW + Color.BOLD)
            for i, quest in enumerate(available_quests, 1):
                cprint(f"    {i}. {quest.name}", Color.WHITE + Color.BOLD)
                cprint(f"       {quest.description}", Color.WHITE)
                cprint(f"       Reward: {quest.reward_exp} EXP, {quest.reward_gold} Gold", Color.GREEN)

            choice = cinput("  Accept quest? (number or n): ")
            if choice.isdigit() and 1 <= int(choice) <= len(available_quests):
                quest = available_quests[int(choice) - 1]
                quest.active = True
                quests.append(quest)
                cprint(f"  Quest accepted: {quest.name}", Color.GREEN)

        if self.shop_items:
            cprint("\n  Shop Items:", Color.YELLOW + Color.BOLD)
            for i, item in enumerate(self.shop_items, 1):
                cprint(f"    {i}. {item.name} - {item.value} Gold", Color.WHITE)
                cprint(f"       {item.description}", Color.DIM)
                if item.requirements:
                    cprint(f"       Requires: {item.requirements}", Color.RED)

            choice = cinput("  Buy item? (number or n): ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.shop_items):
                item = self.shop_items[int(choice) - 1]
                if player.gold >= item.value:
                    player.gold -= item.value
                    player.inventory.append(item)
                    cprint(f"  Purchased {item.name}!", Color.GREEN)
                else:
                    cprint("  Not enough gold!", Color.RED)


class SkillLibrary:
    @staticmethod
    def get_all():
        return [
            Skill("Power Strike", "A heavy physical blow", 8, "physical", 2.0,
                  {"str": 8}),
            Skill("Cleave", "Sweeping attack hitting hard", 15, "physical", 3.0,
                  {"str": 14}),
            Skill("Berserk", "Wild attack with bonus damage", 25, "physical", 4.5,
                  {"str": 20, "con": 12}),
            Skill("Backstab", "Precise strike from the shadows", 10, "physical", 2.5,
                  {"dex": 10}),
            Skill("Rapid Strike", "Quick flurry of blows", 12, "physical", 2.0,
                  {"dex": 15}),
            Skill("Assassinate", "Lethal precision attack", 20, "physical", 5.0,
                  {"dex": 22, "luck": 10}),
            Skill("Fireball", "Hurls a ball of fire", 12, "magic", 2.5,
                  {"int": 8}),
            Skill("Ice Shard", "Launches a shard of ice", 10, "magic", 2.0,
                  {"int": 6}),
            Skill("Lightning Bolt", "Strikes with lightning", 20, "magic", 4.0,
                  {"int": 16}),
            Skill("Meteor", "Calls down a meteor", 35, "magic", 7.0,
                  {"int": 25}),
            Skill("Heal", "Restores HP", 10, "heal", 50,
                  {"int": 5}),
            Skill("Greater Heal", "Restores more HP", 20, "heal", 120,
                  {"int": 14}),
            Skill("War Cry", "Boosts attack with a shout", 8, "buff", 0,
                  {"str": 6, "con": 6}),
        ]


class GameMap:
    def __init__(self):
        self.locations = {
            "village": {
                "name": "Starting Village",
                "description": "A peaceful village where your adventure begins.",
                "enemies": [],
                "npcs": ["elder", "merchant", "innkeeper"],
                "exits": {"north": "forest", "east": "cave", "south": "plains"},
                "items": []
            },
            "plains": {
                "name": "Green Plains",
                "description": "Open grasslands with gentle winds.",
                "enemies": ["slime", "rat"],
                "npcs": ["hunter"],
                "exits": {"north": "village", "east": "swamp"},
                "items": ["herb"]
            },
            "forest": {
                "name": "Dark Forest",
                "description": "A dense forest filled with dangerous creatures.",
                "enemies": ["goblin", "wolf"],
                "npcs": [],
                "exits": {"south": "village", "north": "mountain", "east": "ruins"},
                "items": ["herb"]
            },
            "cave": {
                "name": "Mystic Cave",
                "description": "A dark cave with glowing crystals.",
                "enemies": ["bat", "spider"],
                "npcs": [],
                "exits": {"west": "village", "east": "dungeon", "south": "swamp"},
                "items": ["crystal"]
            },
            "swamp": {
                "name": "Murky Swamp",
                "description": "Fetid waters and twisted trees. Beware the poison.",
                "enemies": ["poison_frog", "swamp_troll"],
                "npcs": [],
                "exits": {"north": "cave", "west": "plains", "east": "dark_tower"},
                "items": ["antidote"]
            },
            "ruins": {
                "name": "Ancient Ruins",
                "description": "Crumbling stone walls hide forgotten treasures.",
                "enemies": ["skeleton", "ghost"],
                "npcs": [],
                "exits": {"west": "forest", "south": "dungeon"},
                "items": ["ancient_relic"]
            },
            "mountain": {
                "name": "Dragon Mountain",
                "description": "A treacherous mountain where dragons nest.",
                "enemies": ["wyvern", "dragon"],
                "npcs": [],
                "exits": {"south": "forest"},
                "items": []
            },
            "dungeon": {
                "name": "Ancient Dungeon",
                "description": "Ruins of an ancient civilization, overrun by monsters.",
                "enemies": ["skeleton", "zombie", "dark_knight"],
                "npcs": [],
                "exits": {"west": "cave", "north": "ruins", "east": "dark_tower"},
                "items": ["ancient_sword"]
            },
            "dark_tower": {
                "name": "Dark Tower",
                "description": "A ominous tower emanating dark energy.",
                "enemies": ["dark_mage", "shadow", "boss"],
                "npcs": [],
                "exits": {"west": "swamp", "north": "dungeon"},
                "items": []
            }
        }
        self.current_location = "village"


class Game:
    def __init__(self):
        self.player = None
        self.game_map = GameMap()
        self.quests = []
        self.items = self.create_items()
        self.enemies = self.create_enemies()
        self.npcs = self.create_npcs()

    def create_items(self):
        return {
            "health_potion": Item("Health Potion", "Restores 50 HP", "consumable",
                                 heal_amount=50, value=25),
            "mana_potion": Item("Mana Potion", "Restores 30 MP", "consumable",
                                mp_amount=30, value=20),
            "greater_health": Item("Greater Health Potion", "Restores 120 HP", "consumable",
                                   heal_amount=120, value=60),
            "antidote": Item("Antidote", "Cures poison", "consumable",
                             heal_amount=20, value=15),
            "iron_sword": Item("Iron Sword", "A sturdy iron sword", "weapon",
                               attack=10, requirements={"str": 5}, value=50),
            "steel_sword": Item("Steel Sword", "A well-crafted steel sword", "weapon",
                                attack=20, requirements={"str": 12}, value=120),
            "mithril_blade": Item("Mithril Blade", "Lightweight but deadly", "weapon",
                                  attack=28, requirements={"str": 16, "dex": 12}, value=200),
            "dragon_slayer": Item("Dragon Slayer", "Legendary anti-dragon blade", "weapon",
                                  attack=40, requirements={"str": 22, "con": 14}, value=400),
            "shadow_dagger": Item("Shadow Dagger", "Swift and silent", "weapon",
                                  attack=18, requirements={"dex": 16, "luck": 8}, value=180),
            "staff_of_flames": Item("Staff of Flames", "Channels fire magic", "weapon",
                                    attack=8, stat_bonus={"int": 8}, requirements={"int": 12}, value=150),
            "archmage_staff": Item("Archmage Staff", "Overflowing with power", "weapon",
                                   attack=12, stat_bonus={"int": 14}, requirements={"int": 20}, value=350),
            "leather_armor": Item("Leather Armor", "Basic leather protection", "armor",
                                  defense=5, requirements={"dex": 3}, value=40),
            "chain_mail": Item("Chain Mail", "Interlocking metal rings", "armor",
                               defense=15, requirements={"con": 10}, value=100),
            "plate_armor": Item("Plate Armor", "Heavy full-body armor", "armor",
                                defense=25, requirements={"str": 16, "con": 14}, value=250),
            "dragon_plate": Item("Dragon Plate", "Forged from dragon scales", "armor",
                                 defense=35, requirements={"str": 22, "con": 18}, value=500),
            "shadow_cloak": Item("Shadow Cloak", "Blends with darkness", "armor",
                                 defense=12, stat_bonus={"dex": 5, "luck": 3}, requirements={"dex": 14}, value=180),
            "magic_ring": Item("Magic Ring", "Increases intelligence", "accessory",
                               stat_bonus={"int": 3}, requirements={"int": 5}, value=80),
            "lucky_charm": Item("Lucky Charm", "Increases luck", "accessory",
                                stat_bonus={"luck": 5}, requirements={"luck": 8}, value=100),
            "warrior_amulet": Item("Warrior Amulet", "Boosts strength and con", "accessory",
                                   stat_bonus={"str": 4, "con": 3}, requirements={"str": 10}, value=120),
            "thieves_ring": Item("Thieves Ring", "Boosts dex and luck", "accessory",
                                 stat_bonus={"dex": 4, "luck": 4}, requirements={"dex": 12}, value=130),
            "crystal": Item("Magic Crystal", "A glowing crystal", "accessory",
                            stat_bonus={"int": 2, "luck": 2}, value=60),
            "herb": Item("Healing Herb", "A magical herb that heals", "consumable",
                         heal_amount=25, value=10),
            "ancient_sword": Item("Ancient Sword", "A legendary weapon", "weapon",
                                  attack=35, requirements={"str": 18, "dex": 14}, value=300),
            "ancient_relic": Item("Ancient Relic", "Mysterious artifact", "accessory",
                                  stat_bonus={"str": 3, "int": 3, "luck": 3}, value=150),
            "dragon_scale": Item("Dragon Scale", "Proof of dragon slaying", "accessory",
                                 stat_bonus={"con": 5, "str": 3}, value=200),
        }

    def create_enemies(self):
        return {
            "slime": Enemy("Slime", 1, 20, 5, 1, 10, 5),
            "rat": Enemy("Giant Rat", 1, 25, 7, 2, 12, 6),
            "goblin": Enemy("Goblin", 2, 35, 10, 3, 20, 10),
            "wolf": Enemy("Wolf", 3, 50, 14, 4, 30, 15),
            "bat": Enemy("Giant Bat", 2, 28, 9, 2, 18, 8),
            "spider": Enemy("Poison Spider", 3, 42, 13, 5, 32, 16),
            "poison_frog": Enemy("Poison Frog", 3, 30, 11, 3, 25, 12),
            "swamp_troll": Enemy("Swamp Troll", 5, 80, 18, 8, 55, 28),
            "skeleton": Enemy("Skeleton Warrior", 4, 55, 16, 7, 40, 20),
            "ghost": Enemy("Ghost", 5, 45, 20, 10, 50, 25, skills=["shadow_bolt"]),
            "wyvern": Enemy("Wyvern", 6, 120, 25, 12, 80, 40),
            "dragon": Enemy("Dragon", 8, 200, 40, 20, 200, 100,
                            loot=[self.items.get("dragon_scale")], skills=["fire_breath"]),
            "zombie": Enemy("Zombie", 5, 70, 18, 6, 45, 22),
            "dark_knight": Enemy("Dark Knight", 7, 150, 30, 18, 120, 60),
            "dark_mage": Enemy("Dark Mage", 8, 100, 35, 10, 150, 75, skills=["shadow_bolt", "dark_fireball"]),
            "shadow": Enemy("Shadow", 7, 80, 28, 15, 100, 50),
            "boss": Enemy("Dark Lord", 10, 350, 50, 25, 500, 250, skills=["shadow_bolt", "dark_fireball", "death_touch"]),
        }

    def create_npcs(self):
        elder = NPC("Village Elder",
                    "Welcome, young adventurer! Our village is in danger.",
                    quests=[
                        Quest("Goblin Trouble", "Clear out the goblins in the forest",
                              "kill", "goblin", 50, 30, target_count=3),
                        Quest("Herb Collection", "Collect 2 healing herbs from the forest",
                              "collect", "Healing Herb", 40, 20,
                              self.items["health_potion"], target_count=2)
                    ])

        merchant = NPC("Merchant",
                      "Take a look at my wares!",
                      shop_items=[
                          self.items["health_potion"],
                          self.items["mana_potion"],
                          self.items["greater_health"],
                          self.items["iron_sword"],
                          self.items["steel_sword"],
                          self.items["leather_armor"],
                          self.items["chain_mail"],
                      ])

        innkeeper = NPC("Innkeeper",
                       "Welcome to the inn! Rest here to recover your strength.",
                       inn=True)

        hunter = NPC("Hunter",
                     "The plains are dangerous. Watch out for trolls in the swamp.",
                     quests=[
                         Quest("Swamp Menace", "Defeat the Swamp Troll",
                               "kill", "swamp_troll", 80, 50, target_count=1),
                         Quest("Rat Infestation", "Clear the giant rats",
                               "kill", "rat", 30, 15, target_count=5),
                     ],
                     shop_items=[
                         self.items["antidote"],
                         self.items["shadow_dagger"],
                         self.items["thieves_ring"],
                     ])

        return {"elder": elder, "merchant": merchant, "innkeeper": innkeeper, "hunter": hunter}

    def start_game(self):
        cprint("\n" + "="*50, Color.YELLOW)
        cprint("     WELCOME TO THE TEXT RPG ADVENTURE!", Color.YELLOW + Color.BOLD)
        cprint("="*50, Color.YELLOW)

        name = cinput("\nEnter your character's name: ")
        cprint("\nChoose your class:", Color.WHITE)
        cprint("  1. Warrior  - High STR and CON", Color.RED)
        cprint("  2. Rogue    - High DEX and LUCK", Color.GREEN)
        cprint("  3. Mage     - High INT", Color.BLUE)

        class_choice = cinput("Enter choice (1-3): ")
        class_map = {"1": ("Warrior", {"str": 7, "con": 6}),
                     "2": ("Rogue", {"dex": 7, "luck": 6}),
                     "3": ("Mage", {"int": 7, "dex": 5})}

        class_name, stat_bonus = class_map.get(class_choice, ("Warrior", {"str": 7, "con": 6}))
        self.player = Character(name, class_name)

        for stat, value in stat_bonus.items():
            self.player.stats[stat] = value

        self.player.inventory.append(self.items["health_potion"])
        self.player.inventory.append(self.items["health_potion"])

        self.player.check_new_skills()

        cprint(f"\nWelcome, {name} the {class_name}!", Color.GREEN + Color.BOLD)
        self.game_loop()

    def game_loop(self):
        while self.player.is_alive():
            location = self.game_map.locations[self.game_map.current_location]
            cprint(f"\n{'='*50}", Color.BLUE)
            cprint(f"  {location['name']}", Color.BLUE + Color.BOLD)
            cprint(f"  {location['description']}", Color.WHITE)
            cprint(f"{'='*50}", Color.BLUE)

            hp_color = Color.GREEN if self.player.hp > self.player.max_hp * 0.3 else Color.RED
            cprint(f"  HP: {self.player.hp}/{self.player.max_hp}  MP: {self.player.mp}/{self.player.max_mp}  Gold: {self.player.gold}", hp_color)

            cprint("\n  Actions:", Color.WHITE + Color.BOLD)
            cprint("    1. Status      5. Explore        9. Skill List", Color.WHITE)
            cprint("    2. Inventory   6. Talk to NPC    0. Quit", Color.WHITE)
            cprint("    3. Use Item    7. Move", Color.WHITE)
            cprint("    4. Equip Item  8. Rest", Color.WHITE)

            choice = cinput("\n  > ")

            if choice == "1":
                self.player.display_status()
            elif choice == "2":
                self.view_inventory()
            elif choice == "3":
                self.use_item()
            elif choice == "4":
                self.equip_item()
            elif choice == "5":
                self.explore()
            elif choice == "6":
                self.talk_to_npc()
            elif choice == "7":
                self.move()
            elif choice == "8":
                self.rest()
            elif choice == "9":
                self.view_skill_list()
            elif choice == "0":
                cprint("\nThanks for playing!", Color.YELLOW)
                sys.exit()
            else:
                cprint("Invalid choice!", Color.RED)

        cprint("\nGame Over! You have been defeated.", Color.RED + Color.BOLD)
        cprint(f"You reached Level {self.player.level} with {self.player.gold} gold.", Color.WHITE)

    def view_skill_list(self):
        all_skills = SkillLibrary.get_all()
        cprint(f"\n{'='*50}", Color.MAGENTA)
        cprint(f"  SKILL LIST", Color.MAGENTA + Color.BOLD)
        cprint(f"{'='*50}", Color.MAGENTA)

        for skill in all_skills:
            can_learn, reason = skill.can_learn(self.player)
            learned = skill in self.player.skills
            status_color = Color.GREEN if learned else (Color.YELLOW if can_learn else Color.RED)
            status_text = "LEARNED" if learned else ("CAN LEARN" if can_learn else reason)

            cprint(f"\n  {skill.name}", Color.WHITE + Color.BOLD)
            cprint(f"    {skill.description}", Color.WHITE)
            cprint(f"    MP Cost: {skill.mp_cost} | Type: {skill.skill_type.capitalize()} | Power: {skill.power}", Color.CYAN)
            cprint(f"    Requirements: {skill.stat_req if skill.stat_req else 'None'}", Color.WHITE)
            cprint(f"    Status: {status_text}", status_color)

        cprint(f"\n{'='*50}", Color.MAGENTA)

    def view_inventory(self):
        cprint(f"\n{'='*50}", Color.CYAN)
        cprint(f"  INVENTORY", Color.CYAN + Color.BOLD)
        cprint(f"{'='*50}", Color.CYAN)
        if not self.player.inventory:
            cprint("  Empty", Color.DIM)
        else:
            for i, item in enumerate(self.player.inventory, 1):
                stats = []
                if item.attack:
                    stats.append(f"ATK+{item.attack}")
                if item.defense:
                    stats.append(f"DEF+{item.defense}")
                if item.stat_bonus:
                    stats.append(str(item.stat_bonus))
                stat_str = f" [{', '.join(stats)}]" if stats else ""
                cprint(f"  {i}. {item.name} - {item.description}{stat_str}", Color.WHITE)
        cprint(f"  Gold: {self.player.gold}", Color.YELLOW)

    def use_item(self):
        if not self.player.inventory:
            cprint("No items to use!", Color.RED)
            return

        self.view_inventory()
        choice = cinput("\nUse item number (or n): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.inventory):
                item = self.player.inventory[idx]
                if item.use(self.player):
                    self.player.inventory.remove(item)
            else:
                cprint("Invalid choice!", Color.RED)

    def equip_item(self):
        equippable = [i for i in self.player.inventory
                      if i.item_type in ["weapon", "armor", "accessory"]]

        if not equippable:
            cprint("No equippable items!", Color.RED)
            return

        cprint(f"\n{'='*50}", Color.CYAN)
        cprint(f"  EQUIPPABLE ITEMS", Color.CYAN + Color.BOLD)
        cprint(f"{'='*50}", Color.CYAN)
        for i, item in enumerate(equippable, 1):
            can_equip, reason = item.can_equip(self.player)
            status_color = Color.GREEN if can_equip else Color.RED
            status_text = "OK" if can_equip else f"BLOCKED ({reason})"
            cprint(f"  {i}. {item.name} ({item.item_type}) - {status_text}", status_color)
            details = []
            if item.attack:
                details.append(f"ATK: +{item.attack}")
            if item.defense:
                details.append(f"DEF: +{item.defense}")
            if item.stat_bonus:
                details.append(f"Bonus: {item.stat_bonus}")
            if item.requirements:
                details.append(f"Req: {item.requirements}")
            if details:
                cprint(f"      {', '.join(details)}", Color.WHITE)

        choice = cinput("\nEquip item number (or n): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(equippable):
                item = equippable[idx]
                can_equip, reason = item.can_equip(self.player)
                if can_equip:
                    old_item = self.player.equipment[item.item_type]
                    if old_item:
                        self.player.equipped_items.remove(old_item)
                        self.player.inventory.append(old_item)
                        cprint(f"  Unequipped {old_item.name}", Color.YELLOW)
                    self.player.equipment[item.item_type] = item
                    self.player.equipped_items.append(item)
                    self.player.inventory.remove(item)
                    cprint(f"  Equipped {item.name}!", Color.GREEN)
                else:
                    cprint(f"  Cannot equip: {reason}", Color.RED)

    def explore(self):
        location = self.game_map.locations[self.game_map.current_location]

        roll = random.random()

        if roll < 0.6:
            if location["enemies"]:
                enemy_type = random.choice(location["enemies"])
                enemy_template = self.enemies[enemy_type]

                level_var = random.randint(-1, 1)
                enemy_level = max(1, enemy_template.level + level_var)

                hp_mod = 1 + (level_var * 0.2)
                atk_mod = 1 + (level_var * 0.15)

                enemy = Enemy(
                    enemy_template.name,
                    enemy_level,
                    int(enemy_template.hp * hp_mod),
                    int(enemy_template.attack * atk_mod),
                    enemy_template.defense,
                    max(10, enemy_template.exp_reward + (level_var * 10)),
                    max(5, enemy_template.gold_reward + (level_var * 5)),
                    enemy_template.loot,
                    enemy_template.skills
                )

                cprint(f"\n  A wild {enemy.name} (Lv.{enemy.level}) appeared!", Color.RED + Color.BOLD)
                self.battle(enemy)
        elif roll < 0.8:
            if location["items"]:
                item_type = random.choice(location["items"])
                item = self.items[item_type]
                cprint(f"\n  You found: {item.name}!", Color.GREEN)
                self.player.inventory.append(item)
        else:
            cprint("\n  You explore but find nothing of interest.", Color.DIM)

    def battle(self, enemy):
        cprint(f"\n{'='*50}", Color.RED)
        cprint(f"  BATTLE: {self.player.name} vs {enemy.name}", Color.RED + Color.BOLD)
        cprint(f"{'='*50}", Color.RED)

        while self.player.is_alive() and enemy.is_alive():
            player_hp_color = Color.GREEN if self.player.hp > self.player.max_hp * 0.3 else Color.RED
            enemy_hp_color = Color.RED

            cprint(f"\n  {self.player.name}:", player_hp_color + Color.BOLD, end=" ")
            cprint(f"HP {self.player.hp}/{self.player.max_hp}  MP {self.player.mp}/{self.player.max_mp}", player_hp_color)
            cprint(f"  {enemy.name}:", enemy_hp_color + Color.BOLD, end=" ")
            cprint(f"HP {enemy.hp}/{enemy.max_hp}", enemy_hp_color)

            cprint("\n  Actions:", Color.WHITE)
            cprint("    1. Attack    3. Skill     5. Run", Color.WHITE)
            cprint("    2. Item      4. Defend", Color.WHITE)

            choice = cinput("\n  > ")

            if choice == "1":
                self.battle_attack(enemy, False)
            elif choice == "2":
                self.battle_item(enemy)
                continue
            elif choice == "3":
                if not self.player.skills:
                    cprint("  No skills learned!", Color.RED)
                    continue
                self.battle_skill(enemy)
            elif choice == "4":
                cprint(f"  {self.player.name} takes a defensive stance!", Color.CYAN)
                reduced = self.player.take_damage(enemy.attack // 2)
                cprint(f"  {enemy.name} attacks for {reduced} damage (reduced)!", Color.YELLOW)
                continue
            elif choice == "5":
                if random.random() < 0.5 + self.player.get_stat("dex") / 100:
                    cprint("  You escaped successfully!", Color.GREEN)
                    return
                else:
                    cprint("  Failed to escape!", Color.RED)
            else:
                cprint("  Invalid choice!", Color.RED)
                continue

            if enemy.is_alive():
                self.enemy_turn(enemy)

        if self.player.is_alive():
            cprint(f"\n  Victory! You defeated {enemy.name}!", Color.GREEN + Color.BOLD)
            cprint(f"  Gained {enemy.exp_reward} EXP and {enemy.gold_reward} Gold", Color.YELLOW)
            self.player.exp += enemy.exp_reward
            self.player.gold += enemy.gold_reward

            for quest in self.quests:
                if quest.quest_type == "kill" and quest.active and not quest.completed:
                    quest.progress += 1
                    cprint(f"  Quest progress: {quest.progress}/{quest.target_count}", Color.YELLOW)

            if random.random() < 0.15 + self.player.get_stat("luck") / 100:
                if enemy.loot:
                    loot = random.choice(enemy.loot)
                    if loot:
                        self.player.inventory.append(loot)
                        cprint(f"  Found special item: {loot.name}!", Color.MAGENTA + Color.BOLD)

            while self.player.exp >= self.player.exp_to_level:
                self.player.level_up()

    def battle_attack(self, enemy, is_magic):
        if random.random() < self.player.get_stat("dex") / 150:
            cprint(f"  {enemy.name} dodged your attack!", Color.YELLOW)
            return

        if is_magic:
            damage = self.player.get_magic_attack() + random.randint(-3, 6)
        else:
            damage = self.player.get_attack() + random.randint(-2, 5)

        crit = random.random() < self.player.get_stat("luck") / 100
        if crit:
            damage = int(damage * 1.8)
            cprint(f"  CRITICAL HIT!", Color.RED + Color.BOLD)

        actual_dmg = enemy.take_damage(damage)
        attack_word = "magically struck" if is_magic else "dealt"
        cprint(f"  You {attack_word} {actual_dmg} damage to {enemy.name}!", Color.GREEN)

    def battle_skill(self, enemy):
        cprint("\n  Skills:", Color.MAGENTA + Color.BOLD)
        for i, skill in enumerate(self.player.skills, 1):
            can_use = Color.GREEN + "OK" if self.player.mp >= skill.mp_cost else Color.RED + "NO MP"
            cprint(f"    {i}. {skill.name} ({skill.mp_cost} MP) [{can_use}]", Color.WHITE)
            cprint(f"       {skill.description}", Color.DIM)

        choice = cinput("\n  Use skill (number or n): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.skills):
                skill = self.player.skills[idx]
                if self.player.use_mp(skill.mp_cost):
                    if skill.skill_type == "physical":
                        damage = int(self.player.get_attack() * skill.power + random.randint(-3, 8))
                        crit = random.random() < self.player.get_stat("luck") / 100
                        if crit:
                            damage = int(damage * 1.8)
                            cprint(f"  CRITICAL HIT!", Color.RED + Color.BOLD)
                        actual_dmg = enemy.take_damage(damage)
                        cprint(f"  {skill.name}! You deal {actual_dmg} damage!", Color.GREEN)
                    elif skill.skill_type == "magic":
                        damage = int(self.player.get_magic_attack() * skill.power + random.randint(-5, 10))
                        crit = random.random() < self.player.get_stat("luck") / 100
                        if crit:
                            damage = int(damage * 1.8)
                            cprint(f"  CRITICAL HIT!", Color.RED + Color.BOLD)
                        actual_dmg = enemy.take_damage(damage)
                        cprint(f"  {skill.name}! You deal {actual_dmg} magic damage!", Color.BLUE)
                    elif skill.skill_type == "heal":
                        heal_amount = int(skill.power + self.player.get_stat("int") * 2)
                        self.player.heal(heal_amount)
                        cprint(f"  {skill.name}! You heal {heal_amount} HP!", Color.GREEN)
                    elif skill.skill_type == "buff":
                        cprint(f"  {skill.name}! You feel empowered!", Color.YELLOW)
                else:
                    cprint("  Not enough MP!", Color.RED)
                    return

    def battle_item(self, enemy):
        consumables = [i for i in self.player.inventory if i.item_type == "consumable"]
        if consumables:
            cprint("\n  Items:", Color.YELLOW)
            for i, item in enumerate(consumables, 1):
                cprint(f"    {i}. {item.name}", Color.WHITE)
            item_choice = cinput("  Use item: ")
            if item_choice.isdigit() and 1 <= int(item_choice) <= len(consumables):
                item = consumables[int(item_choice) - 1]
                item.use(self.player)
                self.player.inventory.remove(item)
        else:
            cprint("  No consumables!", Color.RED)

    def enemy_turn(self, enemy):
        if enemy.skills and random.random() < 0.4:
            skill_name = random.choice(enemy.skills)
            damage = enemy.attack + random.randint(5, 15)
            if skill_name == "fire_breath":
                damage = int(damage * 1.5)
                cprint(f"\n  {enemy.name} uses Fire Breath!", Color.RED + Color.BOLD)
            elif skill_name == "shadow_bolt":
                damage = int(damage * 1.3)
                cprint(f"\n  {enemy.name} casts Shadow Bolt!", Color.MAGENTA + Color.BOLD)
            elif skill_name == "dark_fireball":
                damage = int(damage * 1.8)
                cprint(f"\n  {enemy.name} hurls a Dark Fireball!", Color.RED + Color.BOLD)
            elif skill_name == "death_touch":
                damage = int(damage * 2.0)
                cprint(f"\n  {enemy.name} uses Death Touch!", Color.RED + Color.BOLD)
            else:
                cprint(f"\n  {enemy.name} uses {skill_name}!", Color.RED)
            actual_dmg = self.player.take_damage(damage)
            cprint(f"  You take {actual_dmg} damage!", Color.RED)
        else:
            enemy_dmg = enemy.attack + random.randint(-2, 3)
            actual_dmg = self.player.take_damage(enemy_dmg)
            cprint(f"\n  {enemy.name} attacks for {actual_dmg} damage!", Color.RED)

    def talk_to_npc(self):
        location = self.game_map.locations[self.game_map.current_location]
        npcs_here = location["npcs"]

        if not npcs_here:
            cprint("No one around to talk to.", Color.DIM)
            return

        cprint("\n  NPCs here:", Color.WHITE + Color.BOLD)
        for i, npc_name in enumerate(npcs_here, 1):
            cprint(f"    {i}. {npc_name.capitalize()}", Color.CYAN)

        choice = cinput("  Talk to (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(npcs_here):
            npc_name = npcs_here[int(choice) - 1]
            npc = self.npcs[npc_name]
            npc.interact(self.player, self.quests)

    def move(self):
        location = self.game_map.locations[self.game_map.current_location]
        exits = location["exits"]

        cprint("\n  Exits:", Color.WHITE + Color.BOLD)
        for direction, dest in exits.items():
            dest_loc = self.game_map.locations[dest]
            cprint(f"    {direction.capitalize():>6} -> {dest_loc['name']}", Color.CYAN)

        choice = cinput("\n  Move to (direction): ").lower()
        if choice in exits:
            self.game_map.current_location = exits[choice]
            new_loc = self.game_map.locations[self.game_map.current_location]
            cprint(f"\n  You travel {choice} to {new_loc['name']}...", Color.YELLOW)
        else:
            cprint("  Can't go that way!", Color.RED)

    def rest(self):
        cprint("\n  [Rest] Recover your strength at the inn.", Color.YELLOW)
        cprint("  Cost: 10 Gold | Restores full HP and MP", Color.YELLOW)
        choice = cinput("  Rest now? (y/n): ")
        if choice.lower() == "y":
            if self.player.gold >= 10:
                self.player.gold -= 10
                self.player.hp = self.player.max_hp
                self.player.mp = self.player.max_mp
                cprint("  You rest peacefully. HP and MP fully restored!", Color.GREEN)
            else:
                cprint("  Not enough gold to rest! (Need 10 Gold)", Color.RED)


if __name__ == "__main__":
    game = Game()
    game.start_game()

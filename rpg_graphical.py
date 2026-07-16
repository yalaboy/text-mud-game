import random
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Adventure")

BG_COLOR = (30, 30, 50)
TEXT_COLOR = (220, 220, 220)
RED = (220, 50, 50)
GREEN = (50, 200, 80)
BLUE = (80, 130, 220)
YELLOW = (220, 200, 50)
CYAN = (50, 200, 220)
MAGENTA = (200, 80, 200)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 80)
BTN_COLOR = (70, 70, 110)
BTN_HOVER = (100, 100, 160)
BTN_ACTIVE = (140, 80, 180)

font = pygame.font.Font(None, 28)
font_sm = pygame.font.Font(None, 22)
font_lg = pygame.font.Font(None, 42)
font_xl = pygame.font.Font(None, 56)

class Button:
    def __init__(self, x, y, w, h, text, color=BTN_COLOR):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hovered = False
        self.visible = True
        self.enabled = True

    def draw(self, surf):
        if not self.visible:
            return
        c = BTN_HOVER if self.hovered else (self.color if self.enabled else DARK_GRAY)
        pygame.draw.rect(surf, c, self.rect, border_radius=8)
        pygame.draw.rect(surf, (180, 180, 220) if self.enabled else GRAY, self.rect, 2, border_radius=8)
        tc = TEXT_COLOR if self.enabled else GRAY
        txt = font.render(self.text, True, tc)
        surf.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos) if self.visible and self.enabled else False

    def clicked(self, pos):
        return self.rect.collidepoint(pos) and self.visible and self.enabled


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
        self.stats = {"str": 5, "dex": 5, "int": 5, "con": 5, "luck": 5}
        self.equipment = {"weapon": None, "armor": None, "accessory": None}
        self.inventory = []
        self.equipped_items = []
        self.skills = []

    def get_stat(self, s):
        base = self.stats.get(s, 0)
        bonus = sum(item.stat_bonus.get(s, 0) for item in self.equipped_items if hasattr(item, 'stat_bonus'))
        return base + bonus

    def get_attack(self):
        wb = self.equipment["weapon"].attack if self.equipment["weapon"] else 0
        return self.get_stat("str") * 2 + wb

    def get_magic_attack(self):
        return self.get_stat("int") * 3

    def get_defense(self):
        ab = self.equipment["armor"].defense if self.equipment["armor"] else 0
        return self.get_stat("con") + ab

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.max_hp += 10
        self.max_mp += 5
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.stats["str"] += 1
        self.stats["dex"] += 1
        self.stats["int"] += 1
        self.stats["con"] += 1
        self.stats["luck"] += 1
        self.check_new_skills()

    def check_new_skills(self):
        for sk in ALL_SKILLS:
            if sk not in self.skills and all(self.get_stat(s) >= v for s, v in sk.stat_req.items()):
                self.skills.append(sk)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        actual = max(1, dmg - self.get_defense() // 2)
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amt):
        self.hp = min(self.max_hp, self.hp + amt)


class Skill:
    def __init__(self, name, desc, mp_cost, stype, power, stat_req=None):
        self.name = name
        self.desc = desc
        self.mp_cost = mp_cost
        self.stype = stype
        self.power = power
        self.stat_req = stat_req or {}


ALL_SKILLS = [
    Skill("Power Strike", "Heavy physical blow", 8, "physical", 2.0, {"str": 8}),
    Skill("Cleave", "Sweeping arc attack", 15, "physical", 3.0, {"str": 14}),
    Skill("Backstab", "Precision strike from behind", 10, "physical", 2.5, {"dex": 10}),
    Skill("Whirlwind", "Spinning blade attack", 18, "physical", 2.8, {"str": 12, "dex": 8}),
    Skill("Shield Bash", "Slam with your shield", 6, "physical", 1.5, {"con": 6}),
    Skill("Execute", "Devastating finishing blow", 25, "physical", 4.0, {"str": 18}),
    Skill("Piercing Thrust", "Ignores some armor", 12, "physical", 2.2, {"dex": 12}),
    Skill("Skull Crusher", "Stuns on impact", 14, "physical", 2.6, {"str": 10, "con": 6}),
    Skill("Dual Strike", "Two fast slashes", 11, "physical", 1.8, {"dex": 14}),
    Skill("Berserker Rage", "Frenzied attacks", 20, "physical", 3.5, {"str": 16, "con": 10}),
    Skill("Sunder Armor", "Breaks enemy defenses", 13, "physical", 2.0, {"str": 11}),
    Skill("Frenzy", "Attack speed boost", 16, "physical", 2.4, {"dex": 11, "str": 9}),
    Skill("Impale", "Deep penetrating strike", 19, "physical", 3.2, {"str": 15, "dex": 10}),
    Skill("Rage Slash", "Stronger when hurt", 14, "physical", 2.7, {"str": 13}),
    Skill("Titan Strike", "Earth-shaking blow", 28, "physical", 4.5, {"str": 20, "con": 12}),
    Skill("Fireball", "Launch a ball of fire", 12, "magic", 2.5, {"int": 8}),
    Skill("Ice Shard", "Freezing ice projectile", 10, "magic", 2.0, {"int": 6}),
    Skill("Lightning Bolt", "Chain of lightning", 20, "magic", 4.0, {"int": 16}),
    Skill("Shadow Bolt", "Dark energy projectile", 14, "magic", 2.8, {"int": 10}),
    Skill("Arcane Burst", "Raw magical explosion", 22, "magic", 3.5, {"int": 14}),
    Skill("Frost Nova", "Freeze everything nearby", 18, "magic", 3.0, {"int": 12}),
    Skill("Chain Lightning", "Bounces between targets", 24, "magic", 3.8, {"int": 18}),
    Skill("Inferno", "Raging firestorm", 26, "magic", 4.2, {"int": 17}),
    Skill("Blizzard", "Piercing ice storm", 21, "magic", 3.3, {"int": 15}),
    Skill("Void Pulse", "Dark energy wave", 16, "magic", 2.9, {"int": 11}),
    Skill("Meteor", "Call a meteor from sky", 30, "magic", 5.0, {"int": 20}),
    Skill("Thunder Clap", "Shockwave of thunder", 17, "magic", 3.1, {"int": 13}),
    Skill("Acid Rain", "Corrosive rain damage", 15, "magic", 2.7, {"int": 9}),
    Skill("Rune Blast", "Detonates inscribed runes", 19, "magic", 3.4, {"int": 14, "dex": 6}),
    Skill("Eldritch Beam", "Focused beam of magic", 28, "magic", 4.8, {"int": 19}),
    Skill("Heal", "Restore HP", 10, "heal", 50, {"int": 5}),
    Skill("Greater Heal", "Strong healing", 18, "heal", 100, {"int": 12}),
    Skill("Rejuvenate", "Heal over time", 14, "heal", 70, {"int": 9}),
    Skill("Holy Light", "Divine healing radiance", 22, "heal", 130, {"int": 16}),
    Skill("Blood Drain", "Steal life from enemy", 16, "magic", 2.2, {"int": 10, "luck": 5}),
    Skill("Life Surge", "Heal based on missing HP", 20, "heal", 110, {"int": 14, "con": 8}),
    Skill("Regeneration", "Long-lasting regeneration", 25, "heal", 150, {"int": 18}),
    Skill("Purify", "Cleanse and heal wounds", 8, "heal", 35, {"int": 4}),
    Skill("Nature's Touch", "Heal from nature's power", 12, "heal", 60, {"int": 7, "con": 5}),
    Skill("Resurrection Light", "Massive heal from beyond", 35, "heal", 200, {"int": 22}),
    Skill("Battle Cry", "Boost attack power", 10, "buff", 1.5, {"str": 8, "con": 5}),
    Skill("Iron Skin", "Temporarily harden skin", 12, "buff", 2.0, {"con": 10}),
    Skill("Haste", "Increase dodge chance", 14, "buff", 1.8, {"dex": 12}),
    Skill("Arcane Shield", "Absorb magic damage", 16, "buff", 2.5, {"int": 13}),
    Skill("War Drums", "Boost all stats briefly", 22, "buff", 1.3, {"str": 10, "int": 8}),
    Skill("Weaken", "Reduce enemy attack", 8, "debuff", 0.7, {"int": 6}),
    Skill("Slow", "Reduce enemy speed", 10, "debuff", 0.6, {"int": 8}),
    Skill("Curse", "Lowers enemy luck", 12, "debuff", 0.5, {"int": 10}),
    Skill("Armor Break", "Shatter enemy armor", 14, "debuff", 0.4, {"str": 12, "int": 6}),
    Skill("Siphon Mana", "Drain enemy MP", 18, "debuff", 0.3, {"int": 15}),
]


class Item:
    def __init__(self, name, desc, itype, **kw):
        self.name = name
        self.desc = desc
        self.itype = itype
        self.attack = kw.get("attack", 0)
        self.defense = kw.get("defense", 0)
        self.stat_bonus = kw.get("stat_bonus", {})
        self.requirements = kw.get("requirements", {})
        self.heal_amount = kw.get("heal_amount", 0)
        self.mp_amount = kw.get("mp_amount", 0)
        self.value = kw.get("value", 10)

    def can_equip(self, ch):
        return all(ch.get_stat(s) >= v for s, v in self.requirements.items())


def make_items():
    return {
        "hp_pot": Item("Health Potion", "Restores 50 HP", "consumable", heal_amount=50, value=25),
        "mp_pot": Item("Mana Potion", "Restores 30 MP", "consumable", mp_amount=30, value=20),
        "herb": Item("Healing Herb", "Heals 25 HP", "consumable", heal_amount=25, value=10),
        "hi_pot": Item("Hi-Potion", "Restores 120 HP", "consumable", heal_amount=120, value=60),
        "ether": Item("Ether", "Restores 60 MP", "consumable", mp_amount=60, value=50),
        "elixir": Item("Elixir", "Restores 200 HP+100 MP", "consumable", heal_amount=200, mp_amount=100, value=150),
        "antidote": Item("Antidote", "Cures poison", "consumable", heal_amount=10, value=8),
        "bomb": Item("Bomb", "Deals 80 damage", "consumable", value=40),
        "smoke_bomb": Item("Smoke Bomb", "Escape battle", "consumable", value=30),
        "phoenix_down": Item("Phoenix Down", "Revive with 1 HP", "consumable", value=100),
        "iron_sword": Item("Iron Sword", "Sturdy sword", "weapon", attack=10, requirements={"str": 5}, value=50),
        "steel_sword": Item("Steel Sword", "Well-crafted blade", "weapon", attack=20, requirements={"str": 12}, value=120),
        "shadow_dag": Item("Shadow Dagger", "Swift dark dagger", "weapon", attack=18, requirements={"dex": 16}, value=180),
        "staff_flame": Item("Staff of Flames", "Channels fire magic", "weapon", attack=8, stat_bonus={"int": 8}, requirements={"int": 12}, value=150),
        "warhammer": Item("Warhammer", "Crushing force", "weapon", attack=25, requirements={"str": 18}, value=200),
        "crystal_wand": Item("Crystal Wand", "Amplifies magic", "weapon", attack=6, stat_bonus={"int": 12}, requirements={"int": 15}, value=220),
        "assassin_blade": Item("Assassin Blade", "Venomous edge", "weapon", attack=22, stat_bonus={"dex": 5}, requirements={"dex": 14}, value=250),
        "thunder_axe": Item("Thunder Axe", "Crackles lightning", "weapon", attack=28, stat_bonus={"str": 3}, requirements={"str": 16, "con": 8}, value=300),
        "flame_tongue": Item("Flame Tongue", "Blade wreathed in fire", "weapon", attack=30, stat_bonus={"int": 4}, requirements={"str": 14, "int": 8}, value=350),
        "void_staff": Item("Void Staff", "Draws power from darkness", "weapon", attack=10, stat_bonus={"int": 16}, requirements={"int": 20}, value=400),
        "dragon_bone": Item("Dragon Bone Sword", "Forged from dragon remains", "weapon", attack=35, stat_bonus={"str": 5, "con": 3}, requirements={"str": 20, "con": 12}, value=500),
        "moonblade": Item("Moonblade", "Silver glowing blade", "weapon", attack=32, stat_bonus={"luck": 6}, requirements={"dex": 18, "luck": 10}, value=450),
        "rune_dagger": Item("Rune Dagger", "Etched with runes", "weapon", attack=16, stat_bonus={"int": 6, "dex": 4}, requirements={"int": 8, "dex": 10}, value=160),
        "great_mace": Item("Great Mace", "Devastating blunt weapon", "weapon", attack=38, requirements={"str": 22, "con": 14}, value=550),
        "elven_bow": Item("Elven Bow", "Graceful and deadly", "weapon", attack=24, stat_bonus={"dex": 8}, requirements={"dex": 16}, value=280),
        "soul_reaper": Item("Soul Reaper", "Drains life on hit", "weapon", attack=40, stat_bonus={"luck": 4}, requirements={"str": 18, "luck": 8}, value=600),
        "arcane_scepter": Item("Arcane Scepter", "Pure magical focus", "weapon", attack=12, stat_bonus={"int": 20}, requirements={"int": 22}, value=650),
        "shadow_katana": Item("Shadow Katana", "Cuts through shadow", "weapon", attack=28, stat_bonus={"dex": 10, "luck": 5}, requirements={"dex": 20, "luck": 8}, value=480),
        "leather": Item("Leather Armor", "Basic protection", "armor", defense=5, requirements={"dex": 3}, value=40),
        "chain": Item("Chain Mail", "Metal ring links", "armor", defense=15, requirements={"con": 10}, value=100),
        "plate": Item("Plate Armor", "Heavy full-body", "armor", defense=25, requirements={"str": 16, "con": 14}, value=250),
        "mithril": Item("Mithril Vest", "Light yet strong", "armor", defense=20, stat_bonus={"dex": 4}, requirements={"dex": 12}, value=300),
        "dragon_scale": Item("Dragon Scale Mail", "Near-impenetrable", "armor", defense=35, stat_bonus={"con": 5}, requirements={"str": 18, "con": 16}, value=500),
        "shadow_cloak": Item("Shadow Cloak", "Blends with darkness", "armor", defense=12, stat_bonus={"dex": 8, "luck": 4}, requirements={"dex": 14, "luck": 6}, value=280),
        "holy_vestment": Item("Holy Vestment", "Blessed robes", "armor", defense=18, stat_bonus={"int": 6}, requirements={"int": 10}, value=260),
        "iron_bulwark": Item("Iron Bulwark", "Thick iron plate", "armor", defense=30, requirements={"str": 14, "con": 18}, value=400),
        "phantom_robe": Item("Phantom Robe", "Phase through attacks", "armor", defense=14, stat_bonus={"int": 10}, requirements={"int": 16}, value=350),
        "battle_plate": Item("Battle Plate", "Scarred from wars", "armor", defense=28, stat_bonus={"str": 3, "con": 3}, requirements={"str": 16, "con": 14}, value=380),
        "celestial_robe": Item("Celestial Robe", "Woven from starlight", "armor", defense=22, stat_bonus={"int": 12, "luck": 3}, requirements={"int": 18, "luck": 6}, value=550),
        "void_armor": Item("Void Armor", "Forged in the abyss", "armor", defense=32, stat_bonus={"con": 6, "str": 4}, requirements={"str": 18, "con": 16}, value=580),
        "magic_ring": Item("Magic Ring", "+3 INT", "accessory", stat_bonus={"int": 3}, requirements={"int": 5}, value=80),
        "lucky_charm": Item("Lucky Charm", "+5 LCK", "accessory", stat_bonus={"luck": 5}, requirements={"luck": 8}, value=100),
        "warrior_band": Item("Warrior Band", "+4 STR +2 CON", "accessory", stat_bonus={"str": 4, "con": 2}, requirements={"str": 8}, value=120),
        "rogue_pendant": Item("Rogue Pendant", "+5 DEX +3 LCK", "accessory", stat_bonus={"dex": 5, "luck": 3}, requirements={"dex": 10}, value=140),
        "amulet_flames": Item("Amulet of Flames", "+8 INT +2 STR", "accessory", stat_bonus={"int": 8, "str": 2}, requirements={"int": 12}, value=200),
        "ring_fortitude": Item("Ring of Fortitude", "+6 CON +3 STR", "accessory", stat_bonus={"con": 6, "str": 3}, requirements={"con": 12}, value=180),
        "eye_of_truth": Item("Eye of Truth", "+10 INT +4 LCK", "accessory", stat_bonus={"int": 10, "luck": 4}, requirements={"int": 16}, value=300),
        "berserker_ring": Item("Berserker Ring", "+8 STR +4 DEX", "accessory", stat_bonus={"str": 8, "dex": 4}, requirements={"str": 14}, value=260),
        "shadow_amulet": Item("Shadow Amulet", "+6 DEX +6 LCK", "accessory", stat_bonus={"dex": 6, "luck": 6}, requirements={"dex": 14, "luck": 10}, value=350),
        "crown_sovereign": Item("Crown of Sovereign", "+5 all stats", "accessory", stat_bonus={"str": 5, "dex": 5, "int": 5, "con": 5, "luck": 5}, requirements={"str": 12, "int": 12}, value=500),
    }

ITEMS = make_items()

def make_enemies():
    return {
        "slime": ("Slime", 1, 20, 5, 1, 10, 5),
        "rat": ("Giant Rat", 1, 25, 7, 2, 12, 6),
        "goblin": ("Goblin", 2, 35, 10, 3, 20, 10),
        "wolf": ("Wolf", 3, 50, 14, 4, 30, 15),
        "bat": ("Giant Bat", 2, 28, 9, 2, 18, 8),
        "spider": ("Poison Spider", 3, 42, 13, 5, 32, 16),
        "swamp_troll": ("Swamp Troll", 5, 80, 18, 8, 55, 28),
        "skeleton": ("Skeleton", 4, 55, 16, 7, 40, 20),
        "dragon": ("Dragon", 8, 200, 40, 20, 200, 100),
        "dark_knight": ("Dark Knight", 7, 150, 30, 18, 120, 60),
        "dark_mage": ("Dark Mage", 8, 100, 35, 10, 150, 75),
        "boss": ("Dark Lord", 10, 350, 50, 25, 500, 250),
    }

ENEMIES = make_enemies()

class Quest:
    def __init__(self, name, desc, req_level, gold_reward, xp_reward, req_type, req_target, req_amount):
        self.name = name
        self.desc = desc
        self.req_level = req_level
        self.gold_reward = gold_reward
        self.xp_reward = xp_reward
        self.req_type = req_type  # kill, collect, visit, level, gold
        self.req_target = req_target
        self.req_amount = req_amount

QUESTS = [
    Quest("Rat Problem", "Slay 3 rats in the plains", 1, 50, 40, "kill", "rat", 3),
    Quest("Goblin Hunter", "Defeat 5 goblins", 2, 80, 80, "kill", "goblin", 5),
    Quest("Spider Slayer", "Clear out 4 spiders from the cave", 3, 100, 100, "kill", "spider", 4),
    Quest("Wolf Pack", "Thin the wolf pack - kill 6", 4, 150, 140, "kill", "wolf", 6),
    Quest("Dragon Slayer", "Defeat 2 dragons", 8, 500, 400, "kill", "dragon", 2),
    Quest("Dark Knight's Bane", "Destroy 3 dark knights", 7, 300, 280, "kill", "dark_knight", 3),
    Quest("Gather Herbs", "Find 5 healing herbs", 1, 40, 30, "collect", "herb", 5),
    Quest("Potion Collector", "Collect 3 health potions", 2, 60, 50, "collect", "hp_pot", 3),
    Quest("Herb Master", "Gather 10 herbs for the Elder", 3, 120, 100, "collect", "herb", 10),
    Quest("Explore Forest", "Visit the Dark Forest", 1, 30, 40, "visit", "forest", 1),
    Quest("Cave Explorer", "Venture into the Mystic Cave", 2, 50, 60, "visit", "cave", 1),
    Quest("Dragon's Lair", "Reach Dragon Mountain", 6, 200, 150, "visit", "mountain", 1),
    Quest("Reach Level 5", "Train until level 5", 1, 100, 80, "level", 5, 1),
    Quest("Reach Level 8", "Advance to level 8", 5, 250, 200, "level", 8, 1),
    Quest("Reach Level 10", "Become a true warrior", 8, 500, 400, "level", 10, 1),
    Quest("Accumulate Wealth", "Save 500 gold", 1, 100, 60, "gold", 500, 1),
    Quest("Dragon's Hoard", "Collect 2000 gold", 5, 300, 200, "gold", 2000, 1),
    Quest("Grand Master", "Reach level 12 and defeat the Dark Lord", 10, 1000, 800, "level", 12, 1),
]

MAP = {
    "village": {"name": "Starting Village", "desc": "A peaceful village.", "enemies": [], "npcs": ["Elder", "Merchant"], "exits": {"N": "forest", "E": "cave", "S": "plains"}},
    "plains": {"name": "Green Plains", "desc": "Open grasslands.", "enemies": ["slime", "rat"], "npcs": [], "exits": {"N": "village", "E": "swamp"}},
    "forest": {"name": "Dark Forest", "desc": "Dangerous forest.", "enemies": ["goblin", "wolf"], "npcs": [], "exits": {"S": "village", "N": "mountain"}},
    "cave": {"name": "Mystic Cave", "desc": "Glowing crystals.", "enemies": ["bat", "spider"], "npcs": [], "exits": {"W": "village", "E": "dungeon"}},
    "swamp": {"name": "Murky Swamp", "desc": "Beware poison.", "enemies": ["swamp_troll"], "npcs": [], "exits": {"W": "plains", "N": "cave"}},
    "mountain": {"name": "Dragon Mountain", "desc": "Dragons nest here.", "enemies": ["dragon"], "npcs": [], "exits": {"S": "forest"}},
    "dungeon": {"name": "Ancient Dungeon", "desc": "Overrun by monsters.", "enemies": ["skeleton", "dark_knight"], "npcs": [], "exits": {"W": "cave", "E": "tower"}},
    "tower": {"name": "Dark Tower", "desc": "Dark energy.", "enemies": ["dark_mage", "boss"], "npcs": [], "exits": {"W": "swamp"}},
}

DIR_MAP = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

HERB_LOCATIONS = {"plains", "forest", "swamp"}

MAP_POSITIONS = {
    "village": (2, 2), "forest": (2, 1), "mountain": (2, 0),
    "plains": (1, 2), "cave": (3, 2), "dungeon": (4, 2),
    "swamp": (1, 3), "tower": (4, 3),
}
MAP_CONNECTIONS = [
    ("village", "forest"), ("village", "cave"), ("village", "plains"),
    ("forest", "mountain"), ("plains", "swamp"), ("cave", "dungeon"),
    ("cave", "swamp"), ("dungeon", "tower"),
]


class Enemy:
    def __init__(self, name, level, hp, atk, dfn, exp_r, gold_r):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attack = atk
        self.defense = dfn
        self.exp_reward = exp_r
        self.gold_reward = gold_r

    def take_damage(self, dmg):
        actual = max(1, dmg - self.defense // 2)
        self.hp = max(0, self.hp - actual)
        return actual

    def is_alive(self):
        return self.hp > 0


class Game:
    def __init__(self):
        self.state = "menu"
        self.player = None
        self.location = "village"
        self.enemy = None
        self.message = ""
        self.msg_timer = 0
        self.buttons = []
        self.scroll_offset = 0
        self.visited = {"village"}
        self.create_buttons()
        self.name_input = ""
        self.naming = False
        self.quest_status = {}  # quest_idx -> "active"/"completed"
        self.active_quests = []
        self.kill_counts = {}
        self.battle_count = 0
        self.last_killed_enemy = None

    def create_buttons(self):
        self.buttons = []
        bw, bh = 200, 45
        cx = WIDTH // 2 - bw // 2

        if self.state == "menu":
            self.buttons = [
                Button(cx, 350, bw, bh, "Start Game"),
                Button(cx, 410, bw, bh, "Quit"),
            ]
        elif self.state == "class_select":
            self.buttons = [
                Button(cx, 350, bw, bh, "Warrior", RED),
                Button(cx, 410, bw, bh, "Rogue", GREEN),
                Button(cx, 470, bw, bh, "Mage", BLUE),
            ]
        elif self.state == "naming":
            self.buttons = [
                Button(cx, 420, bw, bh, "Confirm"),
            ]
        elif self.state == "main":
            bw2 = 160
            self.buttons = [
                Button(30, 560, bw2, 40, "Status"),
                Button(200, 560, bw2, 40, "Inventory"),
                Button(370, 560, bw2, 40, "Explore"),
                Button(540, 560, bw2, 40, "Move"),
                Button(710, 560, bw2, 40, "Talk"),
                Button(30, 615, bw2, 40, "Skills"),
                Button(200, 615, bw2, 40, "Use Item"),
                Button(370, 615, bw2, 40, "Equip"),
                Button(540, 615, bw2, 40, "Rest"),
                Button(710, 615, bw2, 40, "Quit"),
            ]
        elif self.state == "inventory":
            self.buttons = [Button(WIDTH // 2 - 50, 620, 100, 40, "Back")]
        elif self.state == "skills_list":
            self.buttons = [Button(WIDTH // 2 - 50, 620, 100, 40, "Back")]
        elif self.state == "battle":
            bw2 = 160
            self.buttons = [
                Button(30, 580, bw2, 40, "Attack", RED),
                Button(200, 580, bw2, 40, "Skill", MAGENTA),
                Button(370, 580, bw2, 40, "Item", YELLOW),
                Button(540, 580, bw2, 40, "Defend", CYAN),
                Button(710, 580, bw2, 40, "Run", GREEN),
            ]
        elif self.state == "skill_select":
            bw2 = 240
            self.buttons = []
            for i, sk in enumerate(self.player.skills[:6]):
                self.buttons.append(Button(30, 380 + i * 50, bw2, 42, f"{sk.name} ({sk.mp_cost}MP)"))
            self.buttons.append(Button(30, 380 + len(self.player.skills[:6]) * 50 + 10, 100, 40, "Back"))
        elif self.state == "item_use":
            cons = [i for i in self.player.inventory if i.itype == "consumable"]
            bw2 = 240
            self.buttons = []
            for i, item in enumerate(cons[:6]):
                self.buttons.append(Button(30, 380 + i * 50, bw2, 42, item.name))
            self.buttons.append(Button(30, 380 + len(cons[:6]) * 50 + 10, 100, 40, "Back"))
        elif self.state == "equip":
            equips = [i for i in self.player.inventory if i.itype in ("weapon", "armor", "accessory")]
            bw2 = 240
            self.buttons = []
            for i, item in enumerate(equips[:6]):
                tag = "[OK]" if item.can_equip(self.player) else "[!]"
                self.buttons.append(Button(30, 380 + i * 50, bw2, 42, f"{item.name} {tag}"))
            self.buttons.append(Button(30, 380 + len(equips[:6]) * 50 + 10, 100, 40, "Back"))
        elif self.state == "move":
            loc = MAP[self.location]
            self.buttons = []
            for i, (d, dest) in enumerate(loc["exits"].items()):
                self.buttons.append(Button(30, 380 + i * 55, 200, 45, f"{d} -> {MAP[dest]['name']}"))
            self.buttons.append(Button(30, 380 + len(loc["exits"]) * 55 + 10, 100, 40, "Back"))
        elif self.state == "npc":
            loc = MAP[self.location]
            self.buttons = []
            for i, npc in enumerate(loc["npcs"]):
                self.buttons.append(Button(30, 380 + i * 55, 200, 45, npc))
            self.buttons.append(Button(30, 380 + len(loc["npcs"]) * 55 + 10, 100, 40, "Back"))
        elif self.state == "npc_shop":
            self.buttons = []
            items = ITEMS.values()
            shop = [i for i in items if i.itype in ("weapon", "armor", "accessory", "consumable") and i.value <= 200]
            for i, item in enumerate(shop[:6]):
                self.buttons.append(Button(30, 380 + i * 50, 240, 42, f"{item.name} ({item.value}g)"))
            self.buttons.append(Button(30, 380 + len(shop[:6]) * 50 + 10, 100, 40, "Back"))
        elif self.state == "level_up":
            self.buttons = [
                Button(30, 580, 160, 40, "+STR", RED),
                Button(200, 580, 160, 40, "+DEX", GREEN),
                Button(370, 580, 160, 40, "+INT", BLUE),
                Button(540, 580, 160, 40, "+CON", CYAN),
                Button(710, 580, 160, 40, "+LCK", YELLOW),
            ]
            self.level_points = 5
        elif self.state == "elder_quest":
            self.buttons = []
            for i, q in enumerate(QUESTS):
                if q.req_level <= self.player.level:
                    status = self.quest_status.get(i, "none")
                    label = f"{q.name} [{status}]"
                    self.buttons.append(Button(30, 380 + i * 35, 400, 30, label))
            self.buttons.append(Button(30, 380 + len(QUESTS) * 35 + 10, 100, 40, "Back"))

    def set_msg(self, txt):
        self.message = txt
        self.msg_timer = 180

    def check_quest_complete(self, quest, idx):
        if quest.req_type == "kill":
            return self.kill_counts.get(quest.req_target, 0) >= quest.req_amount
        elif quest.req_type == "collect":
            count = sum(1 for i in self.player.inventory if i.name.lower().replace(" ", "_") == quest.req_target)
            return count >= quest.req_amount
        elif quest.req_type == "visit":
            return self.location == quest.req_target
        elif quest.req_type == "level":
            return self.player.level >= quest.req_target
        elif quest.req_type == "gold":
            return self.player.gold >= quest.req_target
        return False

    def check_quest_kill(self, enemy_type):
        for i in self.active_quests:
            q = QUESTS[i]
            if q.req_type == "kill" and q.req_target == enemy_type:
                self.kill_counts[enemy_type] = self.kill_counts.get(enemy_type, 0) + 1
                if self.check_quest_complete(q, i):
                    self.quest_status[i] = "completed"
                    self.player.gold += q.gold_reward
                    self.player.exp += q.xp_reward
                    self.set_msg(f"Quest complete: {q.name}! +{q.gold_reward}g +{q.xp_reward}xp")
                    self.check_level_up()
        self.battle_count += 1

    def draw_bar(self, x, y, w, h, cur, maxv, color):
        pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h), border_radius=4)
        if maxv > 0:
            fw = max(0, int(w * cur / maxv))
            pygame.draw.rect(screen, color, (x, y, fw, h), border_radius=4)
        pygame.draw.rect(screen, GRAY, (x, y, w, h), 1, border_radius=4)

    def draw_text(self, txt, x, y, f=None, color=TEXT_COLOR):
        f = f or font
        surf = f.render(txt, True, color)
        screen.blit(surf, (x, y))
        return surf.get_width()

    def draw_center(self, txt, y, f=None, color=TEXT_COLOR):
        f = f or font
        surf = f.render(txt, True, color)
        screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

    def draw_wrapped(self, txt, x, y, max_w, f=None, color=TEXT_COLOR):
        f = f or font_sm
        words = txt.split()
        line = ""
        ty = y
        for w in words:
            test = line + w + " "
            if f.size(test)[0] > max_w:
                self.draw_text(line.strip(), x, ty, f, color)
                ty += 20
                line = w + " "
            else:
                line = test
        if line.strip():
            self.draw_text(line.strip(), x, ty, f, color)
        return ty + 20

    def draw_menu(self):
        self.draw_center("RPG ADVENTURE", 150, font_xl, YELLOW)
        self.draw_center("A graphical RPG", 230, font_lg, CYAN)

    def draw_class_select(self):
        self.draw_center("Choose Your Class", 150, font_lg, YELLOW)
        self.draw_center("Warrior - High STR & CON", 360, font, RED)
        self.draw_center("Rogue - High DEX & LCK", 420, font, GREEN)
        self.draw_center("Mage - High INT", 480, font, BLUE)

    def draw_naming(self):
        self.draw_center("Enter Your Name", 200, font_lg, YELLOW)
        pygame.draw.rect(screen, DARK_GRAY, (WIDTH//2 - 150, 280, 300, 40), border_radius=6)
        pygame.draw.rect(screen, CYAN, (WIDTH//2 - 150, 280, 300, 40), 2, border_radius=6)
        display = self.name_input + "_" if self.naming else self.name_input
        self.draw_center(display, 287, font, TEXT_COLOR)

    def draw_main(self):
        loc = MAP[self.location]
        pygame.draw.rect(screen, (40, 40, 70), (20, 20, WIDTH - 40, 520), border_radius=10)
        pygame.draw.rect(screen, CYAN, (20, 20, WIDTH - 40, 520), 2, border_radius=10)

        self.draw_text(loc["name"], 40, 35, font_lg, CYAN)
        self.draw_text(loc["desc"], 40, 75, font_sm, GRAY)

        self.draw_text(f"LV {self.player.level}", 40, 115, font, YELLOW)
        self.draw_text(f"HP", 40, 145, font_sm, GREEN)
        self.draw_bar(80, 145, 200, 18, self.player.hp, self.player.max_hp, GREEN)
        self.draw_text(f"{self.player.hp}/{self.player.max_hp}", 290, 145, font_sm, GREEN)

        self.draw_text(f"MP", 40, 170, font_sm, BLUE)
        self.draw_bar(80, 170, 200, 18, self.player.mp, self.player.max_mp, BLUE)
        self.draw_text(f"{self.player.mp}/{self.player.max_mp}", 290, 170, font_sm, BLUE)

        self.draw_text(f"EXP: {self.player.exp}/{self.player.exp_to_level}", 40, 195, font_sm, YELLOW)
        self.draw_text(f"Gold: {self.player.gold}", 40, 218, font_sm, YELLOW)

        self.draw_text(f"STR:{self.player.get_stat('str')}  DEX:{self.player.get_stat('dex')}  INT:{self.player.get_stat('int')}  CON:{self.player.get_stat('con')}  LCK:{self.player.get_stat('luck')}", 40, 248, font_sm, TEXT_COLOR)

        if self.player.equipment["weapon"]:
            self.draw_text(f"Wpn: {self.player.equipment['weapon'].name}", 40, 278, font_sm, CYAN)
        if self.player.equipment["armor"]:
            self.draw_text(f"Arm: {self.player.equipment['armor'].name}", 300, 278, font_sm, CYAN)

        if loc["npcs"]:
            self.draw_text(f"NPCs: {', '.join(loc['npcs'])}", 40, 310, font_sm, MAGENTA)

        exits_str = " | ".join(f"{d}->{MAP[e]['name']}" for d, e in loc["exits"].items())
        self.draw_wrapped(f"Exits: {exits_str}", 40, 340, WIDTH - 80, font_sm, GRAY)

        self.draw_minimap()

    def draw_minimap(self):
        map_x, map_y = 580, 30
        map_w, map_h = 290, 230
        scale = 55
        node_r = 8

        bg = pygame.Surface((map_w, map_h), pygame.SRCALPHA)
        bg.fill((20, 20, 40, 180))
        screen.blit(bg, (map_x, map_y))
        pygame.draw.rect(screen, DARK_GRAY, (map_x, map_y, map_w, map_h), 2, border_radius=8)

        self.draw_text("MAP", map_x + 10, map_y + 5, font_sm, CYAN)

        for loc1, loc2 in MAP_CONNECTIONS:
            p1 = MAP_POSITIONS.get(loc1)
            p2 = MAP_POSITIONS.get(loc2)
            if p1 and p2 and loc1 in self.visited and loc2 in self.visited:
                sx = map_x + 30 + p1[0] * scale
                sy = map_y + 35 + p1[1] * scale
                ex = map_x + 30 + p2[0] * scale
                ey = map_y + 35 + p2[1] * scale
                pygame.draw.line(screen, GRAY, (sx, sy), (ex, ey), 2)

        for loc_key, (gx, gy) in MAP_POSITIONS.items():
            if loc_key not in self.visited:
                continue
            cx = map_x + 30 + gx * scale
            cy = map_y + 35 + gy * scale
            r = node_r + 4 if loc_key == self.location else node_r
            color = YELLOW if loc_key == self.location else CYAN
            pygame.draw.circle(screen, color, (cx, cy), r)
            pygame.draw.circle(screen, TEXT_COLOR, (cx, cy), r, 1)
            name = MAP[loc_key]["name"][:6]
            self.draw_text(name, cx - 18, cy + r + 2, font_sm, GRAY)

    def draw_battle(self):
        e = self.enemy
        pygame.draw.rect(screen, (60, 20, 20), (20, 20, WIDTH - 40, 540), border_radius=10)
        pygame.draw.rect(screen, RED, (20, 20, WIDTH - 40, 540), 2, border_radius=10)

        self.draw_center(f"BATTLE", 35, font_lg, RED)
        self.draw_center(f"{e.name} Lv.{e.level}", 80, font, TEXT_COLOR)
        self.draw_text("HP", 300, 120, font_sm, RED)
        self.draw_bar(340, 120, 250, 20, e.hp, e.max_hp, RED)
        self.draw_text(f"{e.hp}/{e.max_hp}", 600, 120, font_sm, RED)

        self.draw_text(self.player.name, 40, 180, font_lg, GREEN)
        self.draw_text("HP", 40, 230, font_sm, GREEN)
        self.draw_bar(80, 230, 200, 18, self.player.hp, self.player.max_hp, GREEN)
        self.draw_text(f"{self.player.hp}/{self.player.max_hp}", 290, 230, font_sm, GREEN)

        self.draw_text("MP", 40, 258, font_sm, BLUE)
        self.draw_bar(80, 258, 200, 18, self.player.mp, self.player.max_mp, BLUE)
        self.draw_text(f"{self.player.mp}/{self.player.max_mp}", 290, 258, font_sm, BLUE)

    def draw_inventory(self):
        pygame.draw.rect(screen, (40, 40, 70), (20, 20, WIDTH - 40, HEIGHT - 40), border_radius=10)
        self.draw_text("INVENTORY", 40, 35, font_lg, CYAN)
        self.draw_text(f"Gold: {self.player.gold}", 40, 75, font, YELLOW)
        y = 110 + self.scroll_offset
        max_y = HEIGHT - 60
        for item in self.player.inventory:
            if y > 100 and y < max_y:
                stats = []
                if item.attack: stats.append(f"ATK+{item.attack}")
                if item.defense: stats.append(f"DEF+{item.defense}")
                s = f" [{','.join(stats)}]" if stats else ""
                self.draw_text(f"{item.name}{s}", 40, y, font_sm, TEXT_COLOR)
                self.draw_text(item.desc, 250, y, font_sm, GRAY)
            y += 28
        if len(self.player.inventory) > 0:
            count_text = f"{len(self.player.inventory)} items"
            self.draw_text(count_text, WIDTH - 200, HEIGHT - 50, font_sm, GRAY)

    def draw_skills_list(self):
        pygame.draw.rect(screen, (40, 40, 70), (20, 20, WIDTH - 40, HEIGHT - 40), border_radius=10)
        self.draw_text("SKILLS", 40, 35, font_lg, MAGENTA)
        y = 80 + self.scroll_offset
        max_y = HEIGHT - 60
        for sk in ALL_SKILLS:
            if y > 70 and y < max_y:
                learned = sk in self.player.skills
                c = GREEN if learned else (YELLOW if all(self.player.get_stat(s) >= v for s, v in sk.stat_req.items()) else RED)
                self.draw_text(f"{sk.name}", 40, y, font, c)
                self.draw_text(f"{sk.desc} | MP:{sk.mp_cost} | {sk.stype}", 200, y, font_sm, GRAY)
                self.draw_text("LEARNED" if learned else ("READY" if c == YELLOW else "LOCKED"), 600, y, font_sm, c)
            y += 32

    def draw_level_up(self):
        self.draw_center("LEVEL UP!", 200, font_xl, YELLOW)
        self.draw_center(f"Level {self.player.level}", 270, font_lg, GREEN)
        pts = getattr(self, 'level_points', 5)
        self.draw_center(f"Points: {pts}", 320, font, TEXT_COLOR)

    def draw_message(self):
        if self.msg_timer > 0:
            self.msg_timer -= 1
            alpha = min(255, self.msg_timer * 3)
            surf = font.render(self.message, True, YELLOW)
            bg = pygame.Surface((surf.get_width() + 20, 36))
            bg.fill((40, 40, 70))
            bg.set_alpha(min(200, alpha))
            screen.blit(bg, (WIDTH//2 - bg.get_width()//2, HEIGHT - 90))
            surf.set_alpha(alpha)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT - 85))

    def start(self):
        while True:
            pos = pygame.mouse.get_pos()
            screen.fill(BG_COLOR)

            for b in self.buttons:
                b.check_hover(pos)
                b.draw(screen)

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "class_select":
                self.draw_class_select()
            elif self.state == "naming":
                self.draw_naming()
            elif self.state == "main":
                self.draw_main()
            elif self.state == "battle":
                self.draw_battle()
            elif self.state in ("inventory", "skills_list"):
                if self.state == "inventory":
                    self.draw_inventory()
                else:
                    self.draw_skills_list()
            elif self.state == "level_up":
                self.draw_level_up()

            self.draw_message()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(pos)
                if event.type == pygame.KEYDOWN and self.state == "naming":
                    if event.key == pygame.K_RETURN and self.name_input:
                        self.state = "class_select"
                        self.create_buttons()
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    elif event.unicode.isprintable() and len(self.name_input) < 16:
                        self.name_input += event.unicode
                if event.type == pygame.MOUSEWHEEL and self.state in ("inventory", "skills_list"):
                    self.scroll_offset += event.y * 30
                    self.scroll_offset = min(0, self.scroll_offset)
                    if self.state == "inventory":
                        max_scroll = -(len(self.player.inventory) * 28 - 480)
                        self.scroll_offset = max(max_scroll, self.scroll_offset)
                    elif self.state == "skills_list":
                        max_scroll = -(len(ALL_SKILLS) * 32 - 480)
                        self.scroll_offset = max(max_scroll, self.scroll_offset)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def handle_click(self, pos):
        for b in self.buttons:
            if not b.clicked(pos):
                continue
            self.process_button(b)
            return

        if self.state == "main" and self.msg_timer <= 0:
            loc = MAP[self.location]
            if loc["enemies"] and random.random() < 0.3:
                etype = random.choice(loc["enemies"])
                t = ENEMIES[etype]
                lv = max(1, t[1] + random.randint(-1, 1))
                self.enemy = Enemy(t[0], lv, int(t[2] * (1 + (lv - t[1]) * 0.2)),
                                   int(t[3] * (1 + (lv - t[1]) * 0.15)), t[4], t[5], t[6])
                self.state = "battle"
                self.create_buttons()
                self.set_msg(f"{self.enemy.name} appeared!")

    def process_button(self, b):
        txt = b.text

        if self.state == "menu":
            if txt == "Start Game":
                self.state = "naming"
                self.naming = True
                self.name_input = ""
                self.create_buttons()
            elif txt == "Quit":
                pygame.quit()
                sys.exit()

        elif self.state == "class_select":
            classes = {"Warrior": ("Warrior", {"str": 7, "con": 6}),
                       "Rogue": ("Rogue", {"dex": 7, "luck": 6}),
                       "Mage": ("Mage", {"int": 7, "dex": 5})}
            cn, stats = classes.get(txt, ("Warrior", {"str": 7, "con": 6}))
            self.player = Character(self.name_input or "Hero", cn)
            for s, v in stats.items():
                self.player.stats[s] = v
            self.player.inventory.extend([ITEMS["hp_pot"], ITEMS["hp_pot"]])
            self.player.check_new_skills()
            self.state = "main"
            self.create_buttons()

        elif self.state == "naming":
            if txt == "Confirm" and self.name_input:
                self.state = "class_select"
                self.create_buttons()

        elif self.state == "main":
            if txt == "Status":
                self.state = "skills_list"
                self.scroll_offset = 0
                self.create_buttons()
            elif txt == "Inventory":
                self.state = "inventory"
                self.scroll_offset = 0
                self.create_buttons()
            elif txt == "Explore":
                self.do_explore()
            elif txt == "Move":
                self.state = "move"
                self.create_buttons()
            elif txt == "Talk":
                self.state = "npc"
                self.create_buttons()
            elif txt == "Skills":
                self.state = "skills_list"
                self.create_buttons()
            elif txt == "Use Item":
                self.state = "item_use"
                self.create_buttons()
            elif txt == "Equip":
                self.state = "equip"
                self.create_buttons()
            elif txt == "Rest":
                if self.player.gold >= 10:
                    self.player.gold -= 10
                    self.player.hp = self.player.max_hp
                    self.player.mp = self.player.max_mp
                    self.set_msg("Rested! HP and MP restored.")
                else:
                    self.set_msg("Not enough gold!")
            elif txt == "Quit":
                pygame.quit()
                sys.exit()

        elif self.state in ("inventory", "skills_list"):
            if txt == "Back":
                self.state = "main"
                self.scroll_offset = 0
                self.create_buttons()

        elif self.state == "battle":
            if txt == "Attack":
                self.do_attack()
            elif txt == "Skill":
                self.state = "skill_select"
                self.create_buttons()
            elif txt == "Item":
                self.state = "item_use"
                self.create_buttons()
            elif txt == "Defend":
                dmg = self.enemy.attack // 2
                self.player.take_damage(dmg)
                self.set_msg(f"Defending! Took {dmg} damage reduced.")
                if not self.player.is_alive():
                    self.state = "menu"
                    self.create_buttons()
                self.do_enemy_turn()
            elif txt == "Run":
                if random.random() < 0.5 + self.player.get_stat("dex") / 100:
                    self.set_msg("Escaped!")
                    self.enemy = None
                    self.state = "main"
                    self.create_buttons()
                else:
                    self.set_msg("Failed to run!")
                    self.do_enemy_turn()

        elif self.state == "skill_select":
            if txt == "Back":
                self.state = "battle"
                self.create_buttons()
            else:
                for sk in self.player.skills[:6]:
                    if sk.name in txt:
                        if self.player.mp >= sk.mp_cost:
                            self.player.mp -= sk.mp_cost
                            if sk.stype == "physical":
                                dmg = int(self.player.get_attack() * sk.power + random.randint(-3, 8))
                                actual = self.enemy.take_damage(dmg)
                                self.set_msg(f"{sk.name}! Dealt {actual} damage!")
                            elif sk.stype == "magic":
                                dmg = int(self.player.get_magic_attack() * sk.power + random.randint(-5, 10))
                                actual = self.enemy.take_damage(dmg)
                                self.set_msg(f"{sk.name}! Dealt {actual} magic damage!")
                            elif sk.stype == "heal":
                                heal = int(sk.power + self.player.get_stat("int") * 2)
                                self.player.heal(heal)
                                self.set_msg(f"{sk.name}! Healed {heal} HP!")
                            if not self.enemy.is_alive():
                                self.do_victory()
                            else:
                                self.do_enemy_turn()
                            if self.state == "skill_select":
                                self.state = "battle"
                                self.create_buttons()
                        else:
                            self.set_msg("Not enough MP!")

        elif self.state == "item_use":
            if txt == "Back":
                self.state = "battle" if self.enemy else "main"
                self.create_buttons()
            else:
                cons = [i for i in self.player.inventory if i.itype == "consumable"]
                for i, item in enumerate(cons[:6]):
                    if item.name in txt:
                        if item.heal_amount > 0:
                            self.player.heal(item.heal_amount)
                            self.set_msg(f"Used {item.name}. Healed {item.heal_amount} HP!")
                        if item.mp_amount > 0:
                            self.player.mp = min(self.player.max_mp, self.player.mp + item.mp_amount)
                            self.set_msg(f"Used {item.name}. Restored {item.mp_amount} MP!")
                        self.player.inventory.remove(item)
                        if self.state == "item_use":
                            self.create_buttons()

        elif self.state == "equip":
            if txt == "Back":
                self.state = "main"
                self.create_buttons()
            else:
                equips = [i for i in self.player.inventory if i.itype in ("weapon", "armor", "accessory")]
                for i, item in enumerate(equips[:6]):
                    if item.name in txt:
                        if item.can_equip(self.player):
                            old = self.player.equipment[item.itype]
                            if old:
                                self.player.equipped_items.remove(old)
                                self.player.inventory.append(old)
                            self.player.equipment[item.itype] = item
                            self.player.equipped_items.append(item)
                            self.player.inventory.remove(item)
                            self.set_msg(f"Equipped {item.name}!")
                        else:
                            self.set_msg("Cannot equip!")
                        self.create_buttons()

        elif self.state == "move":
            if txt == "Back":
                self.state = "main"
                self.create_buttons()
            else:
                loc = MAP[self.location]
                for d, dest in loc["exits"].items():
                    if d in txt:
                        self.location = dest
                        self.visited.add(dest)
                        self.set_msg(f"Traveled to {MAP[dest]['name']}")
                        self.state = "main"
                        self.create_buttons()

        elif self.state == "npc":
            if txt == "Back":
                self.state = "main"
                self.create_buttons()
            else:
                self.set_msg(f"Talked to {txt}")
                if txt == "Merchant":
                    self.state = "npc_shop"
                    self.create_buttons()
                elif txt == "Elder":
                    self.state = "elder_quest"
                    self.create_buttons()

        elif self.state == "npc_shop":
            if txt == "Back":
                self.state = "main"
                self.create_buttons()
            else:
                all_shop = list(ITEMS.values())
                for item in all_shop:
                    if item.name in txt:
                        if self.player.gold >= item.value:
                            self.player.gold -= item.value
                            self.player.inventory.append(item)
                            self.set_msg(f"Bought {item.name}!")
                        else:
                            self.set_msg("Not enough gold!")
                        self.create_buttons()

        elif self.state == "elder_quest":
            if txt == "Back":
                self.state = "main"
                self.create_buttons()
            else:
                for i, q in enumerate(QUESTS):
                    if q.name in txt:
                        if i not in self.quest_status:
                            self.quest_status[i] = "active"
                            self.active_quests.append(i)
                            self.set_msg(f"Accepted quest: {q.name}")
                        elif self.quest_status[i] == "active":
                            if self.check_quest_complete(q, i):
                                self.quest_status[i] = "completed"
                                self.player.gold += q.gold_reward
                                self.player.exp += q.xp_reward
                                self.set_msg(f"Quest complete! +{q.gold_reward}g +{q.xp_reward}xp")
                                self.check_level_up()
                            else:
                                self.set_msg("Quest not yet complete!")
                        else:
                            self.set_msg("Quest already completed!")
                        self.create_buttons()
                        break

        elif self.state == "level_up":
            pts = getattr(self, 'level_points', 5)
            stat_map = {"+STR": "str", "+DEX": "dex", "+INT": "int", "+CON": "con", "+LCK": "luck"}
            if txt in stat_map and pts > 0:
                self.player.stats[stat_map[txt]] += 1
                self.level_points = pts - 1
                self.set_msg(f"{stat_map[txt].upper()} +1!")
                if self.level_points <= 0:
                    self.state = "main"
                self.create_buttons()

    def do_explore(self):
        roll = random.random()
        loc = MAP[self.location]
        if roll < 0.6 and loc["enemies"]:
            etype = random.choice(loc["enemies"])
            t = ENEMIES[etype]
            lv = max(1, t[1] + random.randint(-1, 1))
            self.enemy = Enemy(t[0], lv, int(t[2] * (1 + (lv - t[1]) * 0.2)),
                               int(t[3] * (1 + (lv - t[1]) * 0.15)), t[4], t[5], t[6])
            self.enemy_type = etype
            self.state = "battle"
            self.create_buttons()
            self.set_msg(f"{self.enemy.name} appeared!")
        elif roll < 0.8 and self.location in HERB_LOCATIONS:
            self.player.inventory.append(ITEMS["herb"])
            self.set_msg("Found a Healing Herb!")
        else:
            self.set_msg("Nothing interesting found.")

    def do_attack(self):
        if random.random() < self.player.get_stat("dex") / 150:
            self.set_msg("You missed!")
        else:
            dmg = self.player.get_attack() + random.randint(-2, 5)
            crit = random.random() < self.player.get_stat("luck") / 100
            if crit:
                dmg = int(dmg * 1.8)
                self.set_msg(f"CRITICAL HIT! Dealt {self.enemy.take_damage(dmg)} damage!")
            else:
                self.set_msg(f"Dealt {self.enemy.take_damage(dmg)} damage!")

        if not self.enemy.is_alive():
            self.do_victory()
        else:
            self.do_enemy_turn()

    def do_enemy_turn(self):
        dmg = self.enemy.attack + random.randint(-2, 3)
        actual = self.player.take_damage(dmg)
        self.set_msg(f"{self.enemy.name} attacks for {actual} damage!")
        if not self.player.is_alive():
            self.set_msg("GAME OVER!")
            self.enemy = None
            self.state = "menu"
            self.create_buttons()

    def do_victory(self):
        self.set_msg(f"Victory! +{self.enemy.exp_reward} EXP +{self.enemy.gold_reward} Gold")
        self.player.exp += self.enemy.exp_reward
        self.player.gold += self.enemy.gold_reward
        self.check_quest_kill(self.enemy_type)
        self.enemy = None
        self.state = "main"
        self.create_buttons()
        while self.player.exp >= self.player.exp_to_level:
            self.player.level_up()
            self.state = "level_up"
            self.level_points = 5
            self.create_buttons()


if __name__ == "__main__":
    game = Game()
    game.start()

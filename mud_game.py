from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List


HELP_TEXT = """명령어 안내\n- look: 지도와 현재 위치 확인\n- go east / go west: 이동\n- map: 현재 맵 보기\n- inventory: 인벤토리 확인\n- status: 상태 확인\n- train: 스탯 투자\n- skill: 스킬 목록 확인\n- equip: 장비 장착\n- explore: 현재 지역 탐험\n- combat: 전투 시작\n- shop: 상점 이용\n- quest: NPC 퀘스트 확인\n- save/load: 저장 및 불러오기\n- help: 도움말 보기\n- quit: 종료"""


@dataclass
class Player:
    name: str
    job: str = ""
    level: int = 1
    exp: int = 0
    stat_points: int = 0
    stats: Dict[str, int] = field(default_factory=lambda: {"str": 1, "agi": 1, "int": 1, "hp": 10})
    skills: List[str] = field(default_factory=list)
    equipment: Dict[str, str] = field(default_factory=lambda: {"weapon": "", "armor": ""})
    inventory: List[str] = field(default_factory=list)
    location: str = "village"


JOB_REQUIREMENTS = {
    "warrior": {"slash": 5, "shield_bash": 10},
    "archer": {"quick_shot": 5, "piercing_arrow": 10},
    "mage": {"fireball": 5, "meteor": 10},
}

JOB_STATS = {
    "warrior": "str",
    "archer": "agi",
    "mage": "int",
}

ITEM_REQUIREMENTS = {
    "iron_sword": {"warrior": {"str": 5}},
    "leather_armor": {"warrior": {"str": 3}},
    "longbow": {"archer": {"agi": 5}},
    "mage_robe": {"mage": {"int": 5}},
}

AREA_INFO = {
    "village": "마을입니다. 상점과 직업 교관이 있습니다.",
    "beginner_hunt": "초보자 사냥터입니다. 슬라임과 고블린이 출몰합니다.",
    "mid_dungeon": "중급자 던전입니다. 강한 몬스터가 숨어 있습니다.",
}

AREA_REWARDS = {
    "beginner_hunt": 40,
    "mid_dungeon": 80,
}

SHOP_ITEMS = {
    "healing_potion": 20,
    "iron_sword": 60,
}

QUESTS = {
    "village": "마을의 길드장에게 인사를 하고 퀘스트를 받으세요.",
    "beginner_hunt": "초보자 사냥터에서 슬라임 3마리를 처치하세요.",
    "mid_dungeon": "던전에서 불길한 기운을 조사하세요.",
}


def gain_experience(player: Player, amount: int) -> None:
    player.exp += amount
    while player.exp >= 100:
        player.exp -= 100
        player.level += 1
        player.stat_points += 5


def can_use_skill(player: Player, skill_name: str) -> bool:
    required = JOB_REQUIREMENTS[player.job].get(skill_name, 0)
    stat_key = JOB_STATS[player.job]
    return player.stats[stat_key] >= required


def equip_item(player: Player, item_name: str) -> bool:
    requirements = ITEM_REQUIREMENTS.get(item_name, {})
    job_requirements = requirements.get(player.job, {})
    if not job_requirements:
        return False

    for stat_name, required_value in job_requirements.items():
        if player.stats[stat_name] < required_value:
            return False

    slot = "weapon" if item_name in {"iron_sword", "longbow"} else "armor"
    player.equipment[slot] = item_name
    return True


def describe_world() -> str:
    return (
        "[세계 지도]\n"
        "- 중앙: 마을\n"
        "- 동쪽: 초보자 사냥터\n"
        "- 서쪽: 중급자 던전"
    )


def get_map() -> str:
    return "[맵]\n마을(중앙) - 초보자 사냥터(동쪽) - 중급자 던전(서쪽)"


def add_item(player: Player, item_name: str) -> None:
    player.inventory.append(item_name)


def show_inventory(player: Player) -> str:
    if not player.inventory:
        return "인벤토리: 비어 있습니다."
    return "인벤토리: " + ", ".join(player.inventory)


def choose_job(player: Player, job_name: str) -> str:
    valid_jobs = {"warrior", "archer", "mage"}
    if job_name not in valid_jobs:
        return "직업을 다시 선택해 주세요."

    player.job = job_name
    return f"{job_name}으로 전직했습니다."


def move_player(player: Player, direction: str) -> bool:
    moves = {
        "village": {"east": "beginner_hunt", "west": "mid_dungeon"},
        "beginner_hunt": {"west": "village"},
        "mid_dungeon": {"east": "village"},
    }
    destination = moves.get(player.location, {}).get(direction)
    if destination is None:
        return False

    player.location = destination
    return True


def explore_area(player: Player) -> str:
    if player.location not in AREA_INFO:
        return "알 수 없는 지역입니다."

    reward = AREA_REWARDS.get(player.location, 0)
    gain_experience(player, reward)
    if player.location == "beginner_hunt":
        add_item(player, "healing_potion")
    return f"{AREA_INFO[player.location]}\n{reward} 경험치를 얻었습니다."


def start_combat(player: Player) -> str:
    damage = max(3, player.level + player.stats[JOB_STATS[player.job]] if player.job else 3)
    gain_experience(player, 20)
    return f"전투 시작! 몬스터에게 {damage}의 피해를 주었습니다."


def buy_item(player: Player, item_name: str) -> bool:
    if item_name not in SHOP_ITEMS:
        return False
    price = SHOP_ITEMS[item_name]
    if player.level < 2 and item_name == "iron_sword":
        return False
    add_item(player, item_name)
    return True


def save_game(player: Player, path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(player.__dict__, handle, ensure_ascii=False, indent=2)


def load_game(path: str) -> Player:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    player = Player(name=data["name"])
    player.__dict__.update(data)
    return player


def get_quest(player: Player) -> str:
    return QUESTS.get(player.location, "현재 지역에는 퀘스트가 없습니다.")

from mud_game import (
    Player,
    choose_job,
    describe_world,
    equip_item,
    explore_area,
    move_player,
    get_map,
    show_inventory,
    HELP_TEXT,
    start_combat,
    buy_item,
    save_game,
    load_game,
    get_quest,
)


def main() -> None:
    print("=== 텍스트 MUD 게임 ===")
    name = input("플레이어 이름을 입력하세요: ").strip() or "Player"
    player = Player(name=name)

    print("\n마을에 도착했습니다. 직업을 선택해 주세요.")
    print("가능한 직업: warrior, archer, mage")
    while not player.job:
        job = input("직업: ").strip().lower()
        result = choose_job(player, job)
        print(result)

    print("\n" + describe_world())
    print("\n명령어: look, go east/west, map, inventory, status, train, skill, equip, explore, combat, shop, quest, save/load, help, quit")

    while True:
        command = input("\n명령을 입력하세요: ").strip().lower()

        if command in {"quit", "exit"}:
            print("게임을 종료합니다.")
            break
        elif command == "look":
            print(describe_world())
            print(f"현재 위치: {player.location}")
        elif command == "map":
            print(get_map())
        elif command == "inventory":
            print(show_inventory(player))
        elif command.startswith("go "):
            direction = command.split()[1]
            if move_player(player, direction):
                print(f"{direction}쪽으로 이동했습니다.")
            else:
                print("그 방향으로는 이동할 수 없습니다.")
        elif command == "status":
            print(f"이름: {player.name}")
            print(f"직업: {player.job}")
            print(f"레벨: {player.level}")
            print(f"경험치: {player.exp}/100")
            print(f"스탯 포인트: {player.stat_points}")
            print(f"스탯: {player.stats}")
            print(f"스킬: {player.skills}")
            print(f"장비: {player.equipment}")
            print(f"현재 위치: {player.location}")
        elif command == "train":
            if player.stat_points <= 0:
                print("사용 가능한 스탯 포인트가 없습니다.")
                continue
            print("어디에 스탯을 투자할까요? str/agi/int")
            stat = input("스탯: ").strip().lower()
            if stat not in player.stats:
                print("잘못된 스탯입니다.")
                continue
            player.stats[stat] += 1
            player.stat_points -= 1
            print(f"{stat} 스탯이 1 증가했습니다.")
        elif command == "skill":
            if player.job == "warrior":
                print("배울 수 있는 스킬: slash, shield_bash")
            elif player.job == "archer":
                print("배울 수 있는 스킬: quick_shot, piercing_arrow")
            else:
                print("배울 수 있는 스킬: fireball, meteor")
        elif command == "equip":
            item = input("장착할 아이템 이름: ").strip().lower()
            if equip_item(player, item):
                print(f"{item}을(를) 장착했습니다.")
            else:
                print("조건이 부족해 장착할 수 없습니다.")
        elif command == "explore":
            print(explore_area(player))
        elif command == "combat":
            print(start_combat(player))
        elif command == "shop":
            print("상점에 오셨습니다. 구매 가능: healing_potion, iron_sword")
            item = input("구매할 아이템: ").strip().lower()
            if buy_item(player, item):
                print(f"{item}을(를) 구매했습니다.")
            else:
                print("구매할 수 없는 아이템입니다.")
        elif command == "quest":
            print(get_quest(player))
        elif command == "save":
            save_game(player, "save.json")
            print("저장되었습니다.")
        elif command == "load":
            loaded = load_game("save.json")
            player = loaded
            print("불러오기가 완료되었습니다.")
        elif command == "help":
            print(HELP_TEXT)
        else:
            print("알 수 없는 명령입니다.")


if __name__ == "__main__":
    main()

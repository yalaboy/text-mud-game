export const SKILLS = [
  // === PHYSICAL (15) ===
  { name: 'Power Strike', desc: 'Heavy physical blow', mpCost: 8, type: 'physical', power: 2.0, statReq: { str: 8 } },
  { name: 'Cleave', desc: 'Sweeping arc attack', mpCost: 15, type: 'physical', power: 3.0, statReq: { str: 14 } },
  { name: 'Backstab', desc: 'Precision strike from behind', mpCost: 10, type: 'physical', power: 2.5, statReq: { dex: 10 } },
  { name: 'Whirlwind', desc: 'Spinning blade attack', mpCost: 18, type: 'physical', power: 2.8, statReq: { str: 12, dex: 8 } },
  { name: 'Shield Bash', desc: 'Slam with your shield', mpCost: 6, type: 'physical', power: 1.5, statReq: { con: 6 } },
  { name: 'Execute', desc: 'Devastating finishing blow', mpCost: 25, type: 'physical', power: 4.0, statReq: { str: 18 } },
  { name: 'Piercing Thrust', desc: 'Ignores some armor', mpCost: 12, type: 'physical', power: 2.2, statReq: { dex: 12 } },
  { name: 'Skull Crusher', desc: 'Stuns on impact', mpCost: 14, type: 'physical', power: 2.6, statReq: { str: 10, con: 6 } },
  { name: 'Dual Strike', desc: 'Two fast slashes', mpCost: 11, type: 'physical', power: 1.8, statReq: { dex: 14 } },
  { name: 'Berserker Rage', desc: 'Frenzied attacks, costs HP', mpCost: 20, type: 'physical', power: 3.5, statReq: { str: 16, con: 10 } },
  { name: 'Sunder Armor', desc: 'Breaks enemy defenses', mpCost: 13, type: 'physical', power: 2.0, statReq: { str: 11 } },
  { name: 'Frenzy', desc: 'Attack speed boost', mpCost: 16, type: 'physical', power: 2.4, statReq: { dex: 11, str: 9 } },
  { name: 'Impale', desc: 'Deep penetrating strike', mpCost: 19, type: 'physical', power: 3.2, statReq: { str: 15, dex: 10 } },
  { name: 'Rage Slash', desc: 'Stronger when hurt', mpCost: 14, type: 'physical', power: 2.7, statReq: { str: 13 } },
  { name: 'Titan Strike', desc: 'Massive earth-shaking blow', mpCost: 28, type: 'physical', power: 4.5, statReq: { str: 20, con: 12 } },

  // === MAGIC (15) ===
  { name: 'Fireball', desc: 'Launch a ball of fire', mpCost: 12, type: 'magic', power: 2.5, statReq: { int: 8 } },
  { name: 'Ice Shard', desc: 'Freezing ice projectile', mpCost: 10, type: 'magic', power: 2.0, statReq: { int: 6 } },
  { name: 'Lightning Bolt', desc: 'Chain of lightning', mpCost: 20, type: 'magic', power: 4.0, statReq: { int: 16 } },
  { name: 'Shadow Bolt', desc: 'Dark energy projectile', mpCost: 14, type: 'magic', power: 2.8, statReq: { int: 10 } },
  { name: 'Arcane Burst', desc: 'Raw magical explosion', mpCost: 22, type: 'magic', power: 3.5, statReq: { int: 14 } },
  { name: 'Frost Nova', desc: 'Freeze everything nearby', mpCost: 18, type: 'magic', power: 3.0, statReq: { int: 12 } },
  { name: 'Chain Lightning', desc: 'Bounces between targets', mpCost: 24, type: 'magic', power: 3.8, statReq: { int: 18 } },
  { name: 'Inferno', desc: 'Raging firestorm', mpCost: 26, type: 'magic', power: 4.2, statReq: { int: 17 } },
  { name: 'Blizzard', desc: 'Piercing ice storm', mpCost: 21, type: 'magic', power: 3.3, statReq: { int: 15 } },
  { name: 'Void Pulse', desc: 'Dark energy wave', mpCost: 16, type: 'magic', power: 2.9, statReq: { int: 11 } },
  { name: ' Meteor', desc: 'Call a meteor from the sky', mpCost: 30, type: 'magic', power: 5.0, statReq: { int: 20 } },
  { name: 'Thunder Clap', desc: 'Shockwave of thunder', mpCost: 17, type: 'magic', power: 3.1, statReq: { int: 13 } },
  { name: 'Acid Rain', desc: 'Corrosive rain damage', mpCost: 15, type: 'magic', power: 2.7, statReq: { int: 9 } },
  { name: 'Rune Blast', desc: 'Detonates inscribed runes', mpCost: 19, type: 'magic', power: 3.4, statReq: { int: 14, dex: 6 } },
  { name: 'Eldritch Beam', desc: 'Focused beam of pure magic', mpCost: 28, type: 'magic', power: 4.8, statReq: { int: 19 } },

  // === HEAL / SUPPORT (10) ===
  { name: 'Heal', desc: 'Restore HP', mpCost: 10, type: 'heal', power: 50, statReq: { int: 5 } },
  { name: 'Greater Heal', desc: 'Strong healing', mpCost: 18, type: 'heal', power: 100, statReq: { int: 12 } },
  { name: 'Rejuvenate', desc: 'Heal over time', mpCost: 14, type: 'heal', power: 70, statReq: { int: 9 } },
  { name: 'Holy Light', desc: 'Divine healing radiance', mpCost: 22, type: 'heal', power: 130, statReq: { int: 16 } },
  { name: 'Blood Drain', desc: 'Steal life from enemy', mpCost: 16, type: 'magic', power: 2.2, statReq: { int: 10, luck: 5 } },
  { name: 'Life Surge', desc: 'Heal based on missing HP', mpCost: 20, type: 'heal', power: 110, statReq: { int: 14, con: 8 } },
  { name: 'Regeneration', desc: 'Long-lasting regeneration', mpCost: 25, type: 'heal', power: 150, statReq: { int: 18 } },
  { name: 'Purify', desc: 'Cleanse and heal minor wounds', mpCost: 8, type: 'heal', power: 35, statReq: { int: 4 } },
  { name: 'Nature\'s Touch', desc: 'Heal from nature\'s power', mpCost: 12, type: 'heal', power: 60, statReq: { int: 7, con: 5 } },
  { name: 'Resurrection Light', desc: 'Massive heal from beyond', mpCost: 35, type: 'heal', power: 200, statReq: { int: 22 } },

  // === BUFF (5) ===
  { name: 'Battle Cry', desc: 'Boost attack power', mpCost: 10, type: 'buff', power: 1.5, statReq: { str: 8, con: 5 } },
  { name: 'Iron Skin', desc: 'Temporarily harden skin', mpCost: 12, type: 'buff', power: 2.0, statReq: { con: 10 } },
  { name: 'Haste', desc: 'Increase dodge chance', mpCost: 14, type: 'buff', power: 1.8, statReq: { dex: 12 } },
  { name: 'Arcane Shield', desc: 'Absorb magic damage', mpCost: 16, type: 'buff', power: 2.5, statReq: { int: 13 } },
  { name: 'War Drums', desc: 'Boost all stats briefly', mpCost: 22, type: 'buff', power: 1.3, statReq: { str: 10, int: 8 } },

  // === DEBUFF (5) ===
  { name: 'Weaken', desc: 'Reduce enemy attack', mpCost: 8, type: 'debuff', power: 0.7, statReq: { int: 6 } },
  { name: 'Slow', desc: 'Reduce enemy speed', mpCost: 10, type: 'debuff', power: 0.6, statReq: { int: 8 } },
  { name: 'Curse', desc: 'Lowers enemy luck', mpCost: 12, type: 'debuff', power: 0.5, statReq: { int: 10 } },
  { name: 'Armor Break', desc: 'Shatter enemy armor', mpCost: 14, type: 'debuff', power: 0.4, statReq: { str: 12, int: 6 } },
  { name: 'Siphon Mana', desc: 'Drain enemy MP (converts to damage)', mpCost: 18, type: 'debuff', power: 0.3, statReq: { int: 15 } },
]

export const ITEMS = {
  // === WEAPONS (18) ===
  iron_sword: { id: 'iron_sword', name: 'Iron Sword', desc: 'Sturdy sword', type: 'weapon', attack: 10, requirements: { str: 5 }, value: 50 },
  steel_sword: { id: 'steel_sword', name: 'Steel Sword', desc: 'Well-crafted blade', type: 'weapon', attack: 20, requirements: { str: 12 }, value: 120 },
  shadow_dag: { id: 'shadow_dag', name: 'Shadow Dagger', desc: 'Swift dark dagger', type: 'weapon', attack: 18, requirements: { dex: 16 }, value: 180 },
  staff_flame: { id: 'staff_flame', name: 'Staff of Flames', desc: 'Channels fire magic', type: 'weapon', attack: 8, statBonus: { int: 8 }, requirements: { int: 12 }, value: 150 },
  warhammer: { id: 'warhammer', name: 'Warhammer', desc: 'Crushing force', type: 'weapon', attack: 25, requirements: { str: 18 }, value: 200 },
  crystal_wand: { id: 'crystal_wand', name: 'Crystal Wand', desc: 'Amplifies magic power', type: 'weapon', attack: 6, statBonus: { int: 12 }, requirements: { int: 15 }, value: 220 },
  assassin_blade: { id: 'assassin_blade', name: 'Assassin Blade', desc: 'Venomous edge', type: 'weapon', attack: 22, statBonus: { dex: 5 }, requirements: { dex: 14 }, value: 250 },
  thunder_axe: { id: 'thunder_axe', name: 'Thunder Axe', desc: 'Crackles with lightning', type: 'weapon', attack: 28, statBonus: { str: 3 }, requirements: { str: 16, con: 8 }, value: 300 },
  flame_tongue: { id: 'flame_tongue', name: 'Flame Tongue', desc: 'Blade wreathed in fire', type: 'weapon', attack: 30, statBonus: { int: 4 }, requirements: { str: 14, int: 8 }, value: 350 },
  void_staff: { id: 'void_staff', name: 'Void Staff', desc: 'Draws power from darkness', type: 'weapon', attack: 10, statBonus: { int: 16 }, requirements: { int: 20 }, value: 400 },
  dragon_bone: { id: 'dragon_bone', name: 'Dragon Bone Sword', desc: 'Forged from dragon remains', type: 'weapon', attack: 35, statBonus: { str: 5, con: 3 }, requirements: { str: 20, con: 12 }, value: 500 },
  moonblade: { id: 'moonblade', name: 'Moonblade', desc: 'Silver blade glowing in moonlight', type: 'weapon', attack: 32, statBonus: { luck: 6 }, requirements: { dex: 18, luck: 10 }, value: 450 },
  rune_dagger: { id: 'rune_dagger', name: 'Rune Dagger', desc: 'Etched with ancient runes', type: 'weapon', attack: 16, statBonus: { int: 6, dex: 4 }, requirements: { int: 8, dex: 10 }, value: 160 },
  great_mace: { id: 'great_mace', name: 'Great Mace', desc: 'Devastating blunt weapon', type: 'weapon', attack: 38, requirements: { str: 22, con: 14 }, value: 550 },
  elven_bow: { id: 'elven_bow', name: 'Elven Bow', desc: 'Graceful and deadly accurate', type: 'weapon', attack: 24, statBonus: { dex: 8 }, requirements: { dex: 16 }, value: 280 },
  soul_reaper: { id: 'soul_reaper', name: 'Soul Reaper', desc: 'Drains life on hit', type: 'weapon', attack: 40, statBonus: { luck: 4 }, requirements: { str: 18, luck: 8 }, value: 600 },
  arcane_scepter: { id: 'arcane_scepter', name: 'Arcane Scepter', desc: 'Pure magical energy focus', type: 'weapon', attack: 12, statBonus: { int: 20 }, requirements: { int: 22 }, value: 650 },
  shadow_katana: { id: 'shadow_katana', name: 'Shadow Katana', desc: 'Cuts through shadow itself', type: 'weapon', attack: 28, statBonus: { dex: 10, luck: 5 }, requirements: { dex: 20, luck: 8 }, value: 480 },

  // === ARMOR (12) ===
  leather: { id: 'leather', name: 'Leather Armor', desc: 'Basic protection', type: 'armor', defense: 5, requirements: { dex: 3 }, value: 40 },
  chain: { id: 'chain', name: 'Chain Mail', desc: 'Metal ring links', type: 'armor', defense: 15, requirements: { con: 10 }, value: 100 },
  plate: { id: 'plate', name: 'Plate Armor', desc: 'Heavy full-body armor', type: 'armor', defense: 25, requirements: { str: 16, con: 14 }, value: 250 },
  mithril: { id: 'mithril', name: 'Mithril Vest', desc: 'Light yet strong', type: 'armor', defense: 20, statBonus: { dex: 4 }, requirements: { dex: 12 }, value: 300 },
  dragon_scale: { id: 'dragon_scale', name: 'Dragon Scale Mail', desc: 'Near-impenetrable scales', type: 'armor', defense: 35, statBonus: { con: 5 }, requirements: { str: 18, con: 16 }, value: 500 },
  shadow_cloak: { id: 'shadow_cloak', name: 'Shadow Cloak', desc: 'Blends with darkness', type: 'armor', defense: 12, statBonus: { dex: 8, luck: 4 }, requirements: { dex: 14, luck: 6 }, value: 280 },
  holy_vestment: { id: 'holy_vestment', name: 'Holy Vestment', desc: 'Blessed robes of protection', type: 'armor', defense: 18, statBonus: { int: 6 }, requirements: { int: 10 }, value: 260 },
  iron_bulwark: { id: 'iron_bulwark', name: 'Iron Bulwark', desc: 'Thick iron plate armor', type: 'armor', defense: 30, requirements: { str: 14, con: 18 }, value: 400 },
  phantom_robe: { id: 'phantom_robe', name: 'Phantom Robe', desc: 'Phase through attacks', type: 'armor', defense: 14, statBonus: { int: 10 }, requirements: { int: 16 }, value: 350 },
  battle_plate: { id: 'battle_plate', name: 'Battle Plate', desc: 'Scarred from countless wars', type: 'armor', defense: 28, statBonus: { str: 3, con: 3 }, requirements: { str: 16, con: 14 }, value: 380 },
  celestial_robe: { id: 'celestial_robe', name: 'Celestial Robe', desc: 'Woven from starlight', type: 'armor', defense: 22, statBonus: { int: 12, luck: 3 }, requirements: { int: 18, luck: 6 }, value: 550 },
  void_armor: { id: 'void_armor', name: 'Void Armor', desc: 'Forged in the abyss', type: 'armor', defense: 32, statBonus: { con: 6, str: 4 }, requirements: { str: 18, con: 16 }, value: 580 },

  // === ACCESSORIES (10) ===
  magic_ring: { id: 'magic_ring', name: 'Magic Ring', desc: '+3 INT', type: 'accessory', statBonus: { int: 3 }, requirements: { int: 5 }, value: 80 },
  lucky_charm: { id: 'lucky_charm', name: 'Lucky Charm', desc: '+5 LCK', type: 'accessory', statBonus: { luck: 5 }, requirements: { luck: 8 }, value: 100 },
  warrior_band: { id: 'warrior_band', name: 'Warrior Band', desc: '+4 STR, +2 CON', type: 'accessory', statBonus: { str: 4, con: 2 }, requirements: { str: 8 }, value: 120 },
  rogue_pendant: { id: 'rogue_pendant', name: 'Rogue Pendant', desc: '+5 DEX, +3 LCK', type: 'accessory', statBonus: { dex: 5, luck: 3 }, requirements: { dex: 10 }, value: 140 },
  amulet_flames: { id: 'amulet_flames', name: 'Amulet of Flames', desc: '+8 INT, +2 STR', type: 'accessory', statBonus: { int: 8, str: 2 }, requirements: { int: 12 }, value: 200 },
  ring_fortitude: { id: 'ring_fortitude', name: 'Ring of Fortitude', desc: '+6 CON, +3 STR', type: 'accessory', statBonus: { con: 6, str: 3 }, requirements: { con: 12 }, value: 180 },
  eye_of_truth: { id: 'eye_of_truth', name: 'Eye of Truth', desc: '+10 INT, +4 LCK', type: 'accessory', statBonus: { int: 10, luck: 4 }, requirements: { int: 16 }, value: 300 },
  berserker_ring: { id: 'berserker_ring', name: 'Berserker Ring', desc: '+8 STR, +4 DEX', type: 'accessory', statBonus: { str: 8, dex: 4 }, requirements: { str: 14 }, value: 260 },
  shadow_cloak_acc: { id: 'shadow_cloak_acc', name: 'Shadow Amulet', desc: '+6 DEX, +6 LCK', type: 'accessory', statBonus: { dex: 6, luck: 6 }, requirements: { dex: 14, luck: 10 }, value: 350 },
  crown_sovereign: { id: 'crown_sovereign', name: 'Crown of the Sovereign', desc: '+5 all stats', type: 'accessory', statBonus: { str: 5, dex: 5, int: 5, con: 5, luck: 5 }, requirements: { str: 12, int: 12 }, value: 500 },

  // === CONSUMABLES (10) ===
  hp_pot: { id: 'hp_pot', name: 'Health Potion', desc: 'Restores 50 HP', type: 'consumable', healAmount: 50, value: 25 },
  mp_pot: { id: 'mp_pot', name: 'Mana Potion', desc: 'Restores 30 MP', type: 'consumable', mpAmount: 30, value: 20 },
  herb: { id: 'herb', name: 'Healing Herb', desc: 'Heals 25 HP', type: 'consumable', healAmount: 25, value: 10 },
  hi_pot: { id: 'hi_pot', name: 'Hi-Potion', desc: 'Restores 120 HP', type: 'consumable', healAmount: 120, value: 60 },
  ether: { id: 'ether', name: 'Ether', desc: 'Restores 60 MP', type: 'consumable', mpAmount: 60, value: 50 },
  elixir: { id: 'elixir', name: 'Elixir', desc: 'Restores 200 HP and 100 MP', type: 'consumable', healAmount: 200, mpAmount: 100, value: 150 },
  antidote: { id: 'antidote', name: 'Antidote', desc: 'Cures poison, heals 10 HP', type: 'consumable', healAmount: 10, value: 8 },
  bomb: { id: 'bomb', name: 'Bomb', desc: 'Deals 80 fixed damage', type: 'consumable', damage: 80, value: 40 },
  smoke_bomb: { id: 'smoke_bomb', name: 'Smoke Bomb', desc: 'Guarantees escape from battle', type: 'consumable', escape: true, value: 30 },
  phoenix_down: { id: 'phoenix_down', name: 'Phoenix Down', desc: 'Revives with 1 HP in battle', type: 'consumable', revive: true, value: 100 },
}

export const QUESTS = [
  { id: 'q_slime', name: 'Slime Extermination', desc: 'Defeat 5 slimes in the Green Plains.', type: 'kill', target: 'slime', count: 5, reward: { gold: 50, exp: 30 }, reqLevel: 1 },
  { id: 'q_rat', name: 'Rat Problem', desc: 'Eliminate 3 giant rats from the plains.', type: 'kill', target: 'rat', count: 3, reward: { gold: 40, exp: 20 }, reqLevel: 1 },
  { id: 'q_goblin', name: 'Goblin Menace', desc: 'Slay 4 goblins in the Dark Forest.', type: 'kill', target: 'goblin', count: 4, reward: { gold: 80, exp: 60 }, reqLevel: 2 },
  { id: 'q_wolf', name: 'Wolf Hunt', desc: 'Hunt down 3 wolves in the forest.', type: 'kill', target: 'wolf', count: 3, reward: { gold: 90, exp: 70 }, reqLevel: 3 },
  { id: 'q_bat', name: 'Cave Cleanup', desc: 'Clear 5 giant bats from the Mystic Cave.', type: 'kill', target: 'bat', count: 5, reward: { gold: 70, exp: 50 }, reqLevel: 2 },
  { id: 'q_spider', name: 'Spider Nest', desc: 'Destroy 4 poison spiders.', type: 'kill', target: 'spider', count: 4, reward: { gold: 100, exp: 80 }, reqLevel: 3 },
  { id: 'q_troll', name: 'Swamp Terror', desc: 'Defeat 2 swamp trolls.', type: 'kill', target: 'swamp_troll', count: 2, reward: { gold: 150, exp: 120 }, reqLevel: 5 },
  { id: 'q_skeleton', name: 'Undead Rising', desc: 'Put 5 skeletons to rest.', type: 'kill', target: 'skeleton', count: 5, reward: { gold: 130, exp: 100 }, reqLevel: 4 },
  { id: 'q_dknight', name: 'Dark Knight\'s Fall', desc: 'Defeat 3 dark knights.', type: 'kill', target: 'dark_knight', count: 3, reward: { gold: 250, exp: 200 }, reqLevel: 7 },
  { id: 'q_dragon', name: 'Dragon Slayer', desc: 'Slay the dragon on Dragon Mountain.', type: 'kill', target: 'dragon', count: 1, reward: { gold: 500, exp: 400 }, reqLevel: 8 },
  { id: 'q_dmage', name: 'Banish the Dark Mage', desc: 'Defeat 2 dark mages in the tower.', type: 'kill', target: 'dark_mage', count: 2, reward: { gold: 300, exp: 250 }, reqLevel: 8 },
  { id: 'q_boss', name: 'The Dark Lord', desc: 'Defeat the Dark Lord himself!', type: 'kill', target: 'boss', count: 1, reward: { gold: 1000, exp: 800 }, reqLevel: 10 },
  { id: 'q_herb', name: 'Herb Collection', desc: 'Gather 5 healing herbs.', type: 'collect', target: 'herb', count: 5, reward: { gold: 60, exp: 40 }, reqLevel: 1 },
  { id: 'q_explorer', name: 'Cartographer', desc: 'Visit all 8 locations.', type: 'visit', target: 'all', count: 8, reward: { gold: 200, exp: 150 }, reqLevel: 1 },
  { id: 'q_lv5', name: 'Rising Star', desc: 'Reach level 5.', type: 'level', target: 5, count: 1, reward: { gold: 100, exp: 80 }, reqLevel: 1 },
  { id: 'q_lv10', name: 'Veteran Hero', desc: 'Reach level 10.', type: 'level', target: 10, count: 1, reward: { gold: 300, exp: 200 }, reqLevel: 5 },
  { id: 'q_gold', name: 'Wealthy Adventurer', desc: 'Accumulate 500 gold.', type: 'gold', target: 500, count: 1, reward: { gold: 100, exp: 60 }, reqLevel: 1 },
  { id: 'q_battle20', name: 'Battle Hardened', desc: 'Win 20 battles.', type: 'battles', target: 20, count: 1, reward: { gold: 150, exp: 100 }, reqLevel: 3 },
]

export const ENEMIES = {
  slime: { name: 'Slime', level: 1, hp: 20, attack: 5, defense: 1, expReward: 10, goldReward: 5 },
  rat: { name: 'Giant Rat', level: 1, hp: 25, attack: 7, defense: 2, expReward: 12, goldReward: 6 },
  goblin: { name: 'Goblin', level: 2, hp: 35, attack: 10, defense: 3, expReward: 20, goldReward: 10 },
  wolf: { name: 'Wolf', level: 3, hp: 50, attack: 14, defense: 4, expReward: 30, goldReward: 15 },
  bat: { name: 'Giant Bat', level: 2, hp: 28, attack: 9, defense: 2, expReward: 18, goldReward: 8 },
  spider: { name: 'Poison Spider', level: 3, hp: 42, attack: 13, defense: 5, expReward: 32, goldReward: 16 },
  swamp_troll: { name: 'Swamp Troll', level: 5, hp: 80, attack: 18, defense: 8, expReward: 55, goldReward: 28 },
  skeleton: { name: 'Skeleton', level: 4, hp: 55, attack: 16, defense: 7, expReward: 40, goldReward: 20 },
  dragon: { name: 'Dragon', level: 8, hp: 200, attack: 40, defense: 20, expReward: 200, goldReward: 100 },
  dark_knight: { name: 'Dark Knight', level: 7, hp: 150, attack: 30, defense: 18, expReward: 120, goldReward: 60 },
  dark_mage: { name: 'Dark Mage', level: 8, hp: 100, attack: 35, defense: 10, expReward: 150, goldReward: 75 },
  boss: { name: 'Dark Lord', level: 10, hp: 350, attack: 50, defense: 25, expReward: 500, goldReward: 250 },
}

export const MAP = {
  village: { name: 'Starting Village', desc: 'A peaceful village.', enemies: [], npcs: ['Elder', 'Merchant'], exits: { N: 'forest', E: 'cave', S: 'plains' } },
  plains: { name: 'Green Plains', desc: 'Open grasslands.', enemies: ['slime', 'rat'], npcs: [], exits: { N: 'village', E: 'swamp' } },
  forest: { name: 'Dark Forest', desc: 'Dangerous forest.', enemies: ['goblin', 'wolf'], npcs: [], exits: { S: 'village', N: 'mountain' } },
  cave: { name: 'Mystic Cave', desc: 'Glowing crystals.', enemies: ['bat', 'spider'], npcs: [], exits: { W: 'village', E: 'dungeon' } },
  swamp: { name: 'Murky Swamp', desc: 'Beware poison.', enemies: ['swamp_troll'], npcs: [], exits: { W: 'plains', N: 'cave' } },
  mountain: { name: 'Dragon Mountain', desc: 'Dragons nest here.', enemies: ['dragon'], npcs: [], exits: { S: 'forest' } },
  dungeon: { name: 'Ancient Dungeon', desc: 'Overrun by monsters.', enemies: ['skeleton', 'dark_knight'], npcs: [], exits: { W: 'cave', E: 'tower' } },
  tower: { name: 'Dark Tower', desc: 'Dark energy.', enemies: ['dark_mage', 'boss'], npcs: [], exits: { W: 'swamp' } },
}

export const MAP_POSITIONS = {
  village: [2, 2], forest: [2, 1], mountain: [2, 0],
  plains: [1, 2], cave: [3, 2], dungeon: [4, 2],
  swamp: [1, 3], tower: [4, 3],
}

export const MAP_CONNECTIONS = [
  ['village', 'forest'], ['village', 'cave'], ['village', 'plains'],
  ['forest', 'mountain'], ['plains', 'swamp'], ['cave', 'dungeon'],
  ['cave', 'swamp'], ['dungeon', 'tower'],
]

export const HERB_LOCATIONS = new Set(['plains', 'forest', 'swamp'])

export const CLASS_STATS = {
  Warrior: { str: 7, con: 6 },
  Rogue: { dex: 7, luck: 6 },
  Mage: { int: 7, dex: 5 },
}

export const SHOP_ITEMS = Object.values(ITEMS).filter(
  i => ['weapon', 'armor', 'accessory', 'consumable'].includes(i.type) && i.value <= 350
)

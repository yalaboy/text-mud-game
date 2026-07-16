# RPG Graphical - Project History

## Overview

A graphical RPG with two implementations:
1. **Pygame version** (`rpg_graphical.py`, ~913 lines) — desktop app
2. **React web version** (`rpg-web/`, ~67 modules) — browser app

---

## React Web Version (`rpg-web/`)

### Quick Start
```bash
cd rpg-web
npm install
npm run dev      # dev server at http://localhost:3000
npm run build    # production build to dist/
```

### Tech Stack
- **Vite** — build tool / dev server
- **React 18** — UI (useReducer for state)
- **Pure CSS** — no framework, custom dark theme matching Pygame version

### Project Structure
```
rpg-web/
├── src/
│   ├── App.jsx              # Root component, screen router
│   ├── main.jsx             # Entry point
│   ├── index.css            # Global styles + shared list-screen styles
│   ├── data/
│   │   └── gameData.js      # All constants (MAP, ITEMS, ENEMIES, SKILLS, etc.)
│   ├── logic/
│   │   └── gameReducer.js   # All game state transitions (useReducer)
│   ├── components/
│   │   ├── Button.jsx/css   # Reusable button with color variants
│   │   ├── HealthBar.jsx/css
│   │   ├── MessageToast.jsx/css
│   │   └── Minimap.jsx/css  # SVG minimap with fog of war
│   └── screens/
│       ├── MainMenu.jsx/css
│       ├── ClassSelect.jsx/css
│       ├── NamingScreen.jsx/css
│       ├── MainScreen.jsx/css    # Main game hub with minimap
│       ├── BattleScreen.jsx/css  # Combat with skill/item submenus
│       ├── InventoryScreen.jsx
│       ├── SkillsScreen.jsx
│       ├── EquipScreen.jsx
│       ├── ItemUseScreen.jsx
│       ├── MoveScreen.jsx
│       ├── NPCScreen.jsx
│       ├── ShopScreen.jsx
│       └── LevelUpScreen.jsx/css
```

### Architecture
- **State machine**: `gameState.state` string drives which screen renders (same pattern as Pygame `self.state`)
- **Reducer**: `gameReducer(state, action)` handles all transitions — one action per user action
- **No router**: screens swap via reducer state, not URL routing
- **No backend**: everything runs in browser, state lives in memory
- **Visited locations** tracked via `Set` in reducer state (fog of war on minimap)
- **60fps message timer**: `useEffect` interval dispatches `TICK` actions for toast fadeout

---

## Game Features

### Core Systems
- **3 Classes**: Warrior (STR/CON), Rogue (DEX/LCK), Mage (INT)
- **5 Stats**: STR, DEX, INT, CON, LCK (auto-level all +1 per level, 5 bonus points to distribute)
- **7 Skills**: Unlocked by meeting stat requirements (Power Strike, Cleave, Backstab, Fireball, Ice Shard, Lightning Bolt, Heal)
- **12 Items**: Weapons, armor, accessories, consumables (health/mana potions, herbs)
- **12 Enemies**: Scaling from Slime (Lv1) to Dark Lord boss (Lv10)
- **8 Map Locations** with directional movement (N/S/E/W)
- **Combat**: Attack (with crits), Skills, Items, Defend, Run
- **NPCs**: Elder (lore hint), Merchant (shop with items up to 200g)
- **Rest**: Costs 10g, fully restores HP/MP
- **Level Up**: 5 stat points to distribute after each level

### Map Layout
```
         mountain
             |
         forest
             |
plains - village - cave - dungeon
  |                   |
swamp ----------- tower
```

### Locations & Enemies
| Location | Enemies | Herb? | NPCs |
|----------|---------|-------|------|
| Starting Village | none | no | Elder, Merchant |
| Green Plains | slime, rat | yes | - |
| Dark Forest | goblin, wolf | yes | - |
| Mystic Cave | bat, spider | no | - |
| Murky Swamp | swamp_troll | yes | - |
| Dragon Mountain | dragon | no | - |
| Ancient Dungeon | skeleton, dark_knight | no | - |
| Dark Tower | dark_mage, boss | no | - |

---

## Change History

### Session 1 (current)
All changes in `rpg_graphical.py`:

1. **Back buttons for Inventory/Status screens** (lines 292-295, 696-700)
   - Bug: `create_buttons` had no cases for `"inventory"` or `"skills_list"` states, so no buttons rendered -- player was stuck
   - Added "Back" button at bottom center for both states
   - Handler returns to main state and resets scroll offset

2. **Inventory/skills_list scroll support** (lines 505-518, 520-532, 595-603)
   - Bug: Too many items overflowed beyond window, covering action buttons
   - Added MOUSEWHEEL event handling (scroll 30px per tick)
   - `draw_inventory`: items rendered with `scroll_offset` applied to y, items outside visible area skipped
   - `draw_skills_list`: same scroll treatment
   - Scroll clamped to prevent over-scrolling either direction
   - Scroll offset resets on state entry/exit

3. **Herb find locations restricted** (lines 209, 864)
   - Bug: Herbs found in all locations including towns
   - Added `HERB_LOCATIONS = {"plains", "forest", "swamp"}` constant
   - `do_explore`: herb finding now checks `self.location in HERB_LOCATIONS`

4. **Compact minimap with fog of war** (lines 211-220, 253, 444, 446-479, 808)
   - Added `MAP_POSITIONS` dict (grid coordinates) and `MAP_CONNECTIONS` list
   - `self.visited` set initialized with `{"village"}`, updated on movement
   - `draw_minimap()`: semi-transparent overlay (290x230px) in top-right of main screen
   - Only shows visited locations (fog of war)
   - Lines drawn between connected visited locations
   - Current location: yellow circle (r=12), visited: cyan (r=8)
   - Location name labels below nodes

### Session 2
Ported to React web app in `rpg-web/`:

1. **Full React port** — all game features ported to browser
   - Vite + React 18 setup
   - `gameReducer.js` — centralized state management via useReducer
   - `gameData.js` — all constants extracted to separate module
   - 13 screen components, 4 shared components
   - Pure CSS dark theme matching Pygame colors
   - SVG-based minimap with fog of war
   - Mouse wheel scrolling for inventory/skills
   - Build verified: `npm run build` succeeds

---

## Known Issues / Future Work

- [ ] No save/load system
- [ ] No death animation or respawn mechanic (just returns to menu)
- [ ] Level-up stat allocation screen lacks visual feedback for remaining points
- [ ] Shop doesn't show player gold or prevent buying what you can't afford (gold check only at purchase)
- [ ] No equipment comparison tooltip
- [ ] `DIR_MAP` constant (line 207) is defined but never used
- [ ] `BTN_ACTIVE` color (line 23) is defined but never used
- [ ] Battle screen doesn't show enemy skills/abilities
- [ ] No audio/music
- [ ] No animation system (all state-based)
- [ ] **React version**: no localStorage save/load (easy to add)
- [ ] **React version**: visited Set doesn't persist across re-renders (needs serialization for save)

---

## Session 3 — Quest System, 50 Skills/Items, Elder Interaction

Added quest system with Elder NPC giving 18 quests (kill, collect, visit, level, gold types).

### Pygame Changes (`rpg_graphical.py`):
- **50 skills** (15 physical, 15 magic, 10 heal, 5 buff, 5 debuff) replacing 7
- **50 items** (18 weapons, 12 armor, 10 accessories, 10 consumables) replacing 12
- **18 quests** with `Quest` class and `QUESTS` list
- **Elder NPC** now opens quest screen instead of static message
- Quest tracking: `quest_status`, `active_quests`, `kill_counts`, `battle_count`
- `check_quest_complete()` and `check_quest_kill()` methods for quest progress
- Battle victory triggers quest kill tracking

### React Changes (`rpg-web/`):
- **App.jsx**: Added `ElderQuestScreen` import, `elder_quest` case, quest fields in initialState
- **gameData.js**: 18 quests with `reqLevel` gating, shop shows items up to 350g
- **gameReducer.js**: Quest tracking (kill/collect/visit/level/gold), rest restricted to village
- **ElderQuestScreen.jsx/css**: Quest UI with accept/complete/view
- **MainScreen.jsx**: Rest button shows red when not in village
- Build verified: `npx vite build` succeeds

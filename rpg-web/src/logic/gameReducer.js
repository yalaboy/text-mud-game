import { MAP, ITEMS, ENEMIES, SKILLS, QUESTS, HERB_LOCATIONS, CLASS_STATS } from '../data/gameData'

function getStat(stats, equipped, s) {
  const base = stats[s] || 0
  const bonus = equipped.reduce((sum, item) => sum + (item.statBonus?.[s] || 0), 0)
  return base + bonus
}

function getAttack(stats, equipped) {
  const weapon = equipped.find(i => i.type === 'weapon')
  return getStat(stats, equipped, 'str') * 2 + (weapon?.attack || 0)
}

function getMagicAttack(stats, equipped) {
  return getStat(stats, equipped, 'int') * 3
}

function getDefense(stats, equipped) {
  const armor = equipped.find(i => i.type === 'armor')
  return getStat(stats, equipped, 'con') + (armor?.defense || 0)
}

function canEquip(item, stats, equipped) {
  return Object.entries(item.requirements || {}).every(([s, v]) => getStat(stats, equipped, s) >= v)
}

function getLearnedSkills(stats) {
  return SKILLS.filter(sk =>
    Object.entries(sk.statReq).every(([s, v]) => (stats[s] || 0) >= v)
  )
}

function createEnemy(template, level) {
  const lv = Math.max(1, level + Math.floor(Math.random() * 3) - 1)
  const scale = 1 + (lv - template.level) * 0.2
  const atkScale = 1 + (lv - template.level) * 0.15
  return {
    ...template,
    level: lv,
    hp: Math.floor(template.hp * scale),
    maxHp: Math.floor(template.hp * scale),
    attack: Math.floor(template.attack * atkScale),
  }
}

function checkQuestProgress(quest, player, visited, killCounts, battleCount) {
  switch (quest.type) {
    case 'kill':
      return (killCounts[quest.target] || 0) >= quest.count
    case 'collect':
      return player.inventory.filter(i => i.id === quest.target).length >= quest.count
    case 'visit':
      if (quest.target === 'all') return visited.size >= quest.count
      return visited.has(quest.target)
    case 'level':
      return player.level >= quest.target
    case 'gold':
      return player.gold >= quest.target
    case 'battles':
      return battleCount >= quest.target
    default:
      return false
  }
}

function updateQuestProgress(questId, state) {
  const qs = { ...state.questStatus }
  const q = qs[questId]
  if (!q || q.completed || q.claimed) return qs
  const quest = QUESTS.find(qq => qq.id === questId)
  if (!quest) return qs
  if (checkQuestProgress(quest, state.player, state.visited, state.killCounts, state.battleCount)) {
    qs[questId] = { ...q, readyToClaim: true }
  }
  return qs
}

const initialState = {
  state: 'menu',
  player: null,
  playerName: '',
  location: 'village',
  visited: new Set(['village']),
  enemy: null,
  message: '',
  msgTimer: 0,
  levelPoints: 5,
  scrollOffset: 0,
  questStatus: {},
  killCounts: {},
  battleCount: 0,
  activeQuests: [],
  lastKilledEnemy: null,
}

export function gameReducer(state, action) {
  const s = { ...state }

  switch (action.type) {
    case 'START_GAME':
      s.state = 'naming'
      s.playerName = ''
      return s

    case 'CONFIRM_NAME':
      s.state = 'class_select'
      return s

    case 'SET_NAME':
      s.playerName = action.name
      return s

    case 'SELECT_CLASS': {
      const cls = action.classType
      const bonuses = CLASS_STATS[cls]
      const stats = { str: 5, dex: 5, int: 5, con: 5, luck: 5 }
      Object.entries(bonuses).forEach(([k, v]) => { stats[k] = v })
      s.player = {
        name: state.playerName || 'Hero',
        classType: cls,
        level: 1,
        exp: 0,
        expToLevel: 100,
        hp: 100,
        maxHp: 100,
        mp: 50,
        maxMp: 50,
        gold: 50,
        stats,
        equipment: { weapon: null, armor: null, accessory: null },
        inventory: [
          { ...ITEMS.hp_pot, uid: Date.now() },
          { ...ITEMS.hp_pot, uid: Date.now() + 1 },
        ],
        equippedItems: [],
        skills: getLearnedSkills(stats),
      }
      s.state = 'main'
      s.location = 'village'
      s.visited = new Set(['village'])
      s.questStatus = {}
      s.killCounts = {}
      s.battleCount = 0
      s.activeQuests = []
      return s
    }

    case 'NAVIGATE':
      s.state = action.target
      s.scrollOffset = 0
      return s

    case 'GO_BACK':
      s.state = 'main'
      s.scrollOffset = 0
      return s

    case 'SCROLL':
      s.scrollOffset = Math.min(0, s.scrollOffset + action.delta)
      return s

    case 'MOVE': {
      const loc = MAP[state.location]
      const dest = loc.exits[action.direction]
      if (dest) {
        s.location = dest
        s.visited = new Set([...state.visited, dest])
        s.message = `Traveled to ${MAP[dest].name}`
        s.msgTimer = 180
        // Update quest progress for visit quests
        s.activeQuests = state.activeQuests.map(qid => updateQuestProgress(qid, { ...s }))
        s.questStatus = { ...s.questStatus }
        s.activeQuests.forEach(qid => {
          if (s.questStatus[qid]) s.questStatus[qid] = { ...s.questStatus[qid] }
        })
      }
      s.state = 'main'
      return s
    }

    case 'EXPLORE': {
      const loc = MAP[state.location]
      const roll = Math.random()
      if (roll < 0.6 && loc.enemies.length > 0) {
        const etype = loc.enemies[Math.floor(Math.random() * loc.enemies.length)]
        s.enemy = createEnemy(ENEMIES[etype], ENEMIES[etype].level)
        s.lastKilledEnemy = null
        s.state = 'battle'
        s.message = `${s.enemy.name} appeared!`
        s.msgTimer = 180
      } else if (roll < 0.8 && HERB_LOCATIONS.has(state.location)) {
        s.player = { ...s.player, inventory: [...s.player.inventory, { ...ITEMS.herb, uid: Date.now() }] }
        s.message = 'Found a Healing Herb!'
        s.msgTimer = 180
        s.activeQuests = state.activeQuests.map(qid => updateQuestProgress(qid, { ...s }))
        s.questStatus = { ...s.questStatus }
        s.activeQuests.forEach(qid => {
          if (s.questStatus[qid]) s.questStatus[qid] = { ...s.questStatus[qid] }
        })
      } else {
        s.message = 'Nothing interesting found.'
        s.msgTimer = 180
      }
      return s
    }

    case 'REST': {
      if (state.location !== 'village') {
        s.message = 'You can only rest in the village!'
        s.msgTimer = 180
        return s
      }
      if (s.player.gold >= 10) {
        s.player = { ...s.player, gold: s.player.gold - 10, hp: s.player.maxHp, mp: s.player.maxMp }
        s.message = 'Rested! HP and MP restored.'
      } else {
        s.message = 'Not enough gold!'
      }
      s.msgTimer = 180
      return s
    }

    case 'TALK': {
      const npc = action.npc
      if (npc === 'Merchant') {
        s.state = 'npc_shop'
      } else if (npc === 'Elder') {
        s.state = 'elder_quest'
      } else {
        s.message = `Talked to ${npc}`
        s.msgTimer = 180
      }
      return s
    }

    case 'ACCEPT_QUEST': {
      const questId = action.questId
      if (!state.activeQuests.includes(questId)) {
        s.activeQuests = [...state.activeQuests, questId]
        s.questStatus = { ...state.questStatus, [questId]: { completed: false, claimed: false, readyToClaim: false } }
        const quest = QUESTS.find(q => q.id === questId)
        s.message = `Accepted: ${quest.name}`
        s.msgTimer = 180
      }
      return s
    }

    case 'CLAIM_QUEST': {
      const questId = action.questId
      const qs = { ...state.questStatus }
      const q = qs[questId]
      if (q && q.readyToClaim && !q.claimed) {
        const quest = QUESTS.find(qq => qq.id === questId)
        qs[questId] = { ...q, claimed: true, completed: true }
        s.questStatus = qs
        s.player = {
          ...s.player,
          gold: s.player.gold + quest.reward.gold,
          exp: s.player.exp + quest.reward.exp,
        }
        s.message = `Quest complete! +${quest.reward.gold}g +${quest.reward.exp}exp`
        s.msgTimer = 180
        // Check level up
        while (s.player.exp >= s.player.expToLevel) {
          s.player = levelUp(s.player)
          s.state = 'level_up'
          s.levelPoints = 5
        }
      }
      return s
    }

    case 'BUY_ITEM': {
      const item = action.item
      if (s.player.gold >= item.value) {
        s.player = {
          ...s.player,
          gold: s.player.gold - item.value,
          inventory: [...s.player.inventory, { ...item, uid: Date.now() }],
        }
        s.message = `Bought ${item.name}!`
        // Update gold quests
        s.activeQuests = state.activeQuests.map(qid => updateQuestProgress(qid, { ...s }))
        s.questStatus = { ...s.questStatus }
        s.activeQuests.forEach(qid => {
          if (s.questStatus[qid]) s.questStatus[qid] = { ...s.questStatus[qid] }
        })
      } else {
        s.message = 'Not enough gold!'
      }
      s.msgTimer = 180
      return s
    }

    case 'USE_ITEM': {
      const item = action.item
      const newInv = [...s.player.inventory]
      const idx = newInv.findIndex(i => i.uid === item.uid)
      if (idx === -1) return s
      newInv.splice(idx, 1)
      let hp = s.player.hp
      let mp = s.player.mp
      let msg = ''

      if (item.damage && s.enemy) {
        const actual = Math.max(1, item.damage - Math.floor(s.enemy.defense / 2))
        s.enemy = { ...s.enemy, hp: Math.max(0, s.enemy.hp - actual) }
        msg = `Used ${item.name}! Dealt ${actual} damage!`
      } else if (item.escape) {
        s.enemy = null
        s.state = 'main'
        msg = `Used ${item.name}! Escaped safely!`
      } else if (item.revive) {
        hp = Math.max(hp, 1)
        msg = `Used ${item.name}! Revived with 1 HP!`
      } else {
        if (item.healAmount) {
          hp = Math.min(s.player.maxHp, hp + item.healAmount)
          msg = `Used ${item.name}. Healed ${item.healAmount} HP!`
        }
        if (item.mpAmount) {
          mp = Math.min(s.player.maxMp, mp + item.mpAmount)
          msg = msg ? `${msg} +${item.mpAmount} MP!` : `Used ${item.name}. Restored ${item.mpAmount} MP!`
        }
      }

      s.player = { ...s.player, inventory: newInv, hp, mp }
      s.message = msg
      s.msgTimer = 180

      // Check if bomb killed enemy
      if (item.damage && s.enemy && s.enemy.hp <= 0) {
        return doVictory(s)
      }

      if (s.state === 'item_use' && s.enemy) {
        s.state = 'battle'
      }
      return s
    }

    case 'EQUIP': {
      const item = action.item
      if (!canEquip(item, s.player.stats, s.player.equippedItems)) {
        s.message = 'Cannot equip!'
        s.msgTimer = 180
        return s
      }
      const newInv = s.player.inventory.filter(i => i.uid !== item.uid)
      const newEquipped = s.player.equippedItems.filter(i => i.type !== item.type)
      const newEquip = { ...s.player.equipment }
      const unequipped = s.player.equipment[item.type]
      if (unequipped) newInv.push(unequipped)
      newEquip[item.type] = item
      newEquipped.push(item)
      s.player = { ...s.player, inventory: newInv, equipment: newEquip, equippedItems: newEquipped }
      s.message = `Equipped ${item.name}!`
      s.msgTimer = 180
      return s
    }

    case 'PLAYER_ATTACK': {
      if (Math.random() < getStat(s.player.stats, s.player.equippedItems, 'dex') / 150) {
        s.message = 'You missed!'
        s.msgTimer = 180
      } else {
        let dmg = getAttack(s.player.stats, s.player.equippedItems) + Math.floor(Math.random() * 8) - 2
        const crit = Math.random() < getStat(s.player.stats, s.player.equippedItems, 'luck') / 100
        if (crit) dmg = Math.floor(dmg * 1.8)
        const actual = Math.max(1, dmg - Math.floor(s.enemy.defense / 2))
        const newHp = Math.max(0, s.enemy.hp - actual)
        s.enemy = { ...s.enemy, hp: newHp }
        s.message = crit ? `CRITICAL HIT! Dealt ${actual} damage!` : `Dealt ${actual} damage!`
        s.msgTimer = 180
      }
      if (s.enemy.hp <= 0) {
        return doVictory(s)
      }
      return doEnemyTurn(s)
    }

    case 'USE_SKILL': {
      const skill = action.skill
      if (s.player.mp < skill.mpCost) {
        s.message = 'Not enough MP!'
        s.msgTimer = 180
        return s
      }
      s.player = { ...s.player, mp: s.player.mp - skill.mpCost }

      if (skill.type === 'physical') {
        const dmg = Math.floor(getAttack(s.player.stats, s.player.equippedItems) * skill.power + Math.floor(Math.random() * 12) - 3)
        const actual = Math.max(1, dmg - Math.floor(s.enemy.defense / 2))
        s.enemy = { ...s.enemy, hp: Math.max(0, s.enemy.hp - actual) }
        s.message = `${skill.name}! Dealt ${actual} damage!`
      } else if (skill.type === 'magic') {
        const dmg = Math.floor(getMagicAttack(s.player.stats, s.player.equippedItems) * skill.power + Math.floor(Math.random() * 16) - 5)
        const actual = Math.max(1, dmg - Math.floor(s.enemy.defense / 2))
        s.enemy = { ...s.enemy, hp: Math.max(0, s.enemy.hp - actual) }
        s.message = `${skill.name}! Dealt ${actual} magic damage!`
      } else if (skill.type === 'heal') {
        const heal = Math.floor(skill.power + getStat(s.player.stats, s.player.equippedItems, 'int') * 2)
        s.player = { ...s.player, hp: Math.min(s.player.maxHp, s.player.hp + heal) }
        s.message = `${skill.name}! Healed ${heal} HP!`
      } else if (skill.type === 'buff') {
        const boost = Math.floor(getAttack(s.player.stats, s.player.equippedItems) * skill.power)
        s.player = { ...s.player, hp: Math.min(s.player.maxHp, s.player.hp + boost) }
        s.message = `${skill.name}! Power surges through you!`
      } else if (skill.type === 'debuff') {
        const weaken = Math.floor(s.enemy.attack * (1 - skill.power))
        s.enemy = { ...s.enemy, attack: Math.max(1, s.enemy.attack - weaken) }
        s.message = `${skill.name}! Enemy weakened!`
      }

      s.msgTimer = 180
      if (s.enemy.hp <= 0) {
        return doVictory(s)
      }
      return doEnemyTurn(s)
    }

    case 'DEFEND': {
      const dmg = Math.floor(s.enemy.attack / 2)
      const actual = Math.max(1, dmg - Math.floor(getDefense(s.player.stats, s.player.equippedItems) / 2))
      s.player = { ...s.player, hp: Math.max(0, s.player.hp - actual) }
      s.message = `Defending! Took ${actual} damage reduced.`
      s.msgTimer = 180
      if (s.player.hp <= 0) {
        s.state = 'menu'
        s.enemy = null
        return s
      }
      return doEnemyTurn(s)
    }

    case 'RUN': {
      if (Math.random() < 0.5 + getStat(s.player.stats, s.player.equippedItems, 'dex') / 100) {
        s.message = 'Escaped!'
        s.msgTimer = 180
        s.enemy = null
        s.state = 'main'
      } else {
        s.message = 'Failed to run!'
        s.msgTimer = 180
        return doEnemyTurn(s)
      }
      return s
    }

    case 'ALLOCATE_STAT': {
      const stat = action.stat
      s.levelPoints = state.levelPoints - 1
      s.player = {
        ...s.player,
        stats: { ...s.player.stats, [stat]: s.player.stats[stat] + 1 },
        skills: getLearnedSkills({ ...s.player.stats, [stat]: s.player.stats[stat] + 1 }),
      }
      s.message = `${stat.toUpperCase()} +1!`
      s.msgTimer = 180
      if (s.levelPoints <= 0) {
        s.state = 'main'
      }
      return s
    }

    case 'TICK':
      if (s.msgTimer > 0) s.msgTimer -= 1
      return s

    default:
      return s
  }
}

function levelUp(player) {
  let { level, exp, expToLevel, maxHp, maxMp, stats } = player
  exp -= expToLevel
  level += 1
  expToLevel = Math.floor(expToLevel * 1.5)
  maxHp += 10
  maxMp += 5
  stats = {
    str: stats.str + 1,
    dex: stats.dex + 1,
    int: stats.int + 1,
    con: stats.con + 1,
    luck: stats.luck + 1,
  }
  return {
    ...player,
    level, exp, expToLevel, maxHp, maxMp,
    hp: maxHp, mp: maxMp, stats,
    skills: getLearnedSkills(stats),
  }
}

function doVictory(s) {
  s.message = `Victory! +${s.enemy.expReward} EXP +${s.enemy.goldReward} Gold`
  s.msgTimer = 180

  const enemyType = Object.entries(ENEMIES).find(([, v]) => v.name === s.enemy.name)?.[0]
  const newKillCounts = { ...s.killCounts }
  if (enemyType) {
    newKillCounts[enemyType] = (newKillCounts[enemyType] || 0) + 1
  }

  let player = {
    ...s.player,
    gold: s.player.gold + s.enemy.goldReward,
    exp: s.player.exp + s.enemy.expReward,
  }
  s.enemy = null
  s.killCounts = newKillCounts
  s.battleCount = (s.battleCount || 0) + 1
  s.state = 'main'

  while (player.exp >= player.expToLevel) {
    player = levelUp(player)
    s.state = 'level_up'
    s.levelPoints = 5
  }

  s.player = player

  // Update all active quest progress
  s.activeQuests = (s.activeQuests || []).map(qid => {
    const qs = { ...s.questStatus }
    const q = qs[qid]
    if (!q || q.completed || q.claimed) return qid
    const quest = QUESTS.find(qq => qq.id === qid)
    if (!quest) return qid
    if (checkQuestProgress(quest, s.player, s.visited, s.killCounts, s.battleCount)) {
      qs[qid] = { ...q, readyToClaim: true }
    }
    s.questStatus = qs
    return qid
  })

  return s
}

function doEnemyTurn(s) {
  const dmg = s.enemy.attack + Math.floor(Math.random() * 6) - 2
  const actual = Math.max(1, dmg - Math.floor(getDefense(s.player.stats, s.player.equippedItems) / 2))
  const newHp = Math.max(0, s.player.hp - actual)
  s.player = { ...s.player, hp: newHp }
  s.message = `${s.enemy.name} attacks for ${actual} damage!`
  s.msgTimer = 180
  if (newHp <= 0) {
    s.message = 'GAME OVER!'
    s.enemy = null
    s.state = 'menu'
  }
  return s
}

export { getStat, getAttack, getMagicAttack, getDefense, canEquip, getLearnedSkills, checkQuestProgress }

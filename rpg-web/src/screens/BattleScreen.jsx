import { useState } from 'react'
import { SKILLS } from '../data/gameData'
import { getLearnedSkills } from '../logic/gameReducer'
import Button from '../components/Button'
import HealthBar from '../components/HealthBar'
import './BattleScreen.css'

export default function BattleScreen({ gameState, dispatch }) {
  const [subMenu, setSubMenu] = useState(null)
  const { player, enemy } = gameState

  const learned = getLearnedSkills(player.stats)

  const handleSkillUse = (skill) => {
    dispatch({ type: 'USE_SKILL', skill })
    setSubMenu(null)
  }

  const handleItemUse = (item) => {
    dispatch({ type: 'USE_ITEM', item })
    setSubMenu(null)
  }

  if (subMenu === 'skill') {
    return (
      <div className="screen battle-screen">
        <div className="battle-panel">
          <div className="battle-info">
            <h2 className="battle-title">CHOOSE SKILL</h2>
            <div className="battle-list">
              {learned.slice(0, 6).map((sk, i) => (
                <Button
                  key={i}
                  color="magenta"
                  disabled={player.mp < sk.mpCost}
                  onClick={() => handleSkillUse(sk)}
                >
                  {sk.name} ({sk.mpCost}MP)
                </Button>
              ))}
            </div>
            <Button onClick={() => setSubMenu(null)}>Back</Button>
          </div>
        </div>
      </div>
    )
  }

  if (subMenu === 'item') {
    const consumables = player.inventory.filter(i => i.type === 'consumable')
    return (
      <div className="screen battle-screen">
        <div className="battle-panel">
          <div className="battle-info">
            <h2 className="battle-title">CHOOSE ITEM</h2>
            <div className="battle-list">
              {consumables.slice(0, 6).map((item, i) => (
                <Button key={item.uid || i} color="yellow" onClick={() => handleItemUse(item)}>
                  {item.name}
                </Button>
              ))}
            </div>
            <Button onClick={() => setSubMenu(null)}>Back</Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="screen battle-screen">
      <div className="battle-panel">
        <h2 className="battle-title red">BATTLE</h2>

        <div className="battle-enemy">
          <div className="battle-name">{enemy.name} Lv.{enemy.level}</div>
          <div className="bar-row">
            <span className="bar-label red">HP</span>
            <HealthBar current={enemy.hp} max={enemy.maxHp} color="red" />
            <span className="bar-text red">{enemy.hp}/{enemy.maxHp}</span>
          </div>
        </div>

        <div className="battle-player">
          <div className="battle-name green">{player.name}</div>
          <div className="bar-row">
            <span className="bar-label green">HP</span>
            <HealthBar current={player.hp} max={player.maxHp} color="green" />
            <span className="bar-text green">{player.hp}/{player.maxHp}</span>
          </div>
          <div className="bar-row">
            <span className="bar-label blue">MP</span>
            <HealthBar current={player.mp} max={player.maxMp} color="blue" />
            <span className="bar-text blue">{player.mp}/{player.maxMp}</span>
          </div>
        </div>
      </div>

      <div className="action-bar">
        <div className="action-row">
          <Button color="red" onClick={() => dispatch({ type: 'PLAYER_ATTACK' })}>Attack</Button>
          <Button color="magenta" onClick={() => setSubMenu('skill')}>Skill</Button>
          <Button color="yellow" onClick={() => setSubMenu('item')}>Item</Button>
          <Button color="cyan" onClick={() => dispatch({ type: 'DEFEND' })}>Defend</Button>
          <Button color="green" onClick={() => dispatch({ type: 'RUN' })}>Run</Button>
        </div>
      </div>
    </div>
  )
}

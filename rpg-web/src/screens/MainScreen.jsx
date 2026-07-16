import { MAP } from '../data/gameData'
import { getStat } from '../logic/gameReducer'
import Button from '../components/Button'
import HealthBar from '../components/HealthBar'
import Minimap from '../components/Minimap'
import './MainScreen.css'

export default function MainScreen({ gameState, dispatch }) {
  const { player, location, visited } = gameState
  const loc = MAP[location]

  return (
    <div className="screen main-screen">
      <div className="main-panel">
        <div className="main-content">
          <div className="main-left">
            <h2 className="location-name">{loc.name}</h2>
            <p className="location-desc">{loc.desc}</p>

            <div className="stat-row">
              <span className="stat-label">LV {player.level}</span>
            </div>

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

            <div className="stat-row">
              <span className="stat-text yellow">EXP: {player.exp}/{player.expToLevel}</span>
              <span className="stat-text yellow">Gold: {player.gold}</span>
            </div>

            <div className="stat-row stats-line">
              {['str', 'dex', 'int', 'con', 'luck'].map(s => (
                <span key={s} className="stat-text">{s.toUpperCase()}:{getStat(player.stats, player.equippedItems, s)}</span>
              ))}
            </div>

            {player.equipment.weapon && (
              <div className="equip-row">
                <span className="equip-text">Wpn: {player.equipment.weapon.name}</span>
              </div>
            )}
            {player.equipment.armor && (
              <div className="equip-row">
                <span className="equip-text">Arm: {player.equipment.armor.name}</span>
              </div>
            )}

            {loc.npcs.length > 0 && (
              <div className="npc-row">
                <span className="npc-text">NPCs: {loc.npcs.join(', ')}</span>
              </div>
            )}

            <div className="exits-row">
              <span className="exits-text">
                Exits: {Object.entries(loc.exits).map(([d, e]) => `${d}->${MAP[e].name}`).join(' | ')}
              </span>
            </div>
          </div>

          <div className="main-right">
            <Minimap location={location} visited={visited} />
          </div>
        </div>
      </div>

      <div className="action-bar">
        <div className="action-row">
          <Button onClick={() => dispatch({ type: 'NAVIGATE', target: 'skills_list' })}>Status</Button>
          <Button onClick={() => dispatch({ type: 'NAVIGATE', target: 'inventory' })}>Inventory</Button>
          <Button onClick={() => dispatch({ type: 'EXPLORE' })}>Explore</Button>
          <Button onClick={() => dispatch({ type: 'NAVIGATE', target: 'move' })}>Move</Button>
          <Button onClick={() => dispatch({ type: 'NAVIGATE', target: 'npc' })}>Talk</Button>
        </div>
        <div className="action-row">
          <Button onClick={() => dispatch({ type: 'NAVIGATE', target: 'skills_list' })}>Skills</Button>
          <Button onClick={() => dispatch({ type: 'NAVIGATE', target: 'item_use' })}>Use Item</Button>
          <Button onClick={() => dispatch({ type: 'NAVIGATE', target: 'equip' })}>Equip</Button>
          <Button color={location === 'village' ? '' : 'red'} onClick={() => dispatch({ type: 'REST' })}>Rest</Button>
          <Button onClick={() => window.close()}>Quit</Button>
        </div>
      </div>
    </div>
  )
}

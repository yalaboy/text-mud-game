import { canEquip } from '../logic/gameReducer'
import Button from '../components/Button'
import './EquipScreen.css'

export default function EquipScreen({ gameState, dispatch }) {
  const { player } = gameState
  const equips = player.inventory.filter(i => ['weapon', 'armor', 'accessory'].includes(i.type))

  return (
    <div className="screen list-screen">
      <div className="list-panel">
        <h2 className="list-title cyan">EQUIP</h2>
        <div className="list-scroll">
          {equips.map((item, i) => {
            const ok = canEquip(item, player.stats, player.equippedItems)
            return (
              <div key={item.uid || i} className="list-item clickable" onClick={() => dispatch({ type: 'EQUIP', item })}>
                <span className="list-item-name">{item.name} {ok ? '[OK]' : '[!]'}</span>
                <span className="list-item-desc">{item.desc}</span>
              </div>
            )
          })}
          {equips.length === 0 && <p className="list-empty">No equipment</p>}
        </div>
      </div>
      <div className="action-bar">
        <Button onClick={() => dispatch({ type: 'GO_BACK' })}>Back</Button>
      </div>
    </div>
  )
}

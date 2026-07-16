import Button from '../components/Button'
import './InventoryScreen.css'

export default function InventoryScreen({ gameState, dispatch }) {
  const { player } = gameState

  return (
    <div className="screen list-screen">
      <div className="list-panel">
        <h2 className="list-title cyan">INVENTORY</h2>
        <div className="list-subtitle">Gold: {player.gold}</div>
        <div className="list-scroll">
          {player.inventory.map((item, i) => {
            const stats = []
            if (item.attack) stats.push(`ATK+${item.attack}`)
            if (item.defense) stats.push(`DEF+${item.defense}`)
            return (
              <div key={item.uid || i} className="list-item">
                <span className="list-item-name">{item.name}{stats.length > 0 ? ` [${stats.join(',')}]` : ''}</span>
                <span className="list-item-desc">{item.desc}</span>
              </div>
            )
          })}
          {player.inventory.length === 0 && <p className="list-empty">Empty</p>}
        </div>
        <div className="list-footer">{player.inventory.length} items</div>
      </div>
      <div className="action-bar">
        <Button onClick={() => dispatch({ type: 'GO_BACK' })}>Back</Button>
      </div>
    </div>
  )
}

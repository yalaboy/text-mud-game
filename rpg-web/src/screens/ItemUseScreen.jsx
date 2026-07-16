import Button from '../components/Button'
import './ItemUseScreen.css'

export default function ItemUseScreen({ gameState, dispatch }) {
  const { player, enemy } = gameState
  const consumables = player.inventory.filter(i => i.type === 'consumable')

  return (
    <div className="screen list-screen">
      <div className="list-panel">
        <h2 className="list-title yellow">USE ITEM</h2>
        <div className="list-scroll">
          {consumables.slice(0, 6).map((item, i) => (
            <Button key={item.uid || i} color="yellow" onClick={() => dispatch({ type: 'USE_ITEM', item })}>
              {item.name}
            </Button>
          ))}
          {consumables.length === 0 && <p className="list-empty">No items</p>}
        </div>
      </div>
      <div className="action-bar">
        <Button onClick={() => dispatch({ type: 'GO_BACK' })}>Back</Button>
      </div>
    </div>
  )
}

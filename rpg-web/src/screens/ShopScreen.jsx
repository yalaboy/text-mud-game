import { SHOP_ITEMS } from '../data/gameData'
import Button from '../components/Button'
import './ShopScreen.css'

export default function ShopScreen({ gameState, dispatch }) {
  const { player } = gameState

  return (
    <div className="screen list-screen">
      <div className="list-panel">
        <h2 className="list-title yellow">SHOP</h2>
        <div className="list-subtitle">Gold: {player.gold}</div>
        <div className="list-scroll">
          {SHOP_ITEMS.map((item, i) => (
            <Button
              key={i}
              color="yellow"
              disabled={player.gold < item.value}
              onClick={() => dispatch({ type: 'BUY_ITEM', item })}
            >
              {item.name} ({item.value}g)
            </Button>
          ))}
        </div>
      </div>
      <div className="action-bar">
        <Button onClick={() => dispatch({ type: 'GO_BACK' })}>Back</Button>
      </div>
    </div>
  )
}

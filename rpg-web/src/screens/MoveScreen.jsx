import { MAP } from '../data/gameData'
import Button from '../components/Button'
import './MoveScreen.css'

export default function MoveScreen({ gameState, dispatch }) {
  const loc = MAP[gameState.location]

  return (
    <div className="screen list-screen">
      <div className="list-panel">
        <h2 className="list-title">MOVE</h2>
        <div className="list-scroll">
          {Object.entries(loc.exits).map(([dir, dest]) => (
            <Button key={dir} onClick={() => dispatch({ type: 'MOVE', direction: dir })}>
              {dir} → {MAP[dest].name}
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

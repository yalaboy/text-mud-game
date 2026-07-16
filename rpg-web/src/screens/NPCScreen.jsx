import { MAP } from '../data/gameData'
import Button from '../components/Button'
import './NPCScreen.css'

export default function NPCScreen({ gameState, dispatch }) {
  const loc = MAP[gameState.location]

  return (
    <div className="screen list-screen">
      <div className="list-panel">
        <h2 className="list-title magenta">TALK</h2>
        <div className="list-scroll">
          {loc.npcs.map(npc => (
            <Button key={npc} color="magenta" onClick={() => dispatch({ type: 'TALK', npc })}>
              {npc}
            </Button>
          ))}
          {loc.npcs.length === 0 && <p className="list-empty">No one here</p>}
        </div>
      </div>
      <div className="action-bar">
        <Button onClick={() => dispatch({ type: 'GO_BACK' })}>Back</Button>
      </div>
    </div>
  )
}

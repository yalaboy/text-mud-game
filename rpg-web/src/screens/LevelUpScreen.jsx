import Button from '../components/Button'
import './LevelUpScreen.css'

const stats = [
  { key: 'str', label: '+STR', color: 'red' },
  { key: 'dex', label: '+DEX', color: 'green' },
  { key: 'int', label: '+INT', color: 'blue' },
  { key: 'con', label: '+CON', color: 'cyan' },
  { key: 'luck', label: '+LCK', color: 'yellow' },
]

export default function LevelUpScreen({ gameState, dispatch }) {
  return (
    <div className="screen levelup-screen">
      <h1 className="title-xl">LEVEL UP!</h1>
      <p className="levelup-level">Level {gameState.player.level}</p>
      <p className="levelup-points">Points: {gameState.levelPoints}</p>
      <div className="levelup-buttons">
        {stats.map(s => (
          <Button key={s.key} color={s.color} onClick={() => dispatch({ type: 'ALLOCATE_STAT', stat: s.key })}>
            {s.label}
          </Button>
        ))}
      </div>
    </div>
  )
}

import { SKILLS } from '../data/gameData'
import { getStat, getLearnedSkills } from '../logic/gameReducer'
import Button from '../components/Button'
import './SkillsScreen.css'

export default function SkillsScreen({ gameState, dispatch }) {
  const { player } = gameState
  const learned = getLearnedSkills(player.stats)

  return (
    <div className="screen list-screen">
      <div className="list-panel">
        <h2 className="list-title magenta">SKILLS</h2>
        <div className="list-scroll">
          {SKILLS.map((sk, i) => {
            const isLearned = learned.some(s => s.name === sk.name)
            const isReady = !isLearned && Object.entries(sk.statReq).every(([s, v]) => player.stats[s] >= v)
            const color = isLearned ? 'green' : isReady ? 'yellow' : 'red'
            const status = isLearned ? 'LEARNED' : isReady ? 'READY' : 'LOCKED'
            return (
              <div key={i} className="list-item">
                <span className={`list-item-name color-${color}`}>{sk.name}</span>
                <span className="list-item-desc">{sk.desc} | MP:{sk.mpCost} | {sk.type}</span>
                <span className={`list-item-status color-${color}`}>{status}</span>
              </div>
            )
          })}
        </div>
      </div>
      <div className="action-bar">
        <Button onClick={() => dispatch({ type: 'GO_BACK' })}>Back</Button>
      </div>
    </div>
  )
}

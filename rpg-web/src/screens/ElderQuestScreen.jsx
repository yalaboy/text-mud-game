import { QUESTS } from '../data/gameData'
import { checkQuestProgress } from '../logic/gameReducer'
import Button from '../components/Button'
import './ElderQuestScreen.css'

export default function ElderQuestScreen({ gameState, dispatch }) {
  const { player, visited, killCounts, battleCount, activeQuests, questStatus } = gameState

  const available = QUESTS.filter(q =>
    q.reqLevel <= player.level && !activeQuests.includes(q.id)
  )
  const inProgress = QUESTS.filter(q => activeQuests.includes(q.id) && !(questStatus[q.id]?.claimed))
  const completed = QUESTS.filter(q => activeQuests.includes(q.id) && questStatus[q.id]?.claimed)

  return (
    <div className="screen quest-screen">
      <div className="quest-panel">
        <h2 className="quest-title">ELDER'S QUESTS</h2>
        <p className="quest-subtitle">"Brave adventurer, help our village!"</p>

        {inProgress.length > 0 && (
          <div className="quest-section">
            <h3 className="section-header">In Progress</h3>
            {inProgress.map(q => {
              const ready = questStatus[q.id]?.readyToClaim
              return (
                <div key={q.id} className="quest-card">
                  <div className="quest-info">
                    <span className="quest-name">{q.name}</span>
                    <span className="quest-desc">{q.desc}</span>
                    <span className="quest-reward">Reward: {q.reward.gold}g + {q.reward.exp}exp</span>
                  </div>
                  {ready ? (
                    <Button color="green" onClick={() => dispatch({ type: 'CLAIM_QUEST', questId: q.id })}>
                      Claim
                    </Button>
                  ) : (
                    <span className="quest-progress">Active</span>
                  )}
                </div>
              )
            })}
          </div>
        )}

        {available.length > 0 && (
          <div className="quest-section">
            <h3 className="section-header">Available</h3>
            {available.slice(0, 6).map(q => (
              <div key={q.id} className="quest-card">
                <div className="quest-info">
                  <span className="quest-name">{q.name}</span>
                  <span className="quest-desc">{q.desc}</span>
                  <span className="quest-reward">Reward: {q.reward.gold}g + {q.reward.exp}exp</span>
                </div>
                <Button color="yellow" onClick={() => dispatch({ type: 'ACCEPT_QUEST', questId: q.id })}>
                  Accept
                </Button>
              </div>
            ))}
          </div>
        )}

        {completed.length > 0 && (
          <div className="quest-section">
            <h3 className="section-header">Completed ({completed.length})</h3>
          </div>
        )}

        {available.length === 0 && inProgress.length === 0 && (
          <p className="quest-empty">No quests available right now. Come back when you're stronger!</p>
        )}
      </div>
      <div className="action-bar">
        <Button onClick={() => dispatch({ type: 'GO_BACK' })}>Back</Button>
      </div>
    </div>
  )
}

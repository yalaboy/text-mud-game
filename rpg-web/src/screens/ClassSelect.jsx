import Button from '../components/Button'
import './ClassSelect.css'

const classes = [
  { name: 'Warrior', desc: 'High STR & CON', color: 'red' },
  { name: 'Rogue', desc: 'High DEX & LCK', color: 'green' },
  { name: 'Mage', desc: 'High INT', color: 'blue' },
]

export default function ClassSelect({ dispatch }) {
  return (
    <div className="screen class-screen">
      <h2 className="title-lg">Choose Your Class</h2>
      <div className="class-buttons">
        {classes.map(c => (
          <Button key={c.name} color={c.color} onClick={() => dispatch({ type: 'SELECT_CLASS', classType: c.name })}>
            {c.name} — {c.desc}
          </Button>
        ))}
      </div>
    </div>
  )
}

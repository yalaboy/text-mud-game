import Button from '../components/Button'
import './MainMenu.css'

export default function MainMenu({ dispatch }) {
  return (
    <div className="screen menu-screen">
      <h1 className="title-xl">RPG ADVENTURE</h1>
      <p className="subtitle">A graphical RPG</p>
      <div className="menu-buttons">
        <Button onClick={() => dispatch({ type: 'START_GAME' })}>Start Game</Button>
        <Button onClick={() => window.close()}>Quit</Button>
      </div>
    </div>
  )
}

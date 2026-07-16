import { useState } from 'react'
import Button from '../components/Button'
import './NamingScreen.css'

export default function NamingScreen({ dispatch }) {
  const [name, setName] = useState('')

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && name) {
      dispatch({ type: 'SET_NAME', name })
      dispatch({ type: 'CONFIRM_NAME' })
    }
  }

  const handleConfirm = () => {
    if (name) {
      dispatch({ type: 'SET_NAME', name })
      dispatch({ type: 'CONFIRM_NAME' })
    }
  }

  return (
    <div className="screen naming-screen">
      <h2 className="title-lg">Enter Your Name</h2>
      <input
        className="name-input"
        value={name}
        onChange={(e) => setName(e.target.value.slice(0, 16))}
        onKeyDown={handleKeyDown}
        autoFocus
        placeholder="Hero"
      />
      <Button onClick={handleConfirm} disabled={!name}>Confirm</Button>
    </div>
  )
}

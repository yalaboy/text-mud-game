import './Button.css'

export default function Button({ children, onClick, color, className = '', disabled = false }) {
  return (
    <button
      className={`game-btn ${color || ''} ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}

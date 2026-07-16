import './HealthBar.css'

export default function HealthBar({ current, max, color = 'green' }) {
  const pct = max > 0 ? Math.max(0, Math.min(100, (current / max) * 100)) : 0
  return (
    <div className={`health-bar ${color}`}>
      <div className="health-bar-fill" style={{ width: `${pct}%` }} />
    </div>
  )
}

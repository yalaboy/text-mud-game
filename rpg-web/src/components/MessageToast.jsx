import './MessageToast.css'

export default function MessageToast({ message, timer }) {
  if (!message || timer <= 0) return null
  const opacity = Math.min(1, timer / 60)
  return (
    <div className="message-toast" style={{ opacity }}>
      {message}
    </div>
  )
}

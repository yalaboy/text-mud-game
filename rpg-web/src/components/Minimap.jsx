import { MAP, MAP_POSITIONS, MAP_CONNECTIONS } from '../data/gameData'
import './Minimap.css'

const SCALE = 52
const NODE_R = 8

export default function Minimap({ location, visited }) {
  return (
    <div className="minimap">
      <div className="minimap-title">MAP</div>
      <svg viewBox="0 0 280 220" className="minimap-svg">
        {MAP_CONNECTIONS.map(([a, b]) => {
          const pa = MAP_POSITIONS[a]
          const pb = MAP_POSITIONS[b]
          if (!pa || !pb || !visited.has(a) || !visited.has(b)) return null
          return (
            <line
              key={`${a}-${b}`}
              x1={25 + pa[0] * SCALE}
              y1={25 + pa[1] * SCALE}
              x2={25 + pb[0] * SCALE}
              y2={25 + pb[1] * SCALE}
              stroke="#787878"
              strokeWidth="2"
            />
          )
        })}
        {Object.entries(MAP_POSITIONS).map(([key, [gx, gy]]) => {
          if (!visited.has(key)) return null
          const cx = 25 + gx * SCALE
          const cy = 25 + gy * SCALE
          const isCurrent = key === location
          const r = isCurrent ? NODE_R + 4 : NODE_R
          const color = isCurrent ? '#dcc832' : '#32c8dc'
          return (
            <g key={key}>
              <circle cx={cx} cy={cy} r={r} fill={color} stroke="#dcdcdc" strokeWidth="1" />
              <text x={cx} y={cy + r + 14} textAnchor="middle" className="minimap-label">
                {MAP[key].name.slice(0, 6)}
              </text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}

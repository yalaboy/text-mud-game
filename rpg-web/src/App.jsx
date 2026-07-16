import { useReducer, useEffect } from 'react'
import { gameReducer } from './logic/gameReducer'
import MessageToast from './components/MessageToast'
import MainMenu from './screens/MainMenu'
import NamingScreen from './screens/NamingScreen'
import ClassSelect from './screens/ClassSelect'
import MainScreen from './screens/MainScreen'
import BattleScreen from './screens/BattleScreen'
import InventoryScreen from './screens/InventoryScreen'
import SkillsScreen from './screens/SkillsScreen'
import EquipScreen from './screens/EquipScreen'
import ItemUseScreen from './screens/ItemUseScreen'
import MoveScreen from './screens/MoveScreen'
import NPCScreen from './screens/NPCScreen'
import ShopScreen from './screens/ShopScreen'
import LevelUpScreen from './screens/LevelUpScreen'
import ElderQuestScreen from './screens/ElderQuestScreen'

const initialState = {
  state: 'menu',
  player: null,
  playerName: '',
  location: 'village',
  visited: new Set(['village']),
  enemy: null,
  message: '',
  msgTimer: 0,
  levelPoints: 5,
  scrollOffset: 0,
  questStatus: {},
  killCounts: {},
  battleCount: 0,
  activeQuests: [],
}

export default function App() {
  const [gameState, dispatch] = useReducer(gameReducer, initialState)

  useEffect(() => {
    const interval = setInterval(() => {
      dispatch({ type: 'TICK' })
    }, 1000 / 60)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const handleWheel = (e) => {
      if (gameState.state === 'inventory' || gameState.state === 'skills_list') {
        e.preventDefault()
        dispatch({ type: 'SCROLL', delta: e.deltaY > 0 ? -30 : 30 })
      }
    }
    window.addEventListener('wheel', handleWheel, { passive: false })
    return () => window.removeEventListener('wheel', handleWheel)
  }, [gameState.state])

  const renderScreen = () => {
    switch (gameState.state) {
      case 'menu': return <MainMenu dispatch={dispatch} />
      case 'naming': return <NamingScreen dispatch={dispatch} />
      case 'class_select': return <ClassSelect dispatch={dispatch} />
      case 'main': return <MainScreen gameState={gameState} dispatch={dispatch} />
      case 'battle': return <BattleScreen gameState={gameState} dispatch={dispatch} />
      case 'inventory': return <InventoryScreen gameState={gameState} dispatch={dispatch} />
      case 'skills_list': return <SkillsScreen gameState={gameState} dispatch={dispatch} />
      case 'equip': return <EquipScreen gameState={gameState} dispatch={dispatch} />
      case 'item_use': return <ItemUseScreen gameState={gameState} dispatch={dispatch} />
      case 'move': return <MoveScreen gameState={gameState} dispatch={dispatch} />
      case 'npc': return <NPCScreen gameState={gameState} dispatch={dispatch} />
      case 'npc_shop': return <ShopScreen gameState={gameState} dispatch={dispatch} />
      case 'elder_quest': return <ElderQuestScreen gameState={gameState} dispatch={dispatch} />
      case 'level_up': return <LevelUpScreen gameState={gameState} dispatch={dispatch} />
      default: return <MainMenu dispatch={dispatch} />
    }
  }

  return (
    <>
      {renderScreen()}
      <MessageToast message={gameState.message} timer={gameState.msgTimer} />
    </>
  )
}

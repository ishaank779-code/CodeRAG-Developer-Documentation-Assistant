import {Moon, Sun, UserCircle} from 'lucide-react'
import {useEffect,useState} from 'react'
import Logo from './components/Logo'
import Sidebar from './components/Sidebar'
import RightRail from './components/RightRail'
import Home from './pages/Home'
import AskQuestion from './pages/AskQuestion'
import Documentation from './pages/Documentation'
import SavedChats from './pages/SavedChats'
import Settings from './pages/Settings'
import {favoriteChat,getChat,getChats,type Chat} from './lib/api'
import './styles.css'

export default function App(){const [page,setPage]=useState('home');const [chats,setChats]=useState<Chat[]>([]);const [current,setCurrent]=useState<Chat|null>(null);const [dark,setDark]=useState(false);useEffect(()=>{getChats().then(setChats).catch(()=>{})},[]);useEffect(()=>{document.body.classList.toggle('dark',dark)},[dark]);const saved=(c:Chat)=>{setCurrent(c);setChats(prev=>[c,...prev.filter(x=>x.id!==c.id)])};const open=async(id:number)=>{const c=await getChat(id);setCurrent(c);setPage('ask')};const toggleFavorite=async()=>{if(!current)return;const c=await favoriteChat(current.id);setCurrent(c);setChats(prev=>prev.map(x=>x.id===c.id?{...x,...c}:x))};return <div className="app"><header className="topbar"><Logo/><div className="top-actions"><button onClick={()=>setDark(v=>!v)} title="Theme">{dark?<Sun size={19}/>:<Moon size={19}/>}</button><button title="Profile"><UserCircle size={22}/></button></div></header><div className="layout"><Sidebar page={page} setPage={p=>{setPage(p);if(p!=='ask')setCurrent(null)}}/><div className="center"><div className="mobile-fav">{current&&page==='ask'?<button onClick={toggleFavorite}>{current.favorite?'★ Saved':'☆ Save chat'}</button>:null}</div>{page==='home'&&<Home onAnswer={saved}/>} {page==='ask'&&<AskQuestion initial={current} onSaved={saved} onFavorite={async(id)=>{const c=await favoriteChat(id);setChats(prev=>prev.map(x=>x.id===id?{...x,...c}:x));return c}}/>} {page==='docs'&&<Documentation/>} {page==='saved'&&<SavedChats chats={chats} onOpen={open}/>} {page==='favorites'&&<SavedChats chats={chats} onOpen={open}/>} {page==='settings'&&<Settings/>}</div><RightRail chats={chats} onOpen={open}/></div></div>}

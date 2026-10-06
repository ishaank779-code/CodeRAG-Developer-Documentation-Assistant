import {BookOpen, FileText, FolderHeart, House, MessageCircleQuestion, Settings, Sparkles, Star} from 'lucide-react'
export default function Sidebar({page,setPage}:{page:string,setPage:(p:string)=>void}){
 const items=[['home','Home',House],['ask','Ask Question',MessageCircleQuestion],['docs','Documentation',BookOpen],['saved','Saved Chats',FolderHeart],['favorites','Favorites',Star],['settings','Settings',Settings]] as const
 return <aside className="sidebar"><nav>{items.map(([id,label,Icon])=><button key={id} className={page===id?'nav-item active':'nav-item'} onClick={()=>setPage(id)}><Icon size={19}/><span>{label}</span></button>)}</nav><div className="sidebar-card"><div className="mini-icon"><Sparkles size={18}/></div><strong>Better Answers.<br/>Faster Development.</strong><p>⚡ Powered by RAG</p></div></aside>
}

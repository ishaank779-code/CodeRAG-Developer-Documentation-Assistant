const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export type Source = { document_id:number; title:string; category:string; source_url:string|null; snippet:string; score:number }
export type Chat = { id:number; title:string; question:string; answer:string; favorite:boolean; created_at:string; sources:Source[] }
export type Document = { id:number; title:string; category:string; source_url:string|null; content:string; created_at:string }

async function request<T>(path:string, options:RequestInit={}) {
  const res = await fetch(`${API}${path}`, { headers:{'Content-Type':'application/json'}, ...options })
  if (!res.ok) throw new Error(await res.text())
  return res.json() as Promise<T>
}
export const askQuestion = (question:string) => request<Chat>('/chat',{method:'POST',body:JSON.stringify({question})})
export const getChats = () => request<Chat[]>('/chats')
export const getChat = (id:number) => request<Chat>(`/chats/${id}`)
export const favoriteChat = (id:number) => request<Chat>(`/chats/${id}/favorite`,{method:'POST'})
export const getDocuments = () => request<Document[]>('/documents')

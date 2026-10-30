import seed from './data/games.json'

const LOCAL_KEY = 'arcade.games.local'
const TOKEN_KEY = 'arcade.admin.token'

export const getToken = () => localStorage.getItem(TOKEN_KEY) || ''
export const setToken = (t) => (t ? localStorage.setItem(TOKEN_KEY, t) : localStorage.removeItem(TOKEN_KEY))

const sortGames = (g) => [...g].sort((a, b) => a.order - b.order)
const auth = () => ({ Authorization: `Bearer ${getToken()}` })

const readLocal = () => {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_KEY)) || seed
  } catch {
    return seed
  }
}

// When no API is reachable (plain `vite dev`), fall back to the bundled seed
// plus localStorage so the admin UI can still be exercised.
async function request(path, opts) {
  const res = await fetch(path, opts)
  const type = res.headers.get('content-type') || ''
  if (!type.includes('application/json')) throw Object.assign(new Error('API unavailable'), { offline: true })
  const data = await res.json()
  if (!res.ok) throw Object.assign(new Error(data.error || res.statusText), { status: res.status })
  return data
}

export async function fetchGames({ admin = false } = {}) {
  try {
    return sortGames(await request(admin ? '/api/games?admin=1' : '/api/games', { headers: admin ? auth() : {} }))
  } catch (e) {
    if (!e.offline && e.status) throw e
    return sortGames(admin ? readLocal() : readLocal().filter((g) => g.active))
  }
}

export async function saveGames(games) {
  try {
    return sortGames(await request('/api/games', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', ...auth() },
      body: JSON.stringify(games),
    }))
  } catch (e) {
    if (!e.offline && e.status !== 501) throw e
    localStorage.setItem(LOCAL_KEY, JSON.stringify(games))
    return sortGames(games)
  }
}

export async function uploadTile(blob, name) {
  try {
    const res = await request(`/api/upload?name=${encodeURIComponent(name)}`, {
      method: 'POST',
      headers: { 'Content-Type': blob.type, ...auth() },
      body: blob,
    })
    return res.url
  } catch (e) {
    if (!e.offline && e.status !== 501) throw e
    return new Promise((resolve) => {
      const r = new FileReader()
      r.onload = () => resolve(r.result)
      r.readAsDataURL(blob)
    })
  }
}

export async function checkToken() {
  try {
    await request('/api/games?admin=1', { headers: auth() })
    return true
  } catch (e) {
    if (e.offline) return true // local mode: no server to verify against
    if (e.status === 401) return false
    throw e
  }
}

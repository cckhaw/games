import { useCallback, useEffect, useRef, useState } from 'react'
import { checkToken, fetchGames, getToken, saveGames, setToken, uploadTile } from './api.js'
import { optimizeTile } from './optimize.js'
import { tileBackground } from './Tile.jsx'
import { CATEGORIES } from './categories.js'
import TagPicker from './TagPicker.jsx'

const blank = (order) => ({
  id: '', title: '', url: 'https://', category: '', tags: [], description: '', image: '', order, active: true,
})
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

function Login({ onDone }) {
  const [value, setValue] = useState('')
  const [err, setErr] = useState('')
  const submit = async (e) => {
    e.preventDefault()
    setToken(value)
    try {
      if (await checkToken()) return onDone()
      setToken('')
      setErr('Incorrect token.')
    } catch (x) {
      setErr(x.message)
    }
  }
  return (
    <main className="shell narrow">
      <form className="card login" onSubmit={submit}>
        <h1>Admin</h1>
        <input type="password" placeholder="Admin token" value={value} autoFocus onChange={(e) => setValue(e.target.value)} />
        {err && <p className="err">{err}</p>}
        <button className="btn primary" disabled={!value}>Sign in</button>
      </form>
    </main>
  )
}

function Editor({ game, allTags, onSave, onCancel }) {
  const [g, setG] = useState(game)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [drag, setDrag] = useState(false)
  const fileRef = useRef()
  const set = (k) => (e) => setG({ ...g, [k]: e.target.value })

  const pick = async (file) => {
    if (!file || !file.type.startsWith('image/')) return setErr('Please choose an image file.')
    setBusy(true)
    setErr('')
    try {
      const blob = await optimizeTile(file)
      const url = await uploadTile(blob, slug(g.title) || 'tile')
      setG((p) => ({ ...p, image: url }))
    } catch (x) {
      setErr(x.message)
    } finally {
      setBusy(false)
    }
  }

  const submit = (e) => {
    e.preventDefault()
    if (!/^https?:\/\//i.test(g.url)) return setErr('URL must start with http(s)://')
    onSave({
      ...g,
      id: g.id || slug(g.title) || `game-${Date.now()}`,
      order: Number(g.order) || 0,
    })
  }

  return (
    <div className="modal" onMouseDown={(e) => e.target === e.currentTarget && onCancel()}>
      <form className="card editor" onSubmit={submit}>
        <h2>{game.id ? 'Edit game' : 'Add game'}</h2>
        <label>Title<input required value={g.title} onChange={set('title')} /></label>
        <label>URL<input required type="url" value={g.url} onChange={set('url')} placeholder="https://game.khaw.cc" /></label>
        <div className="row">
          <label>Category
            <select value={g.category} onChange={set('category')}>
              <option value="">Uncategorized</option>
              {/* keep a legacy category selectable so editing never silently drops it */}
              {g.category && !CATEGORIES.includes(g.category) && <option value={g.category}>{g.category}</option>}
              {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </label>
          <label>Order<input type="number" value={g.order} onChange={set('order')} /></label>
        </div>
        <div className="field">Tags <small>pick existing or type a new one, then press Enter</small>
          <TagPicker value={g.tags} options={allTags} onChange={(tags) => setG((p) => ({ ...p, tags }))} />
        </div>
        <label>Description<textarea rows="3" maxLength="400" value={g.description} onChange={set('description')} /></label>

        <div
          className={`drop${drag ? ' over' : ''}`}
          style={g.image ? tileBackground(g) : undefined}
          onClick={() => fileRef.current.click()}
          onDragOver={(e) => { e.preventDefault(); setDrag(true) }}
          onDragLeave={() => setDrag(false)}
          onDrop={(e) => { e.preventDefault(); setDrag(false); pick(e.dataTransfer.files[0]) }}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && fileRef.current.click()}
        >
          <span>{busy ? 'Optimizing…' : g.image ? 'Replace tile image' : 'Drop tile image or click to choose'}</span>
          <input ref={fileRef} type="file" accept="image/png,image/webp,image/jpeg" hidden onChange={(e) => pick(e.target.files[0])} />
        </div>
        <small>Resized to 960×720 and converted to WebP automatically.</small>
        <label>Image path or URL <small>optional, e.g. /tiles/name.webp</small>
          <input
            value={g.image.startsWith('data:') ? '(uploaded image)' : g.image}
            readOnly={g.image.startsWith('data:')}
            onChange={set('image')}
            placeholder="/tiles/name.webp or https://…"
          />
        </label>

        <label className="check"><input type="checkbox" checked={g.active} onChange={(e) => setG({ ...g, active: e.target.checked })} /> Active</label>
        {err && <p className="err">{err}</p>}
        <div className="actions">
          <button type="button" className="btn" onClick={onCancel}>Cancel</button>
          <button className="btn primary" disabled={busy}>Save</button>
        </div>
      </form>
    </div>
  )
}

export default function Admin() {
  const [authed, setAuthed] = useState(!!getToken())
  const [games, setGames] = useState(null)
  const [editing, setEditing] = useState(null)
  const [msg, setMsg] = useState('')

  const logout = useCallback(() => { setToken(''); setAuthed(false); setGames(null) }, [])
  const fail = useCallback((e) => (e.status === 401 ? logout() : setMsg(e.message)), [logout])

  useEffect(() => {
    if (authed) fetchGames({ admin: true }).then(setGames).catch(fail)
  }, [authed, fail])

  const commit = async (next) => {
    setMsg('')
    try { setGames(await saveGames(next)) } catch (e) { fail(e) }
  }

  if (!authed) return <Login onDone={() => setAuthed(true)} />

  const onSave = async (g) => {
    const exists = games.some((x) => x.id === g.id)
    await commit(exists ? games.map((x) => (x.id === g.id ? g : x)) : [...games, g])
    setEditing(null)
  }
  const allTags = [...new Map((games || []).flatMap((g) => g.tags).map((t) => [t.toLowerCase(), t])).values()].sort((x, y) => x.localeCompare(y))
  const toggle = (g) => commit(games.map((x) => (x.id === g.id ? { ...x, active: !x.active } : x)))
  const remove = (g) => confirm(`Delete “${g.title}”?`) && commit(games.filter((x) => x.id !== g.id))

  return (
    <main className="shell">
      <header className="adminbar">
        <h1>Games</h1>
        <div>
          <a className="btn" href="/">View arcade</a>
          <button className="btn primary" onClick={() => setEditing(blank((games?.length || 0) + 1))}>+ Add game</button>
          <button className="btn" onClick={logout}>Sign out</button>
        </div>
      </header>
      {msg && <p className="err">{msg}</p>}
      {!games && <p className="notice">Loading…</p>}
      <ul className="list">
        {(games || []).map((g) => (
          <li key={g.id} className="card item">
            <div className="thumb" style={tileBackground(g)} />
            <div className="meta">
              <strong>{g.title}</strong>
              <small>{g.url}</small>
              <small>#{g.order} · {g.category || 'Uncategorized'}{g.tags.length ? ` · ${g.tags.join(', ')}` : ''}</small>
            </div>
            <button className={`switch${g.active ? ' on' : ''}`} role="switch" aria-checked={g.active} aria-label={`${g.title} active`} onClick={() => toggle(g)}>
              <span />
            </button>
            <span className="status">{g.active ? 'Active' : 'Hidden'}</span>
            <button className="btn" onClick={() => setEditing(g)}>Edit</button>
            <button className="btn danger" onClick={() => remove(g)}>Delete</button>
          </li>
        ))}
      </ul>
      {editing && <Editor game={editing} allTags={allTags} onSave={onSave} onCancel={() => setEditing(null)} />}
    </main>
  )
}

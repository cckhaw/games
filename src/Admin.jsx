import { useCallback, useEffect, useRef, useState } from 'react'
import { checkToken, fetchGames, getToken, saveGames, setToken, uploadTile } from './api.js'
import { optimizeTile } from './optimize.js'
import { tileBackground } from './Tile.jsx'
import { CATEGORIES } from './categories.js'
import TagPicker from './TagPicker.jsx'

const blank = (order) => ({
  id: '', title: '', url: 'https://', category: '', tags: [], description: '', image: '', order, active: true,
})
// Stable sort by `order`, then renumber 1..n so positions are always contiguous.
// On a tie, `firstId` (the game just edited) wins, so typing an existing position puts it ahead of that game.
const normalise = (list, firstId) =>
  list
    .map((g, i) => ({ g, i }))
    .sort((a, b) => a.g.order - b.g.order || (a.g.id === firstId ? -1 : b.g.id === firstId ? 1 : 0) || a.i - b.i)
    .map(({ g }, i) => ({ ...g, order: i + 1 }))
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
  const [saving, setSaving] = useState(false)
  const [drag, setDrag] = useState(null) // { from, over } while a row is being dragged
  const [focusKey, setFocusKey] = useState(null)

  const logout = useCallback(() => { setToken(''); setAuthed(false); setGames(null) }, [])
  const fail = useCallback((e) => (e.status === 401 ? logout() : setMsg(e.message)), [logout])

  useEffect(() => {
    if (authed) fetchGames({ admin: true }).then(setGames).catch(fail)
  }, [authed, fail])

  // Optimistic: show the change at once, roll back if saving fails. Resolves true on success.
  const commit = async (next) => {
    const prev = games
    setMsg('')
    setSaving(true)
    setGames(next)
    try {
      setGames(await saveGames(next))
      return true
    } catch (e) {
      setGames(prev)
      fail(e)
      return false
    } finally {
      setSaving(false)
    }
  }

  // Keep keyboard focus on the arrow that was just used, even though the row moved.
  useEffect(() => {
    if (!focusKey || saving) return // arrows are disabled while a save is in flight; wait for it
    const [id, dir] = focusKey.split('|')
    const row = document.querySelector(`[data-row="${CSS.escape(id)}"]`)
    const btn = row?.querySelector(`[data-move="${dir}"]:not(:disabled)`) || row?.querySelector('[data-move]:not(:disabled)')
    btn?.focus()
    setFocusKey(null)
  }, [focusKey, games, saving])

  if (!authed) return <Login onDone={() => setAuthed(true)} />

  const onSave = async (g) => {
    const exists = games.some((x) => x.id === g.id)
    const next = normalise(exists ? games.map((x) => (x.id === g.id ? g : x)) : [...games, g], g.id)
    if (await commit(next)) setEditing(null)
  }
  const allTags = [...new Map((games || []).flatMap((g) => g.tags).map((t) => [t.toLowerCase(), t])).values()].sort((x, y) => x.localeCompare(y))
  const toggle = (g) => commit(games.map((x) => (x.id === g.id ? { ...x, active: !x.active } : x)))
  const remove = (g) => confirm(`Delete “${g.title}”?`) && commit(normalise(games.filter((x) => x.id !== g.id)))
  const move = (from, to, via) => {
    if (saving || from === to || to < 0 || to >= games.length) return
    const next = [...games]
    const [item] = next.splice(from, 1)
    next.splice(to, 0, item)
    if (via) setFocusKey(`${item.id}|${via}`)
    commit(next.map((g, i) => ({ ...g, order: i + 1 })))
  }

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
      {games && games.length > 1 && (
        <p className="hint">Games appear in this order on the arcade. Drag a row, or use the arrows — changes save automatically. Hidden games keep their place.</p>
      )}
      <ul className="list">
        {(games || []).map((g, i) => (
          <li
            key={g.id}
            data-row={g.id}
            className={`card item${drag?.from === i ? ' dragging' : ''}${drag && drag.over === i && drag.from !== i ? ' dropzone' : ''}`}
            draggable={!saving}
            onDragStart={(e) => { setDrag({ from: i, over: i }); e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', g.id) }}
            onDragOver={(e) => { e.preventDefault(); setDrag((d) => (d && d.over !== i ? { ...d, over: i } : d)) }}
            onDrop={(e) => { e.preventDefault(); if (drag) move(drag.from, i); setDrag(null) }}
            onDragEnd={() => setDrag(null)}
          >
            <div className="reorder">
              <button className="iconbtn" data-move="up" disabled={saving || i === 0} aria-label={`Move ${g.title} up`} onClick={() => move(i, i - 1, 'up')}>▲</button>
              <span className="pos" aria-hidden="true">{i + 1}</span>
              <button className="iconbtn" data-move="down" disabled={saving || i === games.length - 1} aria-label={`Move ${g.title} down`} onClick={() => move(i, i + 1, 'down')}>▼</button>
            </div>
            <div className="thumb" style={tileBackground(g)} />
            <div className="meta">
              <strong>{g.title}</strong>
              <small>{g.url}</small>
              <small>{g.category || 'Uncategorized'}{g.tags.length ? ` · ${g.tags.join(', ')}` : ''}</small>
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

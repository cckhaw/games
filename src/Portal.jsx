import { useEffect, useMemo, useState } from 'react'
import { fetchGames } from './api.js'
import Tile from './Tile.jsx'

export default function Portal() {
  const [games, setGames] = useState(null)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState('All')
  const [playing, setPlaying] = useState(null)

  useEffect(() => {
    fetchGames().then(setGames).catch((e) => setError(e.message))
  }, [])

  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && setPlaying(null)
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  const categories = useMemo(
    () => ['All', ...new Set((games || []).map((g) => g.category).filter(Boolean))],
    [games],
  )
  const visible = (games || []).filter((g) => filter === 'All' || g.category === filter)

  return (
    <main className="shell">
      <header className="hero">
        <h1>Arcade</h1>
        <p>Pick a game. Press play.</p>
      </header>

      {categories.length > 2 && (
        <nav className="chips" aria-label="Categories">
          {categories.map((c) => (
            <button key={c} className={`chip${c === filter ? ' on' : ''}`} onClick={() => setFilter(c)}>
              {c}
            </button>
          ))}
        </nav>
      )}

      {error && <p className="notice">Couldn’t load games: {error}</p>}
      {!games && !error && <p className="notice">Loading…</p>}
      {games && !visible.length && <p className="notice">No games here yet.</p>}

      <section className="grid">
        {visible.map((g) => (
          <Tile key={g.id} game={g} as="button" type="button" onClick={() => setPlaying(g)} aria-label={`Play ${g.title}`} />
        ))}
      </section>

      {playing && (
        <div className="launcher" role="dialog" aria-label={playing.title}>
          <div className="topbar">
            <button className="back" onClick={() => setPlaying(null)}>‹ Arcade</button>
            <strong>{playing.title}</strong>
            <a className="ext" href={playing.url} target="_blank" rel="noreferrer">Open ↗</a>
          </div>
          <iframe
            title={playing.title}
            src={playing.url}
            allow="fullscreen; gamepad; autoplay; accelerometer; gyroscope"
            allowFullScreen
          />
        </div>
      )}
    </main>
  )
}

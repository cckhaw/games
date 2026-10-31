import { useMemo, useState } from 'react'

export const MAX_TAGS = 12
const clean = (s) => s.trim().replace(/\s+/g, ' ').toLowerCase().slice(0, 30)

// Multi-select of existing tags with the option to create new ones.
export default function TagPicker({ value, options, onChange }) {
  const [q, setQ] = useState('')
  const [open, setOpen] = useState(false)
  const [active, setActive] = useState(-1)

  const term = clean(q)
  const canon = (t) => options.find((o) => o.toLowerCase() === t.toLowerCase()) ?? t
  const has = (t) => value.some((v) => v.toLowerCase() === t.toLowerCase())
  const full = value.length >= MAX_TAGS

  const items = useMemo(() => {
    const list = options.filter((o) => !has(o) && o.toLowerCase().includes(term)).slice(0, 8).map((t) => ({ tag: t }))
    const exact = options.some((o) => o.toLowerCase() === term)
    if (term && !exact && !has(term)) list.push({ tag: term, create: true })
    return list
  }, [options, value, term])

  const add = (raw) => {
    const t = canon(clean(raw))
    if (!t || has(t) || full) return
    onChange([...value, t])
    setQ('')
    setActive(-1)
  }
  const remove = (t) => onChange(value.filter((v) => v !== t))

  const onKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault()
      if (active >= 0 && items[active]) add(items[active].tag)
      else if (term) add(term)
    } else if (e.key === 'Backspace' && !q && value.length) {
      remove(value[value.length - 1])
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      setOpen(true)
      setActive((a) => (items.length ? (a + 1) % items.length : -1))
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setActive((a) => (items.length ? (a <= 0 ? items.length - 1 : a - 1) : -1))
    } else if (e.key === 'Escape' && open) {
      e.stopPropagation()
      setOpen(false)
    }
  }

  return (
    <div className="tagpicker">
      <div className="tagbox">
        {value.map((t) => (
          <span key={t} className="tagchip">
            {t}
            <button type="button" aria-label={`Remove ${t}`} onClick={() => remove(t)}>×</button>
          </span>
        ))}
        <input
          value={q}
          disabled={full}
          placeholder={full ? `Maximum ${MAX_TAGS} tags` : value.length ? '' : 'Choose or type a tag'}
          role="combobox"
          aria-expanded={open && items.length > 0}
          aria-autocomplete="list"
          onChange={(e) => { setQ(e.target.value); setOpen(true); setActive(-1) }}
          onFocus={() => setOpen(true)}
          onBlur={() => { setOpen(false); setActive(-1) }}
          onKeyDown={onKeyDown}
        />
      </div>
      {open && !full && items.length > 0 && (
        <ul className="tagmenu" role="listbox">
          {items.map((it, i) => (
            <li key={it.tag} role="option" aria-selected={i === active}>
              <button
                type="button"
                className={i === active ? 'on' : ''}
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => add(it.tag)}
              >
                {it.create ? <>Add “{it.tag}”</> : it.tag}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

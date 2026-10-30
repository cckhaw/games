import { isAdmin, readCatalog, writeCatalog } from './_lib.js'

const str = (v, max) => String(v ?? '').trim().slice(0, max)

function sanitize(g, i) {
  const url = str(g.url, 500)
  if (!/^https?:\/\//i.test(url)) throw new Error(`Invalid URL for "${str(g.title, 80)}"`)
  return {
    id: str(g.id, 80) || `game-${Date.now()}-${i}`,
    title: str(g.title, 80) || 'Untitled',
    url,
    category: str(g.category, 40),
    tags: (Array.isArray(g.tags) ? g.tags : []).map((t) => str(t, 30)).filter(Boolean).slice(0, 12),
    description: str(g.description, 400),
    image: str(g.image, 600),
    order: Number.isFinite(+g.order) ? +g.order : i + 1,
    active: g.active !== false,
  }
}

export default async function handler(req, res) {
  try {
    if (req.method === 'GET') {
      const games = await readCatalog()
      const admin = isAdmin(req)
      if (req.query?.admin && !admin) return res.status(401).json({ error: 'Unauthorized' })
      return res.status(200).json(req.query?.admin ? games : games.filter((g) => g.active))
    }
    if (req.method === 'PUT') {
      if (!isAdmin(req)) return res.status(401).json({ error: 'Unauthorized' })
      if (!process.env.BLOB_READ_WRITE_TOKEN)
        return res.status(501).json({ error: 'Blob storage is not configured' })
      if (!Array.isArray(req.body) || req.body.length > 200)
        return res.status(400).json({ error: 'Expected an array of games' })
      const games = req.body.map(sanitize)
      await writeCatalog(games)
      return res.status(200).json(games)
    }
    res.setHeader('Allow', 'GET, PUT')
    return res.status(405).json({ error: 'Method not allowed' })
  } catch (e) {
    return res.status(400).json({ error: e.message })
  }
}

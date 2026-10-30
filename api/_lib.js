import { timingSafeEqual } from 'node:crypto'
import { list, put } from '@vercel/blob'
import seed from '../src/data/games.json' with { type: 'json' }

const CATALOG = 'catalog/games.json'

export function isAdmin(req) {
  const expected = process.env.ADMIN_TOKEN
  const given = (req.headers.authorization || '').replace(/^Bearer\s+/i, '')
  if (!expected || !given) return false
  const a = Buffer.from(given)
  const b = Buffer.from(expected)
  return a.length === b.length && timingSafeEqual(a, b)
}

export async function readCatalog() {
  if (!process.env.BLOB_READ_WRITE_TOKEN) return seed
  const { blobs } = await list({ prefix: CATALOG, limit: 1 })
  if (!blobs.length) return seed
  const res = await fetch(`${blobs[0].url}?t=${Date.now()}`, { cache: 'no-store' })
  return res.ok ? res.json() : seed
}

export function writeCatalog(games) {
  return put(CATALOG, JSON.stringify(games), {
    access: 'public',
    contentType: 'application/json',
    addRandomSuffix: false,
    allowOverwrite: true,
    cacheControlMaxAge: 0,
  })
}

export async function readBody(req) {
  if (Buffer.isBuffer(req.body)) return req.body
  const chunks = []
  for await (const c of req) chunks.push(c)
  return Buffer.concat(chunks)
}

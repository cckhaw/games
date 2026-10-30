import { put } from '@vercel/blob'
import { isAdmin, readBody } from './_lib.js'

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' })
  if (!isAdmin(req)) return res.status(401).json({ error: 'Unauthorized' })
  if (!process.env.BLOB_READ_WRITE_TOKEN)
    return res.status(501).json({ error: 'Blob storage is not configured' })
  try {
    const body = await readBody(req)
    if (!body.length || body.length > 4 * 1024 * 1024)
      return res.status(413).json({ error: 'Image missing or too large' })
    const type = req.headers['content-type'] === 'image/png' ? 'image/png' : 'image/webp'
    const slug = String(req.query?.name || 'tile').toLowerCase().replace(/[^a-z0-9-]+/g, '-').slice(0, 60)
    const blob = await put(`tiles/${slug}.${type === 'image/png' ? 'png' : 'webp'}`, body, {
      access: 'public',
      contentType: type,
      addRandomSuffix: true,
    })
    return res.status(200).json({ url: blob.url })
  } catch (e) {
    return res.status(500).json({ error: e.message })
  }
}

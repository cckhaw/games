// Keep only the newest READY production deployment; delete every other deployment.
// Env: VERCEL_TOKEN, VERCEL_PROJECT_ID, optional VERCEL_ORG_ID (team id).
const { VERCEL_TOKEN, VERCEL_PROJECT_ID, VERCEL_ORG_ID } = process.env
if (!VERCEL_TOKEN || !VERCEL_PROJECT_ID) {
  console.error('VERCEL_TOKEN and VERCEL_PROJECT_ID are required')
  process.exit(1)
}

const team = VERCEL_ORG_ID?.startsWith('team_') ? `&teamId=${VERCEL_ORG_ID}` : ''
const api = (path, init = {}) =>
  fetch(`https://api.vercel.com${path}${path.includes('?') ? '' : '?'}${team.slice(path.includes('?') ? 0 : 1)}`, {
    ...init,
    headers: { Authorization: `Bearer ${VERCEL_TOKEN}` },
  })

const all = []
let until = ''
for (;;) {
  const res = await api(`/v6/deployments?projectId=${VERCEL_PROJECT_ID}&limit=100${until}`)
  if (!res.ok) throw new Error(`List failed: ${res.status} ${await res.text()}`)
  const { deployments, pagination } = await res.json()
  all.push(...deployments)
  if (!pagination?.next) break
  until = `&until=${pagination.next}`
}

all.sort((a, b) => b.created - a.created)
const keep = all.find((d) => d.target === 'production' && d.state === 'READY')
if (!keep) {
  console.log('No READY production deployment found; nothing pruned.')
  process.exit(0)
}
console.log(`Keeping ${keep.url} (${keep.uid})`)

let failed = 0
for (const d of all) {
  if (d.uid === keep.uid || d.state === 'BUILDING' || d.state === 'QUEUED') continue
  const res = await api(`/v13/deployments/${d.uid}`, { method: 'DELETE' })
  if (res.ok) console.log(`Removed ${d.url}`)
  else {
    failed++
    console.warn(`Could not remove ${d.url}: ${res.status}`)
  }
}
process.exit(failed ? 1 : 0)

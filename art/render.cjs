const { chromium } = require('playwright'); const fs = require('fs')
;(async () => {
  const b = await chromium.launch(); const p = await b.newPage()
  for (const n of ['slipstream', 'neon', 'velopool', 'dunk-n-drop']) {
    const svg = fs.readFileSync(`art/${n}.svg`, 'utf8')
    await p.setContent(`<canvas id=c width=960 height=720></canvas>`)
    const data = await p.evaluate(async (s) => {
      const img = new Image(); img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(s)))
      await img.decode(); const c = document.getElementById('c'); c.getContext('2d').drawImage(img, 0, 0)
      return c.toDataURL('image/webp', 0.85).split(',')[1]
    }, svg)
    fs.writeFileSync(`public/tiles/${n}.webp`, Buffer.from(data, 'base64'))
  }
  await b.close()
})()

const { chromium } = require('playwright'); const fs = require('fs')
;(async () => {
  const b = await chromium.launch(); const p = await b.newPage()
  const shot = async (svgFile, size, out, omit) => {
    await p.setViewportSize({ width: size, height: size })
    await p.setContent(`<body style="margin:0;background:transparent"><img style="width:${size}px;height:${size}px;display:block" src="data:image/svg+xml;base64,${fs.readFileSync(svgFile).toString('base64')}">`)
    await p.waitForTimeout(100)
    await p.screenshot({ path: out, omitBackground: omit })
  }
  await shot('art/icon.svg', 32, 'public/favicon-32.png', true)
  await shot('art/icon.svg', 48, 'public/favicon-48.png', true)
  await shot('art/app-icon.svg', 180, 'public/apple-touch-icon.png', false)
  await shot('art/app-icon.svg', 192, 'public/icon-192.png', false)
  await shot('art/app-icon.svg', 512, 'public/icon-512.png', false)
  await p.setViewportSize({ width: 1200, height: 630 })
  await p.goto('file://' + process.cwd() + '/art/og.html')
  await p.screenshot({ path: 'public/og-image.jpg', type: 'jpeg', quality: 86 })
  await b.close()
})()

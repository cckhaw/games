// Downscale and re-encode an uploaded image to WebP (cover-cropped to the tile ratio).
const W = 960
const H = 720

export async function optimizeTile(file) {
  const bmp = await createImageBitmap(file)
  const scale = Math.max(W / bmp.width, H / bmp.height)
  const w = bmp.width * scale
  const h = bmp.height * scale
  const canvas = document.createElement('canvas')
  canvas.width = W
  canvas.height = H
  const ctx = canvas.getContext('2d')
  ctx.imageSmoothingQuality = 'high'
  ctx.drawImage(bmp, (W - w) / 2, (H - h) / 2, w, h)
  bmp.close?.()
  return new Promise((resolve, reject) =>
    canvas.toBlob((b) => (b ? resolve(b) : reject(new Error('Could not encode image'))), 'image/webp', 0.82),
  )
}

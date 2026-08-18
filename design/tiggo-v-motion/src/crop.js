// Crops the GIIAS 2026 TIGGO V photo to the card's landscape image window
// and applies a light warm grade so it sits on the red card.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const src = 'file://' + path.resolve(__dirname, 'tiggo-v-source.jpg');
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage();
  const blank = path.resolve(__dirname, '.blank.html');
  fs.writeFileSync(blank, '<!doctype html><title>blank</title>');
  await page.goto('file://' + blank);
  const dataUrl = await page.evaluate(async (src) => {
    const img = new Image();
    img.crossOrigin='anonymous'; img.src = src;
    await img.decode();
    // source is 1600x900; car body sits roughly x 240..1290, y 210..810
    const sx = 235, sy = 200, sw = 1075, sh = 614; // ~1.75:1
    const W = 1075, H = 614;
    const c = document.createElement('canvas');
    c.width = W; c.height = H;
    const ctx = c.getContext('2d');
    ctx.filter = 'saturate(1.06) contrast(1.05) brightness(1.02)';
    ctx.drawImage(img, sx, sy, sw, sh, 0, 0, W, H);
    return c.toDataURL('image/jpeg', 0.86);
  }, src);
  const b64 = dataUrl.split(',')[1];
  fs.writeFileSync(path.resolve(__dirname, 'tiggo-v-card.jpg'), Buffer.from(b64, 'base64'));
  await browser.close();
  fs.unlinkSync(blank);
  console.log('written', fs.statSync(path.resolve(__dirname, 'tiggo-v-card.jpg')).size, 'bytes');
})();

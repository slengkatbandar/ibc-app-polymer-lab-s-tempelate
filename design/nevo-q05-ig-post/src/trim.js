// Trims the transparent padding around the Nevo Q05 cutout so the car can be
// placed large in frame without being cropped at the roof or wheels.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const PAD = 6; // keeps the drop shadow's soft edge intact

(async () => {
  const blank = path.resolve(__dirname, '.blank.html');
  fs.writeFileSync(blank, '<!doctype html><title>blank</title>');
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage();
  await page.goto('file://' + blank);

  const out = await page.evaluate(async ({ src, pad }) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.src = src;
    await img.decode();
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const d = ctx.getImageData(0, 0, c.width, c.height).data;

    let minX = c.width, maxX = -1, minY = c.height, maxY = -1;
    for (let y = 0; y < c.height; y++) {
      for (let x = 0; x < c.width; x++) {
        if (d[(y * c.width + x) * 4 + 3] > 8) {
          if (x < minX) minX = x; if (x > maxX) maxX = x;
          if (y < minY) minY = y; if (y > maxY) maxY = y;
        }
      }
    }
    minX = Math.max(0, minX - pad); minY = Math.max(0, minY - pad);
    maxX = Math.min(c.width - 1, maxX + pad); maxY = Math.min(c.height - 1, maxY + pad);
    const w = maxX - minX + 1, h = maxY - minY + 1;

    const o = document.createElement('canvas');
    o.width = w; o.height = h;
    o.getContext('2d').drawImage(c, minX, minY, w, h, 0, 0, w, h);
    return { url: o.toDataURL('image/png'), w, h };
  }, { src: 'file://' + path.resolve(__dirname, 'nevo-q05-source.png'), pad: PAD });

  const file = path.resolve(__dirname, 'nevo-q05.png');
  fs.writeFileSync(file, Buffer.from(out.url.split(',')[1], 'base64'));
  fs.unlinkSync(blank);
  await browser.close();
  console.log(`nevo-q05.png: ${out.w}x${out.h}, ratio ${(out.w / out.h).toFixed(3)}, ${Math.round(fs.statSync(file).size / 1024)} KB`);
})();

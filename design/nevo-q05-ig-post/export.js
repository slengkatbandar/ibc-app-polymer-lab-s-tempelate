/**
 * Renders the looping motion deterministically and encodes it to MP4.
 *   node export.js                  -> 10s / 30fps mp4 + poster
 *   node export.js --preview 0,2.4  -> single preview frames only
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30, DUR = 10, W = 1080, H = 1350;
const OUT = path.resolve(__dirname);
const WORK = process.env.WORK_DIR || '/tmp/tiggo-frames';
// playwright's bundled ffmpeg only speaks VP8/webm, so prefer a full build when present
const FFMPEG = process.env.FFMPEG || (() => {
  try { return require('ffmpeg-static'); } catch (e) { return '/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux'; }
})();

(async () => {
  const previewArg = process.argv.indexOf('--preview');
  const preview = previewArg > -1 ? process.argv[previewArg + 1].split(',').map(Number) : null;

  const browser = await chromium.launch({ args: ['--allow-file-access-from-files', '--force-device-scale-factor=1'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(OUT, 'index.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await page.waitForTimeout(400);

  if (preview) {
    for (const t of preview) {
      await page.evaluate(t => window.__setTime(t), t);
      const f = path.join(WORK, `preview-${String(t).replace('.', '_')}.png`);
      fs.mkdirSync(WORK, { recursive: true });
      await page.screenshot({ path: f });
      console.log('preview', f);
    }
    await browser.close();
    return;
  }

  fs.rmSync(WORK, { recursive: true, force: true });
  fs.mkdirSync(WORK, { recursive: true });
  const total = FPS * DUR;
  for (let n = 0; n < total; n++) {
    const t = n / FPS;
    await page.evaluate(t => window.__setTime(t), t);
    await page.screenshot({
      path: path.join(WORK, 'f' + String(n).padStart(4, '0') + '.jpg'),
      type: 'jpeg', quality: 95,
    });
    if (n % 30 === 0) console.log('frame', n, '/', total);
  }
  await page.evaluate(() => window.__setTime(0));
  await page.screenshot({ path: path.join(OUT, 'poster.jpg'), type: 'jpeg', quality: 92 });
  await browser.close();

  execFileSync(FFMPEG, [
    '-y', '-framerate', String(FPS), '-i', path.join(WORK, 'f%04d.jpg'),
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
    '-shortest', '-c:a', 'aac', '-b:a', '96k',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    '-r', String(FPS), path.join(OUT, 'nevo-q05-post.mp4'),
  ], { stdio: 'inherit' });

  execFileSync(FFMPEG, [
    '-y', '-framerate', String(FPS), '-i', path.join(WORK, 'f%04d.jpg'),
    '-vf', 'fps=15,scale=540:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=3',
    '-loop', '0', path.join(OUT, 'nevo-q05-post.gif'),
  ], { stdio: 'inherit' });

  console.log('done');
})();

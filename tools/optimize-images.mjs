// PNG -> WebP (800/1600 px) für Screenshots. Schreibt images/manifest.json (Breite/Höhe der Originale).
// Aufruf: node tools/optimize-images.mjs
import sharp from 'sharp';
import { readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, extname } from 'node:path';

const ROOT = 'images';
const WIDTHS = [800, 1600];
const manifest = {};

function walk(dir) {
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}

for (const file of walk(ROOT).filter((f) => extname(f) === '.png')) {
  const img = sharp(file);
  const { width, height } = await img.metadata();
  const base = file.slice(0, -4);
  const widths = WIDTHS.filter((w) => w < width);
  if (!widths.length || width <= WIDTHS[0]) widths.push(width);
  else if (!widths.includes(Math.min(width, WIDTHS[1]))) widths.push(width);
  const out = [];
  for (const w of [...new Set(widths)]) {
    const dest = `${base}-${w}.webp`;
    await sharp(file).resize({ width: w, withoutEnlargement: true }).webp({ quality: 80, effort: 5 }).toFile(dest);
    out.push({ w, src: dest });
  }
  manifest[file] = { width, height, variants: out };
}
writeFileSync(join(ROOT, 'manifest.json'), JSON.stringify(manifest, null, 1));
console.log(Object.keys(manifest).length, 'Bilder verarbeitet');

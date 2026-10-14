// Baut dist/: kopiert Site-Dateien und ersetzt <div id="nav-container"></div> durch nav.html.
// Aufruf: node tools/inline-nav.mjs   (nach tailwind-Build; styles.css muss existieren)
import { readFileSync, writeFileSync, mkdirSync, cpSync, readdirSync, existsSync, rmSync } from 'node:fs';

const OUT = 'dist';
rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

const nav = readFileSync('nav.html', 'utf8');
for (const f of readdirSync('.').filter((n) => n.endsWith('.html') && n !== 'nav.html')) {
  const html = readFileSync(f, 'utf8').replace('<div id="nav-container"></div>', nav);
  writeFileSync(`${OUT}/${f}`, html);
}
for (const f of ['styles.css', 'site.js', 'lightbox.js', 'logo.png', 'og-image.png', 'robots.txt', 'sitemap.xml', 'llms.txt']) {
  if (existsSync(f)) cpSync(f, `${OUT}/${f}`);
}
for (const d of ['fonts', 'images', 'video']) {
  // PNG-Originale und Manifest bleiben im Repo, nicht im Image
  if (existsSync(d)) cpSync(d, `${OUT}/${d}`, { recursive: true, filter: (src) => !/\.png$|manifest\.json$/.test(src) });
}
console.log('dist/ gebaut');

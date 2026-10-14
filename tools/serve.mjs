// Kleiner statischer Server für dist/ (Vorschau). Aufruf: node tools/serve.mjs [port]
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const port = Number(process.argv[2] || 4173);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.webp': 'image/webp', '.woff2': 'font/woff2', '.txt': 'text/plain', '.xml': 'application/xml', '.mp4': 'video/mp4', '.svg': 'image/svg+xml', '.json': 'application/json' };
createServer(async (req, res) => {
  let p = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname)).replace(/^(\.\.[/\\])+/, '');
  if (p.endsWith('/')) p += 'index.html';
  try {
    const data = await readFile(join('dist', p));
    res.writeHead(200, { 'Content-Type': types[extname(p)] || 'application/octet-stream' });
    res.end(data);
  } catch {
    const nf = await readFile('dist/404.html').catch(() => 'Nicht gefunden');
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(nf);
  }
}).listen(port, () => console.log(`http://localhost:${port}`));

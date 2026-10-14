// Erzeugt og-image.png (1200x630) aus Logo, Headline und iPhone-Screenshot. Aufruf: npm run og
import sharp from 'sharp';

const W = 1200, H = 630;
const bg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
  <defs><radialGradient id="g" cx="25%" cy="30%" r="70%"><stop offset="0" stop-color="#e96161" stop-opacity=".28"/><stop offset="1" stop-color="#030712" stop-opacity="0"/></radialGradient></defs>
  <rect width="100%" height="100%" fill="#030712"/><rect width="100%" height="100%" fill="url(#g)"/>
  <g font-family="Helvetica, Arial, sans-serif" fill="#fff">
    <text x="130" y="95" font-size="34" font-weight="700">LuxStage</text>
    <text x="70" y="270" font-size="68" font-weight="700">Dein Einleuchtplan</text>
    <text x="70" y="350" font-size="68" font-weight="700">in der Hosentasche:</text>
    <text x="70" y="430" font-size="68" font-weight="700" fill="#e96161">antippen, leuchtet.</text>
    <text x="70" y="520" font-size="28" fill="#9ca3af">Für Beleuchtungsabteilungen am Theater · für ETC Eos</text>
  </g></svg>`);
const logo = await sharp('logo.png').resize(48, 48).toBuffer();
const phone = await sharp('images/screenshots/iOS/Okt2026/einleuchten-liste.png').resize({ height: 520 }).toBuffer();
const pm = await sharp(phone).metadata();
const mask = Buffer.from(`<svg width="${pm.width}" height="${pm.height}"><rect width="100%" height="100%" rx="36" fill="#fff"/></svg>`);
const phoneRound = await sharp(phone).composite([{ input: mask, blend: 'dest-in' }]).png().toBuffer();
await sharp(bg).composite([
  { input: logo, left: 70, top: 56 },
  { input: phoneRound, left: 820, top: 70 },
]).png().toFile('og-image.png');
console.log('og-image.png');

# LuxStage Website

Marketing-Website für [LuxStage](https://luxstage.app). Statisches HTML, Tailwind CSS 4 (CLI), kein Framework.

## Dateien

- `index.html`, `features.html`, `fuer-technische-leitung.html`, `ueber.html`, `updates.html` – Seiten
- `einleuchtplan-digital-fuehren.html`, `eos-kreisliste-importieren.html`, `aufbaudokumentation-theater.html` – Ratgeber-Entwürfe (`noindex`, nicht verlinkt, Faktencheck offen)
- `agb.html`, `avv.html`, `datenschutz.html`, `impressum.html`, `kuendigen.html`, `konto-loeschen.html`, `privacy.html` – Rechtliches
- `nav.html` – Navigation; `<div id="nav-container"></div>` wird beim Build durch sie ersetzt
- `src/input.css` – Tailwind-Quelle (Schrift, Komponenten, Druck-CSS); `styles.css` wird erzeugt
- `site.js` – Einblendungen, Plattform-Umschalter, Demo-Modal; `lightbox.js` – Bildvergrößerung
- `fonts/` – Inter (selbst gehostet); `images/` – Screenshots als PNG-Original plus WebP-Varianten
- `robots.txt`, `sitemap.xml`, `llms.txt`, `404.html`, `default.conf` (nginx), `og-image.png`
- `tools/` – `inline-nav.mjs` (Build nach `dist/`), `serve.mjs`, `optimize-images.mjs`, `render-og.mjs`, `build-updates.py` (nur Newsletter, die im Versand-Log stehen)

## Befehle

```bash
npm run dev      # bauen und Vorschau auf http://localhost:4173
npm run build    # Tailwind + dist/
npm run watch    # nur CSS beobachten
npm run images   # PNG -> WebP (800/1600 px), schreibt images/manifest.json
npm run og       # og-image.png neu rendern
python3 tools/build-updates.py   # updates.html aus versendeten Newslettern erzeugen
```

Neue Screenshots: PNG ablegen, `npm run images`, im HTML `srcset` auf die erzeugten `-800.webp`/`-1600.webp` verweisen (Breite/Höhe stehen in `images/manifest.json`).

## Platzhalter

Offene Inhalte stehen als `[PLATZHALTER: …]` in HTML-Kommentaren, die Sektionen sind `hidden`: Vertrauenszeile (Magdeburg), Vorher-nachher-Foto, Demo-Video (`video/demo.mp4`, `hidden` am Button `#demo-open` entfernen), Über-Seite (Foto, Referenz).

## Deployment

Push auf `main` baut das Docker-Image (Node baut `dist/`, nginx liefert aus).

#!/usr/bin/env python3
"""Erzeugt news.html aus den bereits versendeten Newslettern.
Quelle: ../Newsletter/JJJJ-MM-TT_Newsletter-Entwurf.md, aufgenommen nur, wenn das Datum im Versand-Log
../cockpit-daten/changes/_newsletter-versand.md steht (Format: `- JJJJ-MM-TT | Kampagne | Betreff`, gepflegt von
`luxstage.py newsletter-versendet`). Bilder: images/updates/<name>.png (Quelle) + WebP-Varianten (`npm run images`).
Aufruf: python3 tools/build-updates.py   (danach npm run build)"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = os.path.join(ROOT, '..', 'Newsletter')
LOG = os.path.join(ROOT, '..', 'cockpit-daten', 'changes', '_newsletter-versand.md')
MANIFEST = json.load(open(os.path.join(ROOT, 'images', 'manifest.json')))
MONATE = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']

def de_date(s):
    y, m, d = map(int, s.split('-'))
    return f'{d}. {MONATE[m-1]} {y}'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r'(?<!["=>])(https?://[^\s<)]+)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    return t

def image(alt, path):
    key = 'images/updates/' + os.path.basename(path)
    key = key[:-4] + '.png'
    m = MANIFEST.get(key)
    if not m:
        print('Bild fehlt im Manifest:', key, '(npm run images?)'); return ''
    v = m['variants']
    ss = ', '.join(f"{x['src']} {x['w']}w" for x in v)
    return (f'<figure class="my-6"><div class="rounded-xl border border-white/10 overflow-hidden bg-gray-900">'
            f'<img src="{v[0]["src"]}" srcset="{ss}" sizes="(min-width:768px) 720px, 100vw" width="{m["width"]}" height="{m["height"]}" '
            f'alt="{html.escape(alt)}" class="w-full h-auto lb-trigger" loading="lazy" decoding="async" /></div>'
            f'<figcaption class="mt-2 text-xs text-gray-400">{html.escape(alt)}</figcaption></figure>')

def render(md):
    # Anrede und Grußformel entfernen, Rest unverändert
    md = re.sub(r'^Liebe[^\n]*\n', '', md.strip(), flags=re.M)
    md = re.split(r'\nBis bald!', md)[0]
    out, para = [], []
    def flush():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>'); para.clear()
    for line in md.splitlines():
        s = line.strip()
        m = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', s)
        if not s: flush()
        elif m: flush(); out.append(image(m.group(1), m.group(2)))
        elif s.startswith('## '): flush(); out.append('<h3>' + inline(s[3:]) + '</h3>')
        else: para.append(s)
    flush()
    return '\n'.join(o for o in out if o)

sent = []
for l in open(LOG, encoding='utf-8'):
    m = re.match(r'-\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]*)\|\s*(.*)', l.strip())
    if m: sent.append((m.group(1), m.group(3).strip()))

items = []
for date, subject in sorted(sent, reverse=True):
    f = os.path.join(NL, f'{date}_Newsletter-Entwurf.md')
    if not os.path.exists(f): continue
    txt = open(f, encoding='utf-8').read()
    body = txt.split('\n---\n', 1)[1] if '\n---\n' in txt else txt
    items.append((date, subject, render(body)))

sys.path.insert(0, os.path.join(ROOT, 'tools'))
from pagekit import head, FOOT  # noqa

PER_PAGE = 3  # Newsletter je Seite
pages = [items[i:i + PER_PAGE] for i in range(0, len(items), PER_PAGE)] or [[]]
fname = lambda n: 'news.html' if n == 0 else f'news-{n + 1}.html'
where = {d: fname(n) for n, pg in enumerate(pages) for d, _, _ in pg}

toc = '\n'.join(f'          <li><a href="{where[d]}#nl-{d}" class="flex gap-3 hover:text-white">'
                f'<span class="font-mono text-xs text-gray-500 shrink-0 pt-0.5 w-36">{de_date(d)}</span><span>{html.escape(s)}</span></a></li>'
                for d, s, _ in items)
toc_html = ('      <details class="mt-8 rounded-xl border border-white/10 bg-gray-900/60 px-5 py-4">\n'
            f'        <summary class="cursor-pointer text-sm text-gray-300">Alle Ausgaben ({len(items)})</summary>\n'
            f'        <ul class="mt-4 space-y-2 text-sm text-gray-300">\n{toc}\n        </ul>\n      </details>') if len(pages) > 1 else ''


def pager(n):
    if len(pages) < 2:
        return ''
    link = lambda k, t: f'<a href="{fname(k)}" class="rounded-lg border border-white/10 px-4 py-2 hover:bg-white/5 hover:text-white">{t}</a>'
    nums = ' '.join((f'<span class="rounded-lg bg-white/10 px-3 py-2 text-white" aria-current="page">{k + 1}</span>' if k == n else
                     f'<a href="{fname(k)}" class="rounded-lg px-3 py-2 hover:bg-white/5 hover:text-white">{k + 1}</a>') for k in range(len(pages)))
    prev = link(n - 1, '← Neuer') if n > 0 else ''
    nxt = link(n + 1, 'Älter →') if n < len(pages) - 1 else ''
    return ('      <nav class="mt-16 flex items-center justify-between gap-4 text-sm text-gray-300" aria-label="Seiten">\n'
            f'        <div class="w-28">{prev}</div>\n        <div class="flex gap-1">{nums}</div>\n'
            f'        <div class="w-28 text-right">{nxt}</div>\n      </nav>')


import glob
for old in glob.glob(os.path.join(ROOT, 'news-*.html')):
    os.remove(old)

for n, pg in enumerate(pages):
    arts = '\n'.join(f'''      <article id="nl-{d}" class="mt-14 first:mt-10 scroll-mt-28">
        <p class="font-mono text-xs uppercase tracking-[0.18em] text-gray-400">{de_date(d)}</p>
        <h2 class="mt-2 text-2xl font-semibold text-white text-balance">{html.escape(s)}</h2>
        <div class="prose-lx">
{b}
        </div>
      </article>''' for d, s, b in pg)
    title = 'News – LuxStage' if n == 0 else f'News, Seite {n + 1} – LuxStage'
    page = head(title, 'Was sich in LuxStage zuletzt verbessert hat: die Neuigkeiten aus dem Newsletter.', fname(n)) + f'''
  <main class="pt-28 pb-20 sm:pt-36">
    <div class="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
      <p class="eyebrow">News</p>
      <h1 class="text-4xl sm:text-5xl font-semibold tracking-tight text-balance">Was neu ist in LuxStage</h1>
{toc_html}
      <div>
{arts}
      </div>
{pager(n)}
    </div>
  </main>
''' + FOOT
    open(os.path.join(ROOT, fname(n)), 'w', encoding='utf-8').write(page)

# Sitemap: Folgeseiten eintragen
sm_path = os.path.join(ROOT, 'sitemap.xml')
sm = re.sub(r'\n\s*<url><loc>https://luxstage\.app/news-\d+\.html</loc></url>', '', open(sm_path, encoding='utf-8').read())
main_url = '<url><loc>https://luxstage.app/news.html</loc></url>'
sm = sm.replace(main_url, main_url + ''.join(f'\n  <url><loc>https://luxstage.app/{fname(k)}</loc></url>' for k in range(1, len(pages))))
open(sm_path, 'w', encoding='utf-8').write(sm)
print(len(items), 'Newsletter auf', len(pages), 'Seiten:', ', '.join(d for d, _, _ in items))

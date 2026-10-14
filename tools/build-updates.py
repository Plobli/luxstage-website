#!/usr/bin/env python3
"""Erzeugt updates.html aus den bereits versendeten Newslettern.
Quelle: ../Newsletter/JJJJ-MM-TT_Newsletter-Entwurf.md, aufgenommen nur, wenn das Datum im Versand-Log
../changes/_newsletter-versand.md steht (Format: `- JJJJ-MM-TT | Kampagne | Betreff`, gepflegt von
`luxstage.py newsletter-versendet`). Bilder: images/updates/<name>.png (Quelle) + WebP-Varianten (`npm run images`).
Aufruf: python3 tools/build-updates.py   (danach npm run build)"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = os.path.join(ROOT, '..', 'Newsletter')
LOG = os.path.join(ROOT, '..', 'changes', '_newsletter-versand.md')
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

arts = '\n'.join(f'''      <article class="mt-14 first:mt-10">
        <p class="font-mono text-xs uppercase tracking-[0.18em] text-gray-400">{de_date(d)}</p>
        <h2 class="mt-2 text-2xl font-semibold text-white text-balance">{html.escape(s)}</h2>
        <div class="prose-lx">
{b}
        </div>
      </article>''' for d, s, b in items)

page = head('Updates – LuxStage', 'Was sich in LuxStage zuletzt verbessert hat: die Neuigkeiten aus dem Newsletter.', 'updates.html') + f'''
  <main class="pt-28 pb-20 sm:pt-36">
    <div class="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
      <p class="eyebrow">Updates</p>
      <h1 class="text-4xl sm:text-5xl font-semibold tracking-tight text-balance">Was neu ist in LuxStage</h1>
      <p class="mt-4 text-gray-300">Die Neuigkeiten aus unserem Newsletter, nach dem Versand hier nachzulesen.</p>
{arts}
    </div>
  </main>
''' + FOOT
open(os.path.join(ROOT, 'updates.html'), 'w', encoding='utf-8').write(page)
print(len(items), 'Newsletter:', ', '.join(d for d, _, _ in items))

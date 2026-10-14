#!/usr/bin/env python3
"""Erzeugt updates.html aus ../changes/*.md (nur Nutzertext). Aufruf: python3 tools/build-updates.py
Aufgenommen: Records mit newsletter != nein/n/a und mind. einer fertigen Plattform (server/ios/android),
ohne Titel, die mit „Website“ beginnen. Ausschluss einzelner Records: Dateiname in tools/updates-ausschluss.txt."""
import glob, html, os, re, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, '..', 'changes')
EXCL = set()
ex = os.path.join(ROOT, 'tools', 'updates-ausschluss.txt')
if os.path.exists(ex):
    EXCL = {l.strip() for l in open(ex) if l.strip() and not l.startswith('#')}

MONATE = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
def de_date(s):
    y, m, d = map(int, s.split('-'))
    return f'{d}. {MONATE[m-1]} {y}'

items = []
for f in sorted(glob.glob(os.path.join(CH, '*.md'))):
    name = os.path.basename(f)
    if name.startswith('_') or name in EXCL: continue
    txt = open(f, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', txt, re.S)
    if not m: continue
    fm = dict(l.split(':', 1) for l in m.group(1).splitlines() if ':' in l)
    fm = {k.strip(): v.strip() for k, v in fm.items()}
    if fm.get('newsletter', 'nein') in ('nein', 'n/a'): continue
    if not any(fm.get(k) == 'fertig' for k in ('server', 'ios', 'android')): continue
    titel = fm.get('titel', '')
    if titel.lower().startswith('website'): continue
    body = m.group(2).split('## Technische Notizen')[0].strip()
    if not body: continue
    items.append((fm.get('datum', ''), titel, body))
items.sort(reverse=True)

sys.path.insert(0, os.path.join(ROOT, 'tools'))
from pagekit import head, FOOT  # noqa

cards = '\n'.join(f'''      <article class="feat-card">
        <p class="font-mono text-xs uppercase tracking-[0.18em] text-gray-400">{de_date(d)}</p>
        <h2 class="mt-2 text-lg font-semibold text-white">{html.escape(t)}</h2>
        <p class="mt-2 text-sm text-gray-300">{html.escape(b.replace(chr(10), " "))}</p>
      </article>''' for d, t, b in items)

page = head('Updates – LuxStage', 'Was sich in LuxStage zuletzt verbessert hat: neue Funktionen und Änderungen in Web-App und iOS-App.', 'updates.html') + f'''
  <main class="pt-32 pb-20 sm:pt-40">
    <div class="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
      <p class="eyebrow">Updates</p>
      <h1 class="text-4xl sm:text-5xl font-semibold tracking-tight text-balance">Was neu ist in LuxStage</h1>
      <p class="mt-4 text-gray-300">Neue Funktionen und Verbesserungen, die zuletzt dazugekommen sind. Stand: {de_date(date.today().isoformat())}.</p>
      <div class="mt-10 grid gap-4">
{cards}
      </div>
    </div>
  </main>
''' + FOOT
open(os.path.join(ROOT, 'updates.html'), 'w', encoding='utf-8').write(page)
print(len(items), 'Einträge')

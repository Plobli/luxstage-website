import json
BASE='https://luxstage.app'
UMAMI='''  <script defer src="https://umami.moschu.net/script.js" data-website-id="ab4c6ea3-8423-4402-a3b3-a54149f5bb04"></script>
  <script defer src="https://umami.moschu.net/recorder.js" data-website-id="ab4c6ea3-8423-4402-a3b3-a54149f5bb04"></script>'''
def head(title, desc, path, jsonld=None, noindex=False, extra=''):
    url=f'{BASE}/{path}' if path!='index.html' else f'{BASE}/'
    ld=''
    for j in (jsonld or []):
        ld+=f'  <script type="application/ld+json">{json.dumps(j,ensure_ascii=False)}</script>\n'
    robots='  <meta name="robots" content="noindex" />\n' if noindex else ''
    return f'''<!doctype html>
<html lang="de" class="scroll-smooth no-js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
{robots}  <link rel="canonical" href="{url}" />
  <link rel="icon" href="logo.png" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="LuxStage" />
  <meta property="og:locale" content="de_DE" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{BASE}/og-image.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{BASE}/og-image.png" />
  <link rel="preload" href="fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="styles.css" />
{ld}{extra}{UMAMI}
  <script defer src="site.js"></script>
  <script defer src="lightbox.js"></script>
</head>
<body class="bg-gray-950 text-white font-sans antialiased">

  <div id="nav-container"></div>
'''
FOOT='''
  <!-- FOOTER -->
  <footer class="border-t border-white/5 py-12">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <div class="flex flex-col gap-8 md:flex-row md:justify-between">
        <div class="max-w-sm">
          <div class="flex items-center gap-2.5 text-sm text-gray-300 font-medium">
            <img src="logo.png" alt="" width="24" height="24" class="size-6 rounded-md" />
            LuxStage
          </div>
          <p class="mt-3 text-sm text-gray-400">Der digitale Einleuchtplan für Beleuchtungsabteilungen am Theater.</p>
          <p class="mt-3 text-xs text-gray-500">Version __APP_VERSION__</p>
        </div>
        <div class="grid grid-cols-2 gap-x-12 gap-y-2 text-sm text-gray-400 sm:grid-cols-3">
          <a href="features.html" class="hover:text-white">Funktionen</a>
          <a href="fuer-technische-leitung.html" class="hover:text-white">Für die Technische Leitung</a>
          <a href="updates.html" class="hover:text-white">Updates</a>
          <a href="ueber.html" class="hover:text-white">Über LuxStage</a>
          <a href="https://docs.luxstage.app" class="hover:text-white">Dokumentation</a>
          <a href="https://discord.gg/H8ZMSXyJC" target="_blank" rel="noopener" class="hover:text-white">Discord</a>
          <a href="index.html#kontakt" class="hover:text-white">Kontakt</a>
          <a href="impressum.html" class="hover:text-white">Impressum</a>
          <a href="datenschutz.html" class="hover:text-white">Datenschutz</a>
          <a href="agb.html" class="hover:text-white">AGB</a>
          <a href="avv.html" class="hover:text-white">AVV</a>
          <a href="kuendigen.html" class="hover:text-white">Verträge kündigen</a>
          <a href="konto-loeschen.html" class="hover:text-white">Konto löschen</a>
        </div>
      </div>
      <p class="mt-10 text-xs text-gray-500">ETC und Eos sind Marken von Electronic Theatre Controls, Inc. LuxStage steht in keiner Verbindung zu ETC.</p>
    </div>
  </footer>
</body>
</html>
'''

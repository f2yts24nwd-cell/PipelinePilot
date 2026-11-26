import re, json
src='../canvas/'
def parts(fn):
    s=open(src+fn).read()
    xdc=s[s.index('<x-dc>')+6:s.index('</x-dc>')]
    hel=xdc[xdc.index('<helmet>')+8:xdc.index('</helmet>')]
    body=xdc[xdc.index('</helmet>')+9:].strip()
    style=re.search(r'<style>([\s\S]*?)</style>',hel).group(1)
    style=re.sub(r'body\{[^}]*\}','',style)
    code=re.search(r'<script type="text/x-dc"[^>]*>([\s\S]*?)</script>',s).group(1)
    return body,style,code
ab,ast,acode=parts('C_App.dc.html')
lb,lst,lcode=parts('Leitstand_C.dc.html')
old='width:390px;height:844px;box-sizing:border-box;'
assert old in ab
ab=ab.replace(old,'width:100%;max-width:520px;margin:0 auto;height:calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom));box-sizing:border-box;')
lb=lb.replace('min-height:100vh;','min-height:100dvh;')
runtime=open('runtime.js').read()
html=f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Pipeline Pilot</title>
<meta name="theme-color" content="#52ae32">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Pipeline">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-180.png">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<style>
/* VOICE: selbstbewusst, verspielt, Werkstatt statt Büro
   IDEA: Kartenstapel wie ein Stapel Auftragskarten am Band
   PICTURE: der Stapel selbst
   COLOUR and TYPE: itmX-Grün #52ae32, Navy #272d3a, Hellgrün #cde7c4 · Outfit
   LAYOUT: App als Handy-Spalte, Leitstand als Seite, Umschalter oben */
*{{box-sizing:border-box}}
html,body{{margin:0;-webkit-tap-highlight-color:transparent}}
body{{font-family:'Outfit',system-ui,sans-serif;background:#52ae32;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom);overscroll-behavior:none}}
body.view-hos{{background:#52ae32}}
.view[hidden]{{display:none}}
#view-hos{{background:#eef3ea;min-height:100dvh}}
@media (prefers-reduced-motion: reduce){{*{{animation-duration:.01ms !important;transition-duration:.01ms !important}}}}
{ast}
{lst}
</style>
</head>
<body>
<div id="view-app" class="view"></div>
<div id="view-hos" class="view" hidden></div>
<template id="tpl-app">{ab}</template>
<template id="tpl-hos">{lb}</template>
<script>
{{
{runtime}
var AppComp = (function () {{
{acode}
return Component; }})();
var HosComp = (function () {{
{lcode}
return Component; }})();
var tplA = document.getElementById('tpl-app').content.firstElementChild;
var tplH = document.getElementById('tpl-hos').content.firstElementChild;
DC.mount(AppComp, tplA, document.getElementById('view-app'));
DC.mount(HosComp, tplH, document.getElementById('view-hos'));
function show(v) {{
  var hos = v === 'head-of-sales';
  document.getElementById('view-app').hidden = hos;
  document.getElementById('view-hos').hidden = !hos;
  document.body.classList.toggle('view-hos', hos);
  try {{ window.scrollTo(0, 0); }} catch (e) {{}}
}}
function route() {{ show(location.hash === '#head-of-sales' ? 'head-of-sales' : 'aussendienst'); }}
document.addEventListener('click', function (e) {{
  var a = e.target.closest && e.target.closest('a[href$=".dc.html"]');
  if (!a) return;
  e.preventDefault();
  var to = /Leitstand/.test(a.getAttribute('href')) ? 'head-of-sales' : 'aussendienst';
  try {{ location.hash = to; }} catch (x) {{}}
  show(to);
}});
window.addEventListener('hashchange', route);
route();
if ('serviceWorker' in navigator && /^https?:$/.test(location.protocol)) {{
  try {{ navigator.serviceWorker.register('sw.js').catch(function () {{}}); }} catch (e) {{}}
}}
}}
</script>
</body>
</html>
'''
import os
os.makedirs('../../',exist_ok=True)
open('../../index.html','w').write(html)
man={"name":"Pipeline Pilot","short_name":"Pipeline","description":"Vertriebs-App für Außendienst und Head of Sales","start_url":"./index.html#aussendienst","scope":"./","display":"standalone","orientation":"portrait","background_color":"#52ae32","theme_color":"#52ae32","lang":"de",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}
open('../../manifest.webmanifest','w').write(json.dumps(man,ensure_ascii=False,indent=2))
open('../../sw.js','w').write('''const CACHE = 'pipeline-pilot-v1';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-180.png'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.match(e.request).then((hit) => hit || fetch(e.request).then((res) => {
    const url = new URL(e.request.url);
    if (res.ok && (url.origin === location.origin || /fonts\\.(googleapis|gstatic)\\.com$/.test(url.hostname))) {
      const copy = res.clone(); caches.open(CACHE).then((c) => c.put(e.request, copy));
    }
    return res;
  }).catch(() => caches.match('./index.html'))));
});
''')
print(len(html))

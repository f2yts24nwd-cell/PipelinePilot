# Pipeline Pilot

Klickbarer Prototyp einer Vertriebs-App für den Maschinen- und Anlagenbau: Außendienst-App (Kartenstapel, Sprach-Erfassung, Anrufliste) und Leitstand für den Head of Sales, umschaltbar in einer Web-App.

## Auf dem iPhone installieren

1. Die App-Adresse (GitHub Pages, siehe unten) in **Safari** öffnen.
2. Teilen-Symbol → **Zum Home-Bildschirm** → **Hinzufügen**.
3. Das grüne Icon „Pipeline“ startet die App bildschirmfüllend, auch offline.

## GitHub Pages einschalten (einmalig)

Repository → **Settings** → **Pages** → *Build and deployment*: Source **Deploy from a branch**, Branch **main**, Ordner **/ (root)** → **Save**.
Nach ein bis zwei Minuten läuft die App unter `https://f2yts24nwd-cell.github.io/pipelinepilot/`.

## Aufbau

| Datei / Ordner | Inhalt |
|---|---|
| `index.html` | Die komplette App (Außendienst + Head of Sales) |
| `manifest.webmanifest`, `icon-*.png` | App-Name, Icons, Vollbild-Start |
| `sw.js` | Offline-Cache |
| `quelle/canvas/` | Quell-Vorlagen der beiden Ansichten |
| `quelle/build/` | Mini-Laufzeit und Build-Skript, das `index.html` erzeugt |

## Neu bauen

```bash
cd quelle/build
python3 build.py
```

Danach in `sw.js` den Cache-Namen hochzählen (z. B. `pipeline-pilot-v10`), damit installierte Apps die neue Version laden.

Alle Kunden, Zahlen und Personen sind erfunden. Die Daten bleiben lokal auf dem jeweiligen Gerät.

# Pipeline Pilot

Klickbarer Prototyp einer Vertriebs-App für den Maschinen- und Anlagenbau: Außendienst-App (Kartenstapel, Sprach-Erfassung, Anrufliste) und Leitstand für den Head of Sales, umschaltbar in einer Web-App.

## Audio-Briefing

Oben rechts auf „Heute“ sitzt der Knopf **Briefing**. Er bietet zwei Varianten zum Vorlesen:

- **Nächster Termin**: das Rüstblatt zum Hören (Termin, Lage und Angebot, Personen, Maschinen, die drei wichtigsten Punkte).
- **Ganzer Tag**: alle offenen Stationen des Tages kurz hintereinander, dazu Wochenziel und Anrufliste.

Jedes Rüstblatt hat zusätzlich einen Knopf **Vorlesen**. Die Sprachausgabe läuft über die eingebaute Stimme des Geräts, also offline und ohne Zusatzdienst. Der Ton kommt aus dem Lautsprecher oder über Bluetooth im Auto. Die Vor- und Zurück-Tasten springen von Station zu Station, und ein Antippen eines Satzes springt direkt dorthin. Solange das Briefing läuft, bleibt der Bildschirm an. Hat ein Gerät keine Sprachausgabe, läuft der Text trotzdem mit.

**Stimme:** Im Player öffnet **Stimme** eine Auswahl aller deutschen Stimmen mit Hörprobe. Die App merkt sich die Wahl und nimmt sonst automatisch die beste vorhandene Stimme (Premium vor Erweitert vor Standard). Hinweis: iOS gibt Web-Apps nur die einfachen Stimmen frei; Premium-Stimmen sind dort nicht nutzbar.

## Auf dem iPhone installieren

1. Die App-Adresse (GitHub Pages, siehe unten) in **Safari** öffnen.
2. Teilen-Symbol → **Zum Home-Bildschirm** → **Hinzufügen**.
3. Das grüne Icon „Pipeline“ startet die App bildschirmfüllend, auch offline.

## GitHub Pages einschalten (einmalig)

Repository → **Settings** → **Pages** → *Build and deployment*: Source **Deploy from a branch**, Branch **main**, Ordner **/ (root)** → **Save**.
Nach ein bis zwei Minuten läuft die App unter `https://f2yts24nwd-cell.github.io/PipelinePilot/`.

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

Danach in `build.py` den Cache-Namen hochzählen (aktuell `pipeline-pilot-v6`, dazu `PP_VERSION`) und neu bauen, damit installierte Apps die neue Version laden.

Alle Kunden, Zahlen und Personen sind erfunden. Die Daten bleiben lokal auf dem jeweiligen Gerät.

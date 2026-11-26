# Pipeline Pilot

Klickbarer Prototyp einer Vertriebs-App für den Maschinen- und Anlagenbau: Außendienst-App (Kartenstapel, Sprach-Erfassung, Anrufliste) und Leitstand für den Head of Sales, umschaltbar in einer Web-App.

## Audio-Briefing

Oben rechts auf „Heute“ sitzt der Knopf **Briefing**. Er bietet zwei Varianten zum Vorlesen:

- **Nächster Termin**: das Rüstblatt zum Hören (Termin, Lage und Angebot, Personen, Maschinen, die drei wichtigsten Punkte).
- **Ganzer Tag**: alle offenen Stationen des Tages kurz hintereinander, dazu Wochenziel und Anrufliste.

Jedes Rüstblatt hat zusätzlich einen Knopf **Vorlesen**. Die Sprachausgabe läuft über die eingebaute Stimme des Geräts, also offline und ohne Zusatzdienst. Der Ton kommt aus dem Lautsprecher oder über Bluetooth im Auto. Die Vor- und Zurück-Tasten springen von Station zu Station, und ein Antippen eines Satzes springt direkt dorthin. Solange das Briefing läuft, bleibt der Bildschirm an. Hat ein Gerät keine Sprachausgabe, läuft der Text trotzdem mit.

**Stimme:** Die App nimmt automatisch die deutsche Stimme des Geräts. Auf dem iPhone ist das die einfache Standard-Stimme, weil iOS Web-Apps keine Premium-Stimmen freigibt.

## Route, Lücken, Nachfassen

- **Route** (Umschalter neben den Tagen): Die Tagesroute erscheint als eigener Liniennetzplan, nicht als Straßenkarte. Der Puffer zwischen den Terminen ist farbig markiert: grün = Zeit reicht, gelb = knapp, rot = nicht zu schaffen, dazu ein Knopf zum Verschieben. Die Größe der Ringe zeigt das Potenzial. Kunden **am Weg** (A-Kunden ohne Besuch, alte Anlagen, Anrufliste) lassen sich mit einem Tipp und freier Uhrzeit einplanen. Mit dem Zeitregler fährt man den Tag ab. **Losfahren** übergibt die Adresse an Apple Karten oder Google Maps.
- **Lücken** ab 60 Minuten erscheinen als eigene Karte im Stapel, zusammen mit Kunden in der Nähe.
- **Bevor du reingehst**: Reklamationen, letzter Service-Besuch, offene Rechnungen, Lieferverzug und eigene Zusagen stehen oben im Rüstblatt und im Briefing.
- **Nach dem Termin**: Nach dem Erzählen folgt ein Mail-Entwurf an den Kunden. Aufgaben mit Fälligkeit landen am richtigen Tag im Stapel. Stille Angebote erscheinen als Nachfass-Karte.

Fahrzeiten sind im Prototyp aus der Luftlinie geschätzt.

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

Danach in `build.py` den Cache-Namen hochzählen (aktuell `pipeline-pilot-v8`, dazu `PP_VERSION`) und neu bauen, damit installierte Apps die neue Version laden.

Alle Kunden, Zahlen und Personen sind erfunden. Die Daten bleiben lokal auf dem jeweiligen Gerät.

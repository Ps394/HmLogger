# HmLogger

Ein leichtgewichtiges Logging-Modul fuer Python mit:

- farbiger Konsolen-Ausgabe
- optionalem Rotating-File-Logging
- optionalem asynchronen Logging ueber QueueHandler und QueueListener

## Voraussetzungen

- Python 3.11 oder neuer

Hinweis: Das Projekt verwendet typing.Self und Union-Typen mit |.

## Installation

**Von PyPI (empfohlen):**

```bash
pip install hmlogger
```

**Lokal aus dem Repository:**

```bash
pip install -e .
```

**Mit Test-Abhaengigkeiten:**

```bash
pip install -e .[test]
```

Nach der Installation:

```python
from HmLogger import setup_logging, get_logger
import logging

setup_logging(level=logging.INFO)
log = get_logger(__name__)
log.info("Hello World")
```

## Schnellstart

```python
import logging
from HmLogger import setup_logging, get_logger

setup_logging(
    level=logging.DEBUG,
    use_colors=True,
    file_logging=True,
    async_logging=True,
)

log = get_logger("App")
log.debug("Debug-Nachricht")
log.info("Info-Nachricht")
log.warning("Warnung")
log.error("Fehler")
log.critical("Kritischer Fehler")
```

## API

### setup_logging(...)

```python
setup_logging(
    level=logging.INFO,
    use_colors=True,
    file_logging=True,
    async_logging=True,
    log_folder="./logs",
    log_file="app.log",
    mb=5,
    backup_count=5,
)
```

Parameter:

- level: Log-Level (z. B. logging.DEBUG)
- use_colors: ANSI-Farben fuer Konsole aktivieren
- file_logging: Log-Ausgabe in Datei aktivieren
- async_logging: Queue-basiertes, nicht blockierendes Logging
- log_folder: Zielordner fuer Log-Dateien
- log_file: Dateiname der Haupt-Logdatei
- mb: maximale Dateigroesse in MB vor Rotation
- backup_count: Anzahl aufbewahrter Rotationsdateien

### get_logger(name)

```python
from HmLogger import get_logger

log = get_logger("MyService")
log.info("Service gestartet")
```

## Farben und Styles

```python
from HmLogger import Color, Text

print(Color("green")("Erfolg"))
print(Color("red").bold()("Fehler"))
print(Color("yellow").underline()("Achtung"))
print(Text("Custom Text", Color("magenta").italic()))
```

Verfuegbare Farben:

- default
- grey
- red
- green
- yellow
- blue
- magenta
- cyan
- white

Verfuegbare Styles:

- bold()
- dim()
- italic()
- underline()
- blink()
- reversed()
- strikethrough()
- intense()


## Hinweise

- Bei aktivem async_logging wird ein QueueListener verwendet und per atexit sauber beendet.
- Bei file_logging=True werden Dateien rotiert, sobald die konfigurierte Groesse erreicht ist.

## Tests

Tests liegen im Ordner `tests/`.

```bash
python -m pytest
```

Die Test-Abhaengigkeiten sind als optionales Extra `test` in `pyproject.toml` hinterlegt.

## CI

Ein GitHub-Actions-Workflow unter `.github/workflows/ci.yml` fuehrt die Tests bei Push und Pull Requests nach `main` auf Python 3.11 bis 3.13 aus.

## Lizenz

Dieses Projekt steht unter der MIT License.

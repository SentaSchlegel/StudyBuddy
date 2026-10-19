# 🎓 StudyBuddy

StudyBuddy ist eine in Python entwickelte Anwendung zur Verwaltung und Planung eines Studiums. Sie unterstützt Studierende dabei, ihre Module, Prüfungsleistungen und Bachelorarbeit zu organisieren und ihren Studienfortschritt zu verfolgen.

## Funktionen

- Verwaltung von Einzelmodulen und hierarchisch aufgebauten Übermodulen
- Erfassung und Bearbeitung von Prüfungsleistungen, Noten und Prüfungsterminen
- Berechnung des aktuellen und des für das Notenziel benötigten Notendurchschnitts
- Dashboard mit Studienfortschritt, Statusverteilung und anstehenden Prüfungen
- Verwaltung der Bachelorarbeit einschließlich Terminen, Status, Note und Abgabefrist
- Dauerhafte Speicherung der Studiendaten in einer SQLite-Datenbank

## Verwendete Technologien

- Python 3.13
- Streamlit für die Benutzeroberfläche
- SQLite für die Datenhaltung
- Pytest für automatisierte Tests

## Installation und Start

Voraussetzung ist eine installierte Python-Version.

1. Das GitHub-Repository herunterladen oder klonen.
2. Ein Terminal im Hauptverzeichnis des Projekts öffnen.
3. Die benötigten Pakete installieren:

```bash
python -m pip install -r requirements.txt
```

4. Die Anwendung starten:

```bash
python -m streamlit run app.py
```

Anschließend öffnet sich StudyBuddy im Webbrowser. Beim ersten Start kann ein neues Studium eingerichtet werden.

## Tests

Die automatisierten Tests können im Hauptverzeichnis mit folgendem Befehl ausgeführt werden:

```bash
python -m pytest -q
```

## Projektstruktur

- `app.py` – Startpunkt und Navigation der Anwendung
- `studybuddy/modelle.py` – Objektorientiertes Datenmodell und Berechnungen
- `studybuddy/enums.py` – Aufzählungstypen für Prüfungen, Status und Module
- `studybuddy/repository.py` – Speicherung und Laden der Studiendaten
- `studybuddy/view.py` – Benutzeroberfläche
- `tests/` – Automatisierte Tests

## Projektkontext

StudyBuddy wurde im Rahmen eines Hochschulprojekts zur objektorientierten Programmierung entwickelt. Im Mittelpunkt stehen die Umsetzung eines objektorientierten Datenmodells, die Persistenz von Daten und die Erstellung eines funktionsfähigen Python-Prototyps.
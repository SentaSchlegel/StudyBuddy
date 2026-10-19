import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
verbindung = sqlite3.connect("studybuddy.db")
cursor = verbindung.cursor()

# Tabelle erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS pruefungsleistung (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modulname TEXT NOT NULL,
    pruefungsart TEXT NOT NULL,
    status TEXT NOT NULL,
    note REAL
)
""")

# Testdatensatz einfügen
cursor.execute("""
INSERT INTO pruefungsleistung (modulname, pruefungsart, status, note)
VALUES (?, ?, ?, ?)
""", ("Objektorientierte Programmierung", "Portfolio", "In Bearbeitung", None))

verbindung.commit()

# Gespeicherte Daten auslesen
cursor.execute("SELECT * FROM pruefungsleistung")
daten = cursor.fetchall()

print("Gespeicherte Prüfungsleistungen:")
for eintrag in daten:
    print(eintrag)

# Status der Prüfungsleistung ändern
cursor.execute("""
UPDATE pruefungsleistung
SET status = ?
WHERE id = ?
""", ("Eingereicht", 1))

verbindung.commit()

# Geänderten Datensatz erneut auslesen
cursor.execute("SELECT * FROM pruefungsleistung WHERE id = 1")
aktualisierter_eintrag = cursor.fetchone()

print("\nNach der Statusänderung:")
print(aktualisierter_eintrag)

verbindung.close()
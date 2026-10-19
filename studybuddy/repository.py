
import sqlite3
from pathlib import Path
from contextlib import closing
from datetime import date
from decimal import Decimal
from studybuddy.modelle import Studium
from studybuddy.modelle import Studium, Einzelmodul, Uebermodul
from studybuddy.enums import Modulart
from studybuddy.modelle import Bachelorarbeit
from studybuddy.enums import BachelorarbeitsStatus

from studybuddy.modelle import Pruefungsleistung
from studybuddy.enums import (
    Pruefungsart,
    Bewertungsart,
    Status,
    Pruefungsergebnis,
)

class DatenbankRepository:
    """Verwaltet die dauerhafte Speicherung der Studiendaten in SQLite."""

    def __init__(self, db_pfad: str = "studybuddy.db"):
        if not isinstance(db_pfad, str) or not db_pfad.strip():
            raise ValueError("Der Datenbankpfad darf nicht leer sein.")

        self._dbPfad = db_pfad

    def initialisiereDatenbank(self) -> None:
        """Erstellt die benötigten Tabellen, falls sie noch nicht existieren."""

        with closing(sqlite3.connect(self._dbPfad)) as verbindung:
            verbindung.execute("PRAGMA foreign_keys = ON")

            verbindung.execute("""
                CREATE TABLE IF NOT EXISTS studium (
                    id INTEGER PRIMARY KEY,
                    studiengang TEXT NOT NULL,
                    ziel_abschlussdatum TEXT NOT NULL,
                    pruefungs_meilenstein TEXT NOT NULL,
                    notenziel TEXT NOT NULL
                )
            """)

            verbindung.execute("""
                CREATE TABLE IF NOT EXISTS module (
                    id INTEGER PRIMARY KEY,
                    studium_id INTEGER NOT NULL,
                    elternmodul_id INTEGER,
                    modulname TEXT NOT NULL,
                    modultyp TEXT NOT NULL
                        CHECK (modultyp IN ('EINZEL', 'UEBER')),
                    modulart TEXT,
                    ects INTEGER,
                    FOREIGN KEY (studium_id)
                        REFERENCES studium(id),
                    FOREIGN KEY (elternmodul_id)
                        REFERENCES module(id)
                )
            """)

            verbindung.execute("""
                CREATE TABLE IF NOT EXISTS pruefungsleistungen (
                    id INTEGER PRIMARY KEY,
                    modul_id INTEGER NOT NULL UNIQUE,
                    pruefungsart TEXT NOT NULL,
                    bewertungsart TEXT NOT NULL,
                    status TEXT NOT NULL,
                    geplantes_pruefungsdatum TEXT,
                    note TEXT,
                    ergebnis TEXT,
                    FOREIGN KEY (modul_id)
                        REFERENCES module(id)
                )
            """)

            verbindung.execute("""
                CREATE TABLE IF NOT EXISTS bachelorarbeiten (
                    id INTEGER PRIMARY KEY,
                    studium_id INTEGER NOT NULL UNIQUE,
                    status TEXT NOT NULL,
                    anmeldedatum TEXT,
                    fristablaufdatum TEXT,
                    startdatum TEXT,
                    abgabedatum TEXT,
                    ects INTEGER NOT NULL,
                    note TEXT,
                    FOREIGN KEY (studium_id)
                        REFERENCES studium(id)
                )
            """)

    def speichereStudium(self, studium: Studium) -> None:
        """Speichert die grundlegenden Daten eines Studiums."""

        if not isinstance(studium, Studium):
            raise ValueError("Es muss ein gültiges Studium übergeben werden.")

        self.initialisiereDatenbank()

        with closing(sqlite3.connect(self._dbPfad)) as verbindung:
            try:
                verbindung.execute("BEGIN")

                verbindung.execute(
                    """
                    INSERT INTO studium (
                        id,
                        studiengang,
                        ziel_abschlussdatum,
                        pruefungs_meilenstein,
                        notenziel
                    )
                    VALUES (1, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        studiengang = excluded.studiengang,
                        ziel_abschlussdatum = excluded.ziel_abschlussdatum,
                        pruefungs_meilenstein = excluded.pruefungs_meilenstein,
                        notenziel = excluded.notenziel
                    """,
                    (
                        studium._studiengang,
                        studium._zielAbschlussdatum.isoformat(),
                        studium._pruefungsMeilenstein.isoformat(),
                        str(studium._notenziel),
                    ),
                )

                # Vorhandene Modulstruktur ersetzen
                verbindung.execute(
                    "DELETE FROM pruefungsleistungen"
                )
                verbindung.execute(
                    "DELETE FROM module"
                )

                def speichere_modul(modul, elternmodul_id=None):
                    """Speichert ein Modul und seine Unterstruktur."""

                    if isinstance(modul, Einzelmodul):
                        cursor = verbindung.execute(
                            """
                            INSERT INTO module (
                                studium_id,
                                elternmodul_id,
                                modulname,
                                modultyp,
                                modulart,
                                ects
                            )
                            VALUES (1, ?, ?, 'EINZEL', ?, ?)
                            """,
                            (
                                elternmodul_id,
                                modul.modulname,
                                modul._modulart.name,
                                modul.getEcts(),
                            ),
                        )

                        modul_id = cursor.lastrowid
                        pruefung = modul._pruefungsleistung

                        if pruefung is not None:
                            verbindung.execute(
                                """
                                INSERT INTO pruefungsleistungen (
                                    modul_id,
                                    pruefungsart,
                                    bewertungsart,
                                    status,
                                    geplantes_pruefungsdatum,
                                    note,
                                    ergebnis
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """,
                                (
                                    modul_id,
                                    pruefung._pruefungsart.name,
                                    pruefung.bewertungsart.name,
                                    pruefung._status.name,
                                    (
                                        pruefung._geplantes_pruefungsdatum.isoformat()
                                        if pruefung._geplantes_pruefungsdatum
                                        else None
                                    ),
                                    (
                                        str(pruefung.note)
                                        if pruefung.note is not None
                                        else None
                                    ),
                                    (
                                        pruefung.ergebnis.name
                                        if pruefung.ergebnis is not None
                                        else None
                                    ),
                                ),
                            )

                    elif isinstance(modul, Uebermodul):
                        cursor = verbindung.execute(
                            """
                            INSERT INTO module (
                                studium_id,
                                elternmodul_id,
                                modulname,
                                modultyp
                            )
                            VALUES (1, ?, ?, 'UEBER')
                            """,
                            (
                                elternmodul_id,
                                modul.modulname,
                            ),
                        )

                        modul_id = cursor.lastrowid

                        for untermodul in modul._untermodule:
                            speichere_modul(
                                untermodul,
                                modul_id,
                            )

                    else:
                        raise ValueError("Unbekannter Modultyp.")

                for modul in studium._topLevelModule:
                    speichere_modul(modul)

                # Vorhandene Bachelorarbeit ersetzen
                verbindung.execute(
                    "DELETE FROM bachelorarbeiten WHERE studium_id = 1"
                )

                bachelorarbeit = studium._bachelorarbeit

                if bachelorarbeit is not None:
                    verbindung.execute(
                        """
                        INSERT INTO bachelorarbeiten (
                            studium_id,
                            status,
                            anmeldedatum,
                            fristablaufdatum,
                            startdatum,
                            abgabedatum,
                            ects,
                            note
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            1,
                            bachelorarbeit._status.name,
                            (
                                bachelorarbeit._anmeldedatum.isoformat()
                                if bachelorarbeit._anmeldedatum
                                else None
                            ),
                            (
                                bachelorarbeit._fristablaufdatum.isoformat()
                                if bachelorarbeit._fristablaufdatum
                                else None
                            ),
                            (
                                bachelorarbeit._startdatum.isoformat()
                                if bachelorarbeit._startdatum
                                else None
                            ),
                            (
                                bachelorarbeit._abgabedatum.isoformat()
                                if bachelorarbeit._abgabedatum
                                else None
                            ),
                            bachelorarbeit.ects,
                            (
                                str(bachelorarbeit.note)
                                if bachelorarbeit.note is not None
                                else None
                            ),
                        ),
                    )

                verbindung.commit()

            except Exception:
                verbindung.rollback()
                raise
    
    
    def ladeStudium(self) -> Studium:
        """Lädt das Studium einschließlich seiner Modulhierarchie."""

        self.initialisiereDatenbank()

        with closing(sqlite3.connect(self._dbPfad)) as verbindung:
            datensatz = verbindung.execute(
                """
                SELECT
                    studiengang,
                    ziel_abschlussdatum,
                    pruefungs_meilenstein,
                    notenziel
                FROM studium
                WHERE id = 1
                """
            ).fetchone()

            if datensatz is None:
                raise ValueError(
                    "Es wurde noch kein Studium gespeichert."
                )

            studium = Studium(
                studiengang=datensatz[0],
                ziel_abschlussdatum=date.fromisoformat(datensatz[1]),
                pruefungs_meilenstein=date.fromisoformat(datensatz[2]),
                notenziel=Decimal(datensatz[3]),
            )

            modul_datensaetze = verbindung.execute(
                """
                SELECT
                    id,
                    elternmodul_id,
                    modulname,
                    modultyp,
                    modulart,
                    ects
                FROM module
                WHERE studium_id = 1
                ORDER BY id
                """
            ).fetchall()

            # Zunächst alle Modulobjekte erstellen
            module_nach_id = {}

            for (
                modul_id,
                elternmodul_id,
                modulname,
                modultyp,
                modulart,
                ects,
            ) in modul_datensaetze:

                if modultyp == "EINZEL":
                    modul = Einzelmodul(
                        modulname,
                        Modulart[modulart],
                        ects,
                    )

                elif modultyp == "UEBER":
                    modul = Uebermodul(modulname)

                else:
                    raise ValueError(
                        f"Unbekannter Modultyp: {modultyp}"
                    )

                module_nach_id[modul_id] = modul

            # Prüfungsleistungen aus der Datenbank laden
            pruefungs_datensaetze = verbindung.execute(
                """
                SELECT
                    modul_id,
                    pruefungsart,
                    bewertungsart,
                    status,
                    geplantes_pruefungsdatum,
                    note,
                    ergebnis
                FROM pruefungsleistungen
                """
            ).fetchall()

            for (
                modul_id,
                pruefungsart,
                bewertungsart,
                status,
                geplantes_datum,
                note,
                ergebnis,
            ) in pruefungs_datensaetze:

                modul = module_nach_id.get(modul_id)

                if not isinstance(modul, Einzelmodul):
                    raise ValueError(
                        "Prüfungsleistung ohne gültiges Einzelmodul."
                    )

                pruefung = Pruefungsleistung(
                    Pruefungsart[pruefungsart],
                    Bewertungsart[bewertungsart],
                    Status[status],
                    (
                        date.fromisoformat(geplantes_datum)
                        if geplantes_datum is not None
                        else None
                    ),
                )

                if note is not None:
                    pruefung.setzeNote(Decimal(note))

                if ergebnis is not None:
                    pruefung.setzeErgebnis(
                        Pruefungsergebnis[ergebnis]
                    )

                modul.setzePruefungsleistung(pruefung)

            # Danach Eltern-Kind-Beziehungen herstellen
            for (
                modul_id,
                elternmodul_id,
                modulname,
                modultyp,
                modulart,
                ects,
            ) in modul_datensaetze:

                modul = module_nach_id[modul_id]

                if elternmodul_id is None:
                    studium.fuegeModulHinzu(modul)

                else:
                    elternmodul = module_nach_id.get(
                        elternmodul_id
                    )

                    if not isinstance(elternmodul, Uebermodul):
                        raise ValueError(
                            "Ungültige Modulhierarchie in der Datenbank."
                        )

                    elternmodul.fuegeUntermodulHinzu(modul)

            # Bachelorarbeit aus der Datenbank laden
            bachelor_datensatz = verbindung.execute(
                """
                SELECT
                    status,
                    anmeldedatum,
                    fristablaufdatum,
                    startdatum,
                    abgabedatum,
                    ects,
                    note
                FROM bachelorarbeiten
                WHERE studium_id = 1
                """
            ).fetchone()

            if bachelor_datensatz is not None:
                (
                    status,
                    anmeldedatum,
                    fristablaufdatum,
                    startdatum,
                    abgabedatum,
                    ects,
                    note,
                ) = bachelor_datensatz

                bachelorarbeit = Bachelorarbeit(
                    status=BachelorarbeitsStatus[status],
                    anmeldedatum=(
                        date.fromisoformat(anmeldedatum)
                        if anmeldedatum is not None
                        else None
                    ),
                    fristablaufdatum=(
                        date.fromisoformat(fristablaufdatum)
                        if fristablaufdatum is not None
                        else None
                    ),
                    startdatum=(
                        date.fromisoformat(startdatum)
                        if startdatum is not None
                        else None
                    ),
                    abgabedatum=(
                        date.fromisoformat(abgabedatum)
                        if abgabedatum is not None
                        else None
                    ),
                    ects=ects,
                    note=(
                        Decimal(note)
                        if note is not None
                        else None
                    ),
                )

                studium.setzeBachelorarbeit(bachelorarbeit)

        return studium


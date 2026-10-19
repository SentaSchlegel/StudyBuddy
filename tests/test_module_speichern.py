
import sqlite3
import tempfile
from pathlib import Path
from contextlib import closing
from datetime import date
from decimal import Decimal

from studybuddy.enums import (
    Modulart,
    Pruefungsart,
    Bewertungsart,
)

from studybuddy.modelle import (
    Studium,
    Einzelmodul,
    Uebermodul,
    Pruefungsleistung,
)

from studybuddy.repository import DatenbankRepository


def test_module_speichern():
    with tempfile.TemporaryDirectory() as ordner:
        db_pfad = str(Path(ordner) / "test.db")

        studium = Studium(
            "Wirtschaftsinformatik",
            date(2027, 3, 31),
            date(2026, 12, 16),
            Decimal("2.5"),
        )

        uebermodul = Uebermodul("Programmierung")

        python_modul = Einzelmodul(
            "Python",
            Modulart.PFLICHT,
            5,
        )

        pruefung = Pruefungsleistung(
            Pruefungsart.KLAUSUR,
            Bewertungsart.BENOTET,
        )
        pruefung.setzeNote(Decimal("1.7"))

        python_modul.setzePruefungsleistung(pruefung)
        uebermodul.fuegeUntermodulHinzu(python_modul)
        studium.fuegeModulHinzu(uebermodul)

        repository = DatenbankRepository(db_pfad)
        repository.speichereStudium(studium)

        with closing(sqlite3.connect(db_pfad)) as verbindung:
            module = verbindung.execute(
                """
                SELECT modulname, modultyp, elternmodul_id
                FROM module
                ORDER BY id
                """
            ).fetchall()

            pruefungen = verbindung.execute(
                """
                SELECT pruefungsart, note
                FROM pruefungsleistungen
                """
            ).fetchall()

        assert len(module) == 2
        assert module[0][0] == "Programmierung"
        assert module[0][1] == "UEBER"
        assert module[0][2] is None

        assert module[1][0] == "Python"
        assert module[1][1] == "EINZEL"
        assert module[1][2] is not None

        assert pruefungen == [("KLAUSUR", "1.7")]

    print("Alle Modulspeichertests erfolgreich!")


if __name__ == "__main__":
    test_module_speichern()

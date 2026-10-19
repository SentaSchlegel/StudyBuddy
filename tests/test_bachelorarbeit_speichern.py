
import sqlite3
import tempfile
from contextlib import closing
from datetime import date
from decimal import Decimal
from pathlib import Path

from studybuddy.enums import BachelorarbeitsStatus
from studybuddy.modelle import Studium, Bachelorarbeit
from studybuddy.repository import DatenbankRepository


def test_bachelorarbeit_speichern():
    with tempfile.TemporaryDirectory() as ordner:
        db_pfad = str(Path(ordner) / "test.db")

        studium = Studium(
            "Wirtschaftsinformatik",
            date(2027, 3, 31),
            date(2026, 12, 16),
            Decimal("2.5"),
        )

        bachelorarbeit = Bachelorarbeit(
            status=BachelorarbeitsStatus.BENOTET,
            anmeldedatum=date(2027, 1, 5),
            fristablaufdatum=date(2027, 3, 31),
            startdatum=date(2027, 1, 5),
            abgabedatum=date(2027, 3, 20),
            ects=10,
            note=Decimal("1.7"),
        )

        studium.setzeBachelorarbeit(bachelorarbeit)

        repository = DatenbankRepository(db_pfad)
        repository.speichereStudium(studium)

        with closing(sqlite3.connect(db_pfad)) as verbindung:
            datensatz = verbindung.execute(
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

        assert datensatz == (
            "BENOTET",
            "2027-01-05",
            "2027-03-31",
            "2027-01-05",
            "2027-03-20",
            10,
            "1.7",
        )

    print("Alle Bachelorarbeit-Speichertests erfolgreich!")


if __name__ == "__main__":
    test_bachelorarbeit_speichern()

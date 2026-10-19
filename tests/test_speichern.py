
import sqlite3
import tempfile
from pathlib import Path
from contextlib import closing
from datetime import date
from decimal import Decimal

from studybuddy.modelle import Studium
from studybuddy.repository import DatenbankRepository


def test_speichern():
    with tempfile.TemporaryDirectory() as ordner:
        db_pfad = str(Path(ordner) / "test.db")

        studium = Studium(
            "Wirtschaftsinformatik",
            date(2027, 3, 31),
            date(2026, 12, 16),
            Decimal("2.5"),
        )

        repository = DatenbankRepository(db_pfad)
        repository.speichereStudium(studium)

        with closing(sqlite3.connect(db_pfad)) as verbindung:
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

        assert datensatz == (
            "Wirtschaftsinformatik",
            "2027-03-31",
            "2026-12-16",
            "2.5",
        )

    print("Alle Speichertests erfolgreich!")


if __name__ == "__main__":
    test_speichern()

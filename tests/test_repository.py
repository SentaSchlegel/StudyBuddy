
import sqlite3
import tempfile
from pathlib import Path
from contextlib import closing

from studybuddy.repository import DatenbankRepository


def test_repository():
    with tempfile.TemporaryDirectory() as ordner:
        db_pfad = str(Path(ordner) / "test_studybuddy.db")

        repository = DatenbankRepository(db_pfad)
        repository.initialisiereDatenbank()

        with closing(sqlite3.connect(db_pfad)) as verbindung:
            tabellen = {
                zeile[0]
                for zeile in verbindung.execute("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                """)
            }

        erwartete_tabellen = {
            "studium",
            "module",
            "pruefungsleistungen",
            "bachelorarbeiten",
        }

        assert erwartete_tabellen.issubset(tabellen)

    print("Alle Datenbanktests erfolgreich!")


if __name__ == "__main__":
    test_repository()

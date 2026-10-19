
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

from studybuddy.modelle import Studium
from studybuddy.repository import DatenbankRepository


def test_studium_laden():
    with tempfile.TemporaryDirectory() as ordner:
        db_pfad = str(Path(ordner) / "test.db")

        original = Studium(
            "Wirtschaftsinformatik",
            date(2027, 3, 31),
            date(2026, 12, 16),
            Decimal("2.5"),
        )

        repository = DatenbankRepository(db_pfad)
        repository.speichereStudium(original)

        geladen = repository.ladeStudium()

        assert geladen._studiengang == "Wirtschaftsinformatik"
        assert geladen._zielAbschlussdatum == date(2027, 3, 31)
        assert geladen._pruefungsMeilenstein == date(2026, 12, 16)
        assert geladen._notenziel == Decimal("2.5")

    print("Alle Studium-Ladetests erfolgreich!")


if __name__ == "__main__":
    test_studium_laden()

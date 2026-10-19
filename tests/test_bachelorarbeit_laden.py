
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

from studybuddy.enums import BachelorarbeitsStatus
from studybuddy.modelle import Studium, Bachelorarbeit
from studybuddy.repository import DatenbankRepository


def test_bachelorarbeit_laden():
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

        geladen = repository.ladeStudium()

        geladene_bachelorarbeit = geladen._bachelorarbeit

        assert geladene_bachelorarbeit is not None
        assert (
            geladene_bachelorarbeit._status
            == BachelorarbeitsStatus.BENOTET
        )
        assert geladene_bachelorarbeit.ects == 10
        assert geladene_bachelorarbeit.note == Decimal("1.7")
        assert (
            geladene_bachelorarbeit._anmeldedatum
            == date(2027, 1, 5)
        )
        assert (
            geladene_bachelorarbeit._fristablaufdatum
            == date(2027, 3, 31)
        )
        assert (
            geladene_bachelorarbeit._startdatum
            == date(2027, 1, 5)
        )
        assert (
            geladene_bachelorarbeit._abgabedatum
            == date(2027, 3, 20)
        )

        assert (
            geladen.berechneAktuellenNotendurchschnitt()
            == Decimal("1.7")
        )

    print("Alle Bachelorarbeit-Ladetests erfolgreich!")


if __name__ == "__main__":
    test_bachelorarbeit_laden()

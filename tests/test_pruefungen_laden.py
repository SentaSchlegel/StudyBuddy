
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

from studybuddy.enums import (
    Modulart,
    Pruefungsart,
    Bewertungsart,
    Status,
    Pruefungsergebnis,
)

from studybuddy.modelle import (
    Studium,
    Einzelmodul,
    Pruefungsleistung,
)

from studybuddy.repository import DatenbankRepository


def test_pruefungen_laden():
    with tempfile.TemporaryDirectory() as ordner:
        db_pfad = str(Path(ordner) / "test.db")

        studium = Studium(
            "Wirtschaftsinformatik",
            date(2027, 3, 31),
            date(2026, 12, 16),
            Decimal("2.5"),
        )

        modul = Einzelmodul(
            "Python",
            Modulart.PFLICHT,
            5,
        )

        pruefung = Pruefungsleistung(
            Pruefungsart.KLAUSUR,
            Bewertungsart.BENOTET,
            Status.ABGESCHLOSSEN,
            date(2026, 10, 15),
        )

        pruefung.setzeNote(Decimal("1.7"))
        pruefung.setzeErgebnis(Pruefungsergebnis.BESTANDEN)

        modul.setzePruefungsleistung(pruefung)
        studium.fuegeModulHinzu(modul)

        repository = DatenbankRepository(db_pfad)
        repository.speichereStudium(studium)

        geladen = repository.ladeStudium()
        geladenes_modul = geladen.gibEinzelmodule()[0]
        geladene_pruefung = geladenes_modul._pruefungsleistung

        assert geladene_pruefung is not None
        assert geladene_pruefung._pruefungsart == Pruefungsart.KLAUSUR
        assert geladene_pruefung.bewertungsart == Bewertungsart.BENOTET
        assert geladene_pruefung._status == Status.ABGESCHLOSSEN
        assert (
            geladene_pruefung._geplantes_pruefungsdatum
            == date(2026, 10, 15)
        )
        assert geladene_pruefung.note == Decimal("1.7")
        assert geladene_pruefung.ergebnis == Pruefungsergebnis.BESTANDEN

        assert (
            geladen.berechneAktuellenNotendurchschnitt()
            == Decimal("1.7")
        )

    print("Alle Prüfungsleistung-Ladetests erfolgreich!")


if __name__ == "__main__":
    test_pruefungen_laden()

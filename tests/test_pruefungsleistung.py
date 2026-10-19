
from decimal import Decimal

from studybuddy.enums import (
    Modulart,
    Pruefungsart,
    Bewertungsart,
    Pruefungsergebnis,
)
from studybuddy.modelle import Einzelmodul, Pruefungsleistung


def test_pruefungsleistung():
    pruefung = Pruefungsleistung(
        Pruefungsart.KLAUSUR,
        Bewertungsart.BENOTET,
    )

    pruefung.setzeNote(Decimal("2.0"))
    pruefung.setzeErgebnis(Pruefungsergebnis.BESTANDEN)

    assert pruefung.note == Decimal("2.0")

    try:
        pruefung.setzeNote(Decimal("6.0"))
        assert False, "Ungültige Note wurde nicht verhindert."
    except ValueError:
        pass

    assert pruefung.note == Decimal("2.0")

    modul = Einzelmodul("Python", Modulart.PFLICHT, 5)
    modul.setzePruefungsleistung(pruefung)

    anderes_modul = Einzelmodul("Datenbanken", Modulart.PFLICHT, 5)

    try:
        anderes_modul.setzePruefungsleistung(pruefung)
        assert False, "Mehrfachzuordnung wurde nicht verhindert."
    except ValueError:
        pass

    print("Alle Prüfungsleistungstests erfolgreich!")


if __name__ == "__main__":
    test_pruefungsleistung()

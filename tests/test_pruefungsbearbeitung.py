
from datetime import date

from studybuddy.enums import (
    Pruefungsart,
    Bewertungsart,
    Status,
)

from studybuddy.modelle import Pruefungsleistung


def test_pruefungsbearbeitung():
    pruefung = Pruefungsleistung(
        Pruefungsart.KLAUSUR,
        Bewertungsart.BENOTET,
    )

    pruefung.setzeStatus(Status.IN_BEARBEITUNG)

    assert pruefung._status == Status.IN_BEARBEITUNG

    pruefung.setzeGeplantesPruefungsdatum(
        date(2026, 11, 15)
    )

    assert (
        pruefung._geplantes_pruefungsdatum
        == date(2026, 11, 15)
    )

    pruefung.setzeGeplantesPruefungsdatum(None)

    assert pruefung._geplantes_pruefungsdatum is None

    print("Alle Prüfungsbearbeitungstests erfolgreich!")


if __name__ == "__main__":
    test_pruefungsbearbeitung()

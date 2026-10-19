
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
    Bachelorarbeit,
)


def test_notendurchschnitt():
    studium = Studium(
        studiengang="Wirtschaftsinformatik",
        ziel_abschlussdatum=date(2027, 3, 31),
        pruefungs_meilenstein=date(2026, 12, 16),
        notenziel=Decimal("2.5"),
    )

    assert studium.berechneAktuellenNotendurchschnitt() is None

    python_modul = Einzelmodul("Python", Modulart.PFLICHT, 5)
    datenbank_modul = Einzelmodul("Datenbanken", Modulart.PFLICHT, 10)

    python_pruefung = Pruefungsleistung(
        Pruefungsart.KLAUSUR,
        Bewertungsart.BENOTET,
    )
    python_pruefung.setzeNote(Decimal("1.0"))
    python_modul.setzePruefungsleistung(python_pruefung)

    datenbank_pruefung = Pruefungsleistung(
        Pruefungsart.PROJEKTBERICHT,
        Bewertungsart.BENOTET,
    )
    datenbank_pruefung.setzeNote(Decimal("3.0"))
    datenbank_modul.setzePruefungsleistung(datenbank_pruefung)

    uebermodul = Uebermodul("Programmierung")
    uebermodul.fuegeUntermodulHinzu(python_modul)

    studium.fuegeModulHinzu(uebermodul)
    studium.fuegeModulHinzu(datenbank_modul)

    # (1.0 * 5 + 3.0 * 10) / 15
    erwartet = Decimal("35") / Decimal("15")

    assert studium.berechneAktuellenNotendurchschnitt() == erwartet

    bachelorarbeit = Bachelorarbeit(
        ects=10,
        note=Decimal("2.0"),
    )
    studium.setzeBachelorarbeit(bachelorarbeit)

    # (1.0 * 5 + 3.0 * 10 + 2.0 * 10) / 25
    erwartet_mit_bachelorarbeit = Decimal("55") / Decimal("25")

    assert (
        studium.berechneAktuellenNotendurchschnitt()
        == erwartet_mit_bachelorarbeit
    )

    print("Alle Notendurchschnittstests erfolgreich!")


if __name__ == "__main__":
    test_notendurchschnitt()

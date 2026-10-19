
from decimal import Decimal

from studybuddy.enums import (
    Modulart,
    Pruefungsart,
    Bewertungsart,
)

from studybuddy.modelle import (
    Einzelmodul,
    Uebermodul,
    Pruefungsleistung,
    Studium,
)

from datetime import date


def erwartet_value_error(aktion):
    """Prüft, ob eine ungültige Aktion abgelehnt wird."""
    try:
        aktion()
    except ValueError:
        return

    raise AssertionError(
        "Eine ungültige Aktion wurde nicht verhindert."
    )


def test_modellvalidierung():
    # 1. Indirekte Zyklen verhindern
    modul_a = Uebermodul("A")
    modul_b = Uebermodul("B")
    modul_c = Uebermodul("C")

    modul_a.fuegeUntermodulHinzu(modul_b)
    modul_b.fuegeUntermodulHinzu(modul_c)

    erwartet_value_error(
        lambda: modul_c.fuegeUntermodulHinzu(modul_a)
    )

    # 2. Hauptmodule dürfen keine Untermodule werden
    studium = Studium(
        "Wirtschaftsinformatik",
        date(2027, 3, 31),
        date(2026, 12, 16),
        Decimal("2.5"),
    )

    einzelmodul = Einzelmodul(
        "Python",
        Modulart.PFLICHT,
        5,
    )

    studium.fuegeModulHinzu(einzelmodul)

    anderes_uebermodul = Uebermodul("Programmierung")

    erwartet_value_error(
        lambda: anderes_uebermodul.fuegeUntermodulHinzu(
            einzelmodul
        )
    )

    # 3. Unbenotete Prüfungen dürfen keine Note erhalten
    pruefung = Pruefungsleistung(
        Pruefungsart.PORTFOLIO,
        Bewertungsart.UNBENOTET,
    )

    erwartet_value_error(
        lambda: pruefung.setzeNote(Decimal("2.0"))
    )

    assert pruefung.note is None

    print("Alle Modellvalidierungstests erfolgreich!")


if __name__ == "__main__":
    test_modellvalidierung()

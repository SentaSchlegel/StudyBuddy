
from datetime import date
from decimal import Decimal

from studybuddy.enums import Modulart
from studybuddy.modelle import Studium, Einzelmodul, Uebermodul


def test_modul_loeschen():
    studium = Studium(
        "Wirtschaftsinformatik",
        date(2027, 3, 31),
        date(2026, 12, 16),
        Decimal("2.5"),
    )

    # Einzelmodul direkt im Studium
    einzelmodul = Einzelmodul(
        "Datenbanken",
        Modulart.PFLICHT,
        5,
    )

    studium.fuegeModulHinzu(einzelmodul)

    studium.entferneModul(einzelmodul)

    assert einzelmodul not in studium._topLevelModule

    # Einzelmodul innerhalb eines Übermoduls
    uebermodul = Uebermodul("Programmierung")

    python_modul = Einzelmodul(
        "Objektorientierte Programmierung",
        Modulart.PFLICHT,
        5,
    )

    uebermodul.fuegeUntermodulHinzu(python_modul)
    studium.fuegeModulHinzu(uebermodul)

    studium.entferneModul(python_modul)

    assert python_modul not in uebermodul._untermodule
    assert uebermodul.getEcts() == 0

    # Das Übermodul selbst bleibt bestehen
    assert uebermodul in studium._topLevelModule

    print("Alle Modullöschtests erfolgreich!")


if __name__ == "__main__":
    test_modul_loeschen()

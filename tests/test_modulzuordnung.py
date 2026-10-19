
from datetime import date
from decimal import Decimal

from studybuddy.enums import Modulart
from studybuddy.modelle import Studium, Einzelmodul, Uebermodul


def test_modulzuordnung():
    studium = Studium(
        "Wirtschaftsinformatik",
        date(2027, 3, 31),
        date(2026, 12, 16),
        Decimal("2.5"),
    )

    uebermodul = Uebermodul("Programmierung")
    einzelmodul = Einzelmodul(
        "Objektorientierte Programmierung",
        Modulart.WAHLPFLICHT,
        5,
    )

    studium.fuegeModulHinzu(uebermodul)
    studium.fuegeModulHinzu(einzelmodul)

    studium.ordneModulZu(einzelmodul, uebermodul)

    assert einzelmodul not in studium._topLevelModule
    assert einzelmodul in uebermodul._untermodule
    assert einzelmodul._elternmodul is uebermodul
    assert uebermodul.getEcts() == 5

    print("Alle Modulzuordnungstests erfolgreich!")


if __name__ == "__main__":
    test_modulzuordnung()

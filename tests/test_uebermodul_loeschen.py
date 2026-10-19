
from datetime import date
from decimal import Decimal

from studybuddy.enums import Modulart
from studybuddy.modelle import Studium, Einzelmodul, Uebermodul


def test_uebermodul_loeschen():
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

    uebermodul.fuegeUntermodulHinzu(einzelmodul)
    studium.fuegeModulHinzu(uebermodul)

    # Übermodul entfernen
    studium.entferneUebermodul(uebermodul)

    # Übermodul wurde entfernt
    assert uebermodul not in studium._topLevelModule

    # Einzelmodul bleibt erhalten
    assert einzelmodul in studium._topLevelModule

    # Einzelmodul hat kein Elternmodul mehr
    assert einzelmodul._elternmodul is None

    # ECTS bleiben erhalten
    assert einzelmodul.getEcts() == 5

    print("Alle Übermodullöschtests erfolgreich!")


if __name__ == "__main__":
    test_uebermodul_loeschen()

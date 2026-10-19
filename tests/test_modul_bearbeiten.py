
from studybuddy.enums import Modulart
from studybuddy.modelle import Einzelmodul, Uebermodul


def test_modul_bearbeiten():
    modul = Einzelmodul(
        "Objektorientierte Programmierung",
        Modulart.PFLICHT,
        5,
    )

    uebermodul = Uebermodul("Programmierung")
    uebermodul.fuegeUntermodulHinzu(modul)

    # Modulnamen ändern
    modul.setzeModulname("Python OOP")
    assert modul.modulname == "Python OOP"

    # Modulart ändern
    modul.setzeModulart(Modulart.WAHLPFLICHT)
    assert modul._modulart == Modulart.WAHLPFLICHT

    # ECTS ändern
    modul.setzeEcts(10)
    assert modul.getEcts() == 10

    # ECTS des Übermoduls müssen automatisch mitsteigen
    assert uebermodul.getEcts() == 10

    # Ungültige ECTS verhindern
    try:
        modul.setzeEcts(-5)
        raise AssertionError("Ungültige ECTS wurden akzeptiert.")
    except ValueError:
        pass

    print("Alle Modulbearbeitungstests erfolgreich!")


if __name__ == "__main__":
    test_modul_bearbeiten()

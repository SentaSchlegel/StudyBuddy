
from studybuddy.enums import Modulart
from studybuddy.modelle import Einzelmodul, Uebermodul


def test_modulhierarchie():
    daten = Einzelmodul("Datenanalyse", Modulart.PFLICHT, 5)
    python = Einzelmodul("Python", Modulart.PFLICHT, 5)

    uebermodul = Uebermodul("Programmierung")
    uebermodul.fuegeUntermodulHinzu(daten)
    uebermodul.fuegeUntermodulHinzu(python)

    assert uebermodul.getEcts() == 10

    try:
        uebermodul.fuegeUntermodulHinzu(daten)
        assert False, "Doppelte Zuordnung wurde nicht verhindert."
    except ValueError:
        pass

    anderes = Uebermodul("Anderes Übermodul")

    try:
        anderes.fuegeUntermodulHinzu(daten)
        assert False, "Mehrfachzuordnung wurde nicht verhindert."
    except ValueError:
        pass

    try:
        uebermodul.fuegeUntermodulHinzu(uebermodul)
        assert False, "Selbstzuordnung wurde nicht verhindert."
    except ValueError:
        pass

    print("Alle Modultests erfolgreich!")


if __name__ == "__main__":
    test_modulhierarchie()

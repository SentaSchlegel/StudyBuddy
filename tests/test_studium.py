
from datetime import date
from decimal import Decimal

from studybuddy.enums import Modulart
from studybuddy.modelle import Studium, Einzelmodul, Uebermodul


def test_studium():
    studium = Studium(
        studiengang="Wirtschaftsinformatik",
        ziel_abschlussdatum=date(2027, 3, 31),
        pruefungs_meilenstein=date(2026, 12, 16),
        notenziel=Decimal("2.5"),
    )

    python_modul = Einzelmodul(
        "Python", Modulart.PFLICHT, 5
    )

    datenbank_modul = Einzelmodul(
        "Datenbanken", Modulart.PFLICHT, 5
    )

    uebermodul = Uebermodul("Programmierung")
    uebermodul.fuegeUntermodulHinzu(python_modul)

    studium.fuegeModulHinzu(uebermodul)
    studium.fuegeModulHinzu(datenbank_modul)

    einzelmodule = studium.gibEinzelmodule()

    assert len(einzelmodule) == 2
    assert python_modul in einzelmodule
    assert datenbank_modul in einzelmodule

    try:
        studium.fuegeModulHinzu(python_modul)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Ein Untermodul wurde als Hauptmodul akzeptiert."
        )

    try:
        studium.fuegeModulHinzu(datenbank_modul)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Eine doppelte Hauptmodulzuordnung wurde akzeptiert."
        )

    print("Alle Studiumstests erfolgreich!")


if __name__ == "__main__":
    test_studium()

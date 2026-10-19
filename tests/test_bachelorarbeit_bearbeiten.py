
from datetime import date

from studybuddy.enums import BachelorarbeitsStatus
from studybuddy.modelle import Bachelorarbeit


def test_bachelorarbeit_bearbeiten():
    bachelorarbeit = Bachelorarbeit(ects=10)

    bachelorarbeit.setzeStatus(
        BachelorarbeitsStatus.ANGEMELDET
    )

    assert (
        bachelorarbeit._status
        == BachelorarbeitsStatus.ANGEMELDET
    )

    bachelorarbeit.setzeTermine(
        anmeldedatum=date(2027, 1, 10),
        fristablaufdatum=date(2027, 3, 31),
        startdatum=date(2027, 1, 15),
        abgabedatum=None,
    )

    assert bachelorarbeit._anmeldedatum == date(2027, 1, 10)
    assert bachelorarbeit._startdatum == date(2027, 1, 15)
    assert bachelorarbeit._fristablaufdatum == date(2027, 3, 31)
    assert bachelorarbeit._abgabedatum is None

    print("Alle Bachelorarbeits-Bearbeitungstests erfolgreich!")


if __name__ == "__main__":
    test_bachelorarbeit_bearbeiten()

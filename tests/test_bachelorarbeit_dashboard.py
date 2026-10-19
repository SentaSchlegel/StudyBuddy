
from datetime import date
from decimal import Decimal

from studybuddy.modelle import Studium, Bachelorarbeit
from studybuddy.enums import BachelorarbeitsStatus


def test_bachelorarbeit_dashboard():
    studium = Studium(
        "Wirtschaftsinformatik",
        date(2027, 3, 31),
        date(2026, 12, 16),
        Decimal("2.5"),
    )

    bachelorarbeit = Bachelorarbeit(ects=10)
    bachelorarbeit.setzeStatus(BachelorarbeitsStatus.ANGEMELDET)

    bachelorarbeit.setzeTermine(
        date(2027, 2, 1),
        date(2027, 3, 15),
        None,
        None,
    )

    studium.setzeBachelorarbeit(bachelorarbeit)

    assert studium._bachelorarbeit is bachelorarbeit
    assert bachelorarbeit._fristablaufdatum == date(2027, 3, 15)
    assert bachelorarbeit._status == BachelorarbeitsStatus.ANGEMELDET

    print("Bachelorarbeits-Datentest erfolgreich!")


if __name__ == "__main__":
    test_bachelorarbeit_dashboard()

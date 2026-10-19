
from datetime import date, timedelta
from decimal import Decimal

from studybuddy.modelle import Bachelorarbeit


def test_bachelorarbeit():
    abgabe = date.today() + timedelta(days=30)

    arbeit = Bachelorarbeit(
        ects=10,
        fristablaufdatum=abgabe,
        note=Decimal("1.7"),
    )

    assert arbeit.ects == 10
    assert arbeit.note == Decimal("1.7")
    assert arbeit.berechneVerbleibendeTage() == 30

    try:
        arbeit.setzeNote(Decimal("6.0"))
    except ValueError:
        pass
    else:
        raise AssertionError("Ungültige Note wurde akzeptiert.")

    assert arbeit.note == Decimal("1.7")

    print("Alle Bachelorarbeitstests erfolgreich!")


if __name__ == "__main__":
    test_bachelorarbeit()

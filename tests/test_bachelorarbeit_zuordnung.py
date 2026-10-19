
from datetime import date
from decimal import Decimal

import pytest

from studybuddy.modelle import Studium, Bachelorarbeit


def test_bachelorarbeit_exklusive_zuordnung():
    studium1 = Studium(
        "Wirtschaftsinformatik",
        date(2027, 3, 31),
        date(2026, 12, 16),
        Decimal("2.5"),
    )

    studium2 = Studium(
        "Informatik",
        date(2027, 3, 31),
        date(2026, 12, 16),
        Decimal("2.5"),
    )

    bachelorarbeit = Bachelorarbeit(ects=10)

    studium1.setzeBachelorarbeit(bachelorarbeit)

    assert studium1._bachelorarbeit is bachelorarbeit
    assert bachelorarbeit._studium is studium1

    # Dieselbe Bachelorarbeit darf nicht
    # einem zweiten Studium zugeordnet werden.
    with pytest.raises(ValueError):
        studium2.setzeBachelorarbeit(bachelorarbeit)

    assert studium2._bachelorarbeit is None

    print("Exklusive Bachelorarbeitszuordnung erfolgreich!")


if __name__ == "__main__":
    test_bachelorarbeit_exklusive_zuordnung()

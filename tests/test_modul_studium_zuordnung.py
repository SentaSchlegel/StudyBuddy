
from datetime import date
from decimal import Decimal

import pytest

from studybuddy.modelle import Studium, Einzelmodul
from studybuddy.enums import Modulart


def test_modul_nicht_in_zwei_studien():
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

    modul = Einzelmodul(
        "Objektorientierte Programmierung",
        Modulart.PFLICHT,
        5,
    )

    studium1.fuegeModulHinzu(modul)

    with pytest.raises(ValueError):
        studium2.fuegeModulHinzu(modul)

    assert modul in studium1._topLevelModule
    assert modul not in studium2._topLevelModule

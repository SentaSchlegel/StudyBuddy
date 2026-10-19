
from decimal import Decimal

from studybuddy.enums import NotenzielStatus
from studybuddy.modelle import NotenzielErgebnis


def test_notenziel_ergebnis():
    ergebnis = NotenzielErgebnis(
        Decimal("2.3"),
        NotenzielStatus.BERECHNET,
    )

    assert ergebnis.benoetigterDurchschnitt == Decimal("2.3")
    assert ergebnis.status == NotenzielStatus.BERECHNET

    ohne_offene_leistungen = NotenzielErgebnis(
        None,
        NotenzielStatus.KEINE_OFFENEN_LEISTUNGEN,
    )

    assert ohne_offene_leistungen.benoetigterDurchschnitt is None

    print("Alle NotenzielErgebnis-Tests erfolgreich!")


if __name__ == "__main__":
    test_notenziel_ergebnis()

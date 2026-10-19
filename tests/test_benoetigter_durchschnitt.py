
from datetime import date
from decimal import Decimal

from studybuddy.enums import (
    Modulart,
    Pruefungsart,
    Bewertungsart,
    NotenzielStatus,
)

from studybuddy.modelle import (
    Studium,
    Einzelmodul,
    Pruefungsleistung,
)


def erstelle_studium(notenziel):
    return Studium(
        studiengang="Wirtschaftsinformatik",
        ziel_abschlussdatum=date(2027, 3, 31),
        pruefungs_meilenstein=date(2026, 12, 16),
        notenziel=Decimal(notenziel),
    )


def fuege_pruefung_hinzu(studium, name, ects, note=None):
    modul = Einzelmodul(name, Modulart.PFLICHT, ects)

    pruefung = Pruefungsleistung(
        Pruefungsart.KLAUSUR,
        Bewertungsart.BENOTET,
    )

    if note is not None:
        pruefung.setzeNote(Decimal(note))

    modul.setzePruefungsleistung(pruefung)
    studium.fuegeModulHinzu(modul)


def test_benoetigter_durchschnitt():
    # Fall 1: Ziel ist erreichbar
    studium = erstelle_studium("2.5")

    fuege_pruefung_hinzu(studium, "Python", 5, "2.0")
    fuege_pruefung_hinzu(studium, "Datenbanken", 5)

    ergebnis = studium.berechneBenoetigtenNotendurchschnitt()

    assert ergebnis.benoetigterDurchschnitt == Decimal("3.0")
    assert ergebnis.status == NotenzielStatus.BERECHNET

    # Fall 2: Ziel ist nicht mehr erreichbar
    studium = erstelle_studium("1.0")

    fuege_pruefung_hinzu(studium, "Python", 5, "4.0")
    fuege_pruefung_hinzu(studium, "Datenbanken", 5)

    ergebnis = studium.berechneBenoetigtenNotendurchschnitt()

    assert ergebnis.status == NotenzielStatus.NICHT_ERREICHBAR

    # Fall 3: Ziel ist bereits gesichert
    studium = erstelle_studium("4.0")

    fuege_pruefung_hinzu(studium, "Python", 5, "1.0")
    fuege_pruefung_hinzu(studium, "Datenbanken", 5)

    ergebnis = studium.berechneBenoetigtenNotendurchschnitt()

    assert ergebnis.status == NotenzielStatus.BEREITS_GESICHERT

    # Fall 4: Keine offenen benoteten Leistungen
    studium = erstelle_studium("2.5")

    fuege_pruefung_hinzu(studium, "Python", 5, "2.0")

    ergebnis = studium.berechneBenoetigtenNotendurchschnitt()

    assert (
        ergebnis.status
        == NotenzielStatus.KEINE_OFFENEN_LEISTUNGEN
    )

    print("Alle Tests zum benötigten Durchschnitt erfolgreich!")


if __name__ == "__main__":
    test_benoetigter_durchschnitt()

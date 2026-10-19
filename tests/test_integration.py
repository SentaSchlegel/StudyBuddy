
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

from studybuddy.enums import (
    Modulart,
    Pruefungsart,
    Bewertungsart,
    Status,
    Pruefungsergebnis,
    BachelorarbeitsStatus,
)

from studybuddy.modelle import (
    Studium,
    Einzelmodul,
    Uebermodul,
    Pruefungsleistung,
    Bachelorarbeit,
)

from studybuddy.repository import DatenbankRepository


def test_integration():
    with tempfile.TemporaryDirectory() as ordner:
        db_pfad = str(Path(ordner) / "integration.db")

        studium = Studium(
            "Wirtschaftsinformatik",
            date(2027, 3, 31),
            date(2026, 12, 16),
            Decimal("2.5"),
        )

        # Verschachtelte Modulstruktur
        programmierung = Uebermodul("Programmierung")
        grundlagen = Uebermodul("Grundlagen")

        python = Einzelmodul("Python", Modulart.PFLICHT, 5)
        datenbanken = Einzelmodul("Datenbanken", Modulart.PFLICHT, 10)
        projekt = Einzelmodul("Praxisprojekt", Modulart.PFLICHT, 5)

        # Benotete Prüfung
        python_pruefung = Pruefungsleistung(
            Pruefungsart.KLAUSUR,
            Bewertungsart.BENOTET,
            Status.ABGESCHLOSSEN,
        )
        python_pruefung.setzeNote(Decimal("1.7"))
        python_pruefung.setzeErgebnis(Pruefungsergebnis.BESTANDEN)
        python.setzePruefungsleistung(python_pruefung)

        # Noch offene benotete Prüfung
        datenbank_pruefung = Pruefungsleistung(
            Pruefungsart.PROJEKTBERICHT,
            Bewertungsart.BENOTET,
            Status.IN_BEARBEITUNG,
        )
        datenbanken.setzePruefungsleistung(datenbank_pruefung)

        # Unbenotete Prüfung
        projekt_pruefung = Pruefungsleistung(
            Pruefungsart.PORTFOLIO,
            Bewertungsart.UNBENOTET,
            Status.ABGESCHLOSSEN,
        )
        projekt_pruefung.setzeErgebnis(Pruefungsergebnis.BESTANDEN)
        projekt.setzePruefungsleistung(projekt_pruefung)

        grundlagen.fuegeUntermodulHinzu(python)
        grundlagen.fuegeUntermodulHinzu(datenbanken)
        programmierung.fuegeUntermodulHinzu(grundlagen)

        studium.fuegeModulHinzu(programmierung)
        studium.fuegeModulHinzu(projekt)

        # Bachelorarbeit
        bachelorarbeit = Bachelorarbeit(
            status=BachelorarbeitsStatus.BENOTET,
            ects=10,
            note=Decimal("2.0"),
        )
        studium.setzeBachelorarbeit(bachelorarbeit)

        # Ergebnisse vor dem Speichern
        durchschnitt_vorher = (
            studium.berechneAktuellenNotendurchschnitt()
        )
        notenziel_vorher = (
            studium.berechneBenoetigtenNotendurchschnitt()
        )

        # Speichern und erneut laden
        repository = DatenbankRepository(db_pfad)
        repository.speichereStudium(studium)

        geladen = repository.ladeStudium()

        # Grunddaten prüfen
        assert geladen._studiengang == studium._studiengang
        assert geladen._notenziel == studium._notenziel

        # Modulstruktur prüfen
        assert len(geladen._topLevelModule) == 2
        assert len(geladen.gibEinzelmodule()) == 3

        geladenes_programmierung = geladen._topLevelModule[0]
        assert geladenes_programmierung.getEcts() == 15

        # Prüfungsleistungen prüfen
        module_nach_name = {
            modul.modulname: modul
            for modul in geladen.gibEinzelmodule()
        }

        assert (
            module_nach_name["Python"]._pruefungsleistung.note
            == Decimal("1.7")
        )
        assert (
            module_nach_name["Datenbanken"]._pruefungsleistung.note
            is None
        )
        assert (
            module_nach_name["Praxisprojekt"]
            ._pruefungsleistung.bewertungsart
            == Bewertungsart.UNBENOTET
        )

        # Bachelorarbeit prüfen
        assert geladen._bachelorarbeit is not None
        assert geladen._bachelorarbeit.note == Decimal("2.0")

        # Berechnungen vor und nach dem Laden vergleichen
        assert (
            geladen.berechneAktuellenNotendurchschnitt()
            == durchschnitt_vorher
        )

        notenziel_nachher = (
            geladen.berechneBenoetigtenNotendurchschnitt()
        )

        assert (
            notenziel_nachher.benoetigterDurchschnitt
            == notenziel_vorher.benoetigterDurchschnitt
        )
        assert notenziel_nachher.status == notenziel_vorher.status

        # Auch wiederholtes Speichern darf keine Duplikate erzeugen
        repository.speichereStudium(geladen)
        erneut_geladen = repository.ladeStudium()

        assert len(erneut_geladen.gibEinzelmodule()) == 3

    print("Alle Integrationstests erfolgreich!")


if __name__ == "__main__":
    test_integration()

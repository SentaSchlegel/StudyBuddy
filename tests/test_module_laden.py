
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

from studybuddy.enums import Modulart
from studybuddy.modelle import Studium, Einzelmodul, Uebermodul
from studybuddy.repository import DatenbankRepository


def test_module_laden():
    with tempfile.TemporaryDirectory() as ordner:
        db_pfad = str(Path(ordner) / "test.db")

        studium = Studium(
            "Wirtschaftsinformatik",
            date(2027, 3, 31),
            date(2026, 12, 16),
            Decimal("2.5"),
        )

        programmierung = Uebermodul("Programmierung")
        python = Einzelmodul("Python", Modulart.PFLICHT, 5)

        grundlagen = Uebermodul("Grundlagen")
        datenbanken = Einzelmodul(
            "Datenbanken",
            Modulart.PFLICHT,
            10,
        )

        grundlagen.fuegeUntermodulHinzu(datenbanken)
        programmierung.fuegeUntermodulHinzu(python)
        programmierung.fuegeUntermodulHinzu(grundlagen)

        studium.fuegeModulHinzu(programmierung)

        repository = DatenbankRepository(db_pfad)
        repository.speichereStudium(studium)

        geladen = repository.ladeStudium()

        assert len(geladen._topLevelModule) == 1

        geladenes_uebermodul = geladen._topLevelModule[0]

        assert isinstance(geladenes_uebermodul, Uebermodul)
        assert geladenes_uebermodul.modulname == "Programmierung"
        assert geladenes_uebermodul.getEcts() == 15

        einzelmodule = geladen.gibEinzelmodule()

        assert len(einzelmodule) == 2

        namen = {modul.modulname for modul in einzelmodule}

        assert namen == {"Python", "Datenbanken"}

    print("Alle Modul-Ladetests erfolgreich!")


if __name__ == "__main__":
    test_module_laden()

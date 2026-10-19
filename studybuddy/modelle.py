
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal, InvalidOperation

from studybuddy.enums import (
    Modulart,
    Pruefungsart,
    Bewertungsart,
    Status,
    Pruefungsergebnis,
    BachelorarbeitsStatus,
    NotenzielStatus,
)


class Modul(ABC):
    """Abstrakte Basisklasse für alle Studienmodule."""

    def __init__(self, modulname: str):
        if not isinstance(modulname, str) or not modulname.strip():
            raise ValueError("Der Modulname darf nicht leer sein.")

        self._modulname = modulname
        self._elternmodul = None

    @property
    def modulname(self) -> str:
        """Gibt den Modulnamen zurück."""
        return self._modulname

    def setzeModulname(self, modulname: str) -> None:
        """Ändert den Namen eines Moduls."""

        if not isinstance(modulname, str) or not modulname.strip():
            raise ValueError(
                "Der Modulname darf nicht leer sein."
            )

        self._modulname = modulname.strip()

    @abstractmethod
    def getEcts(self) -> int:
        """Ermittelt die ECTS eines Moduls."""
        pass


class Einzelmodul(Modul):
    """Ein einzelnes Pflicht- oder Wahlpflichtmodul."""

    def __init__(
        self,
        modulname: str,
        modulart: Modulart,
        ects: int,
    ):
        super().__init__(modulname)

        if not isinstance(modulart, Modulart):
            raise ValueError("Ungültige Modulart.")

        if type(ects) is not int or ects <= 0:
            raise ValueError(
                "ECTS müssen eine positive ganze Zahl sein."
            )

        self._modulart = modulart
        self._ects = ects
        self._pruefungsleistung = None

    def getEcts(self) -> int:
        """Gibt die festgelegten ECTS des Einzelmoduls zurück."""
        return self._ects

    
    def setzeEcts(self, ects: int) -> None:
        """Ändert die ECTS eines Einzelmoduls."""

        if type(ects) is not int or ects <= 0:
            raise ValueError(
                "ECTS müssen eine positive ganze Zahl sein."
            )

        self._ects = ects

    def setzeModulart(self, modulart: Modulart) -> None:
        """Ändert die Modulart eines Einzelmoduls."""

        if not isinstance(modulart, Modulart):
            raise TypeError("Ungültige Modulart.")

        self._modulart = modulart


    def setzePruefungsleistung(
        self,
        pruefung: "Pruefungsleistung",
    ) -> None:
        """Ordnet eine Prüfungsleistung exklusiv zu."""

        if not isinstance(pruefung, Pruefungsleistung):
            raise TypeError(
                "Es muss eine Prüfungsleistung übergeben werden."
            )

        if pruefung._einzelmodul is not None:
            raise ValueError(
                "Die Prüfungsleistung gehört bereits "
                "zu einem Einzelmodul."
            )

        if self._pruefungsleistung is not None:
            raise ValueError(
                "Dieses Einzelmodul besitzt bereits "
                "eine Prüfungsleistung."
            )

        self._pruefungsleistung = pruefung
        pruefung._einzelmodul = self


class Uebermodul(Modul):
    """Ein Modul, das weitere Module enthalten kann."""

    def __init__(self, modulname: str):
        super().__init__(modulname)
        self._untermodule = []

    @property
    def ects(self) -> int:
        """Berechnet die ECTS aus den enthaltenen Modulen."""
        return self.getEcts()

    def getEcts(self) -> int:
        """Ermittelt die ECTS aller Untermodule rekursiv."""
        return sum(
            modul.getEcts()
            for modul in self._untermodule
        )

    def enthaelt(self, modul: Modul) -> bool:
        """Prüft rekursiv, ob ein bestimmtes Modul enthalten ist."""

        for untermodul in self._untermodule:
            if untermodul is modul:
                return True

            if isinstance(untermodul, Uebermodul):
                if untermodul.enthaelt(modul):
                    return True

        return False

    def fuegeUntermodulHinzu(self, modul: Modul) -> None:
        """Verhindert Zyklen und unzulässige Mehrfachzuordnungen."""

        if not isinstance(modul, Modul):
            raise TypeError(
                "Es muss ein Modul übergeben werden."
            )

        if modul is self:
            raise ValueError(
                "Ein Modul darf sich nicht selbst enthalten."
            )

        if (
            isinstance(modul, Uebermodul)
            and modul.enthaelt(self)
        ):
            raise ValueError(
                "Zyklische Modulzuordnung ist nicht erlaubt."
            )

        if getattr(modul, "_ist_top_level", False):
            raise ValueError(
                "Ein Hauptmodul darf nicht gleichzeitig "
                "als Untermodul geführt werden."
            )

        if modul._elternmodul is not None:
            raise ValueError(
                "Das Modul gehört bereits "
                "zu einem anderen Übermodul."
            )

        if any(
            vorhanden is modul
            for vorhanden in self._untermodule
        ):
            raise ValueError(
                "Das Modul ist bereits zugeordnet."
            )

        self._untermodule.append(modul)
        modul._elternmodul = self


class Pruefungsleistung:
    """Verwaltet eine Prüfungsleistung mit gültigen Bewertungsdaten."""

    def __init__(
        self,
        pruefungsart: Pruefungsart,
        bewertungsart: Bewertungsart,
        status: Status = Status.NOCH_NICHT_BEGONNEN,
        geplantes_pruefungsdatum: date | None = None,
    ):
        if not isinstance(pruefungsart, Pruefungsart):
            raise ValueError("Ungültige Prüfungsart.")

        if not isinstance(bewertungsart, Bewertungsart):
            raise ValueError("Ungültige Bewertungsart.")

        if not isinstance(status, Status):
            raise ValueError("Ungültiger Status.")

        if (
            geplantes_pruefungsdatum is not None
            and not isinstance(geplantes_pruefungsdatum, date)
        ):
            raise ValueError("Ungültiges Prüfungsdatum.")

        self._pruefungsart = pruefungsart
        self._bewertungsart = bewertungsart
        self._status = status
        self._geplantes_pruefungsdatum = geplantes_pruefungsdatum

        self._note: Decimal | None = None
        self._ergebnis: Pruefungsergebnis | None = None
        self._einzelmodul: Einzelmodul | None = None

    @property
    def note(self) -> Decimal | None:
        """Gibt die Note zurück."""
        return self._note

    @property
    def ergebnis(self) -> Pruefungsergebnis | None:
        """Gibt das Prüfungsergebnis zurück."""
        return self._ergebnis

    @property
    def bewertungsart(self) -> Bewertungsart:
        """Gibt die Bewertungsart zurück."""
        return self._bewertungsart

    def validiereBewertung(self) -> None:
        """Prüft die fachliche Konsistenz der Bewertungsdaten."""

        if self._bewertungsart == Bewertungsart.UNBENOTET:
            if self._note is not None:
                raise ValueError(
                    "Unbenotete Leistungen dürfen keine Note haben."
                )

        if self._note is not None:
            if not self._note.is_finite():
                raise ValueError(
                    "Die Note muss eine endliche Zahl sein."
                )

            if not (
                Decimal("1.0")
                <= self._note
                <= Decimal("5.0")
            ):
                raise ValueError(
                    "Die Note muss zwischen 1.0 und 5.0 liegen."
                )

            erwartetes_ergebnis = (
                Pruefungsergebnis.BESTANDEN
                if self._note <= Decimal("4.0")
                else Pruefungsergebnis.NICHT_BESTANDEN
            )

            if (
                self._ergebnis is not None
                and self._ergebnis != erwartetes_ergebnis
            ):
                raise ValueError(
                    "Note und Prüfungsergebnis widersprechen sich."
                )

    def setzeNote(self, note: Decimal | None) -> None:
        """Ändert die Note und stellt bei Fehlern den alten Wert wieder her."""

        alte_note = self._note

        if note is not None:
            try:
                note = Decimal(str(note))
            except (ValueError, TypeError, InvalidOperation):
                raise ValueError("Ungültiger Notenwert.")

            if not note.is_finite():
                raise ValueError(
                    "Die Note muss eine endliche Zahl sein."
                )

        self._note = note

        try:
            self.validiereBewertung()
        except ValueError:
            self._note = alte_note
            raise

    def setzeErgebnis(
        self,
        ergebnis: Pruefungsergebnis,
    ) -> None:
        """Ändert das Prüfungsergebnis kontrolliert."""

        if not isinstance(ergebnis, Pruefungsergebnis):
            raise ValueError(
                "Ungültiges Prüfungsergebnis."
            )

        altes_ergebnis = self._ergebnis
        self._ergebnis = ergebnis

        try:
            self.validiereBewertung()
        except ValueError:
            self._ergebnis = altes_ergebnis
            raise

    def setzeBewertungsart(
        self,
        art: Bewertungsart,
    ) -> None:
        """Ändert die Bewertungsart kontrolliert."""

        if not isinstance(art, Bewertungsart):
            raise ValueError(
                "Ungültige Bewertungsart."
            )

        alte_art = self._bewertungsart
        self._bewertungsart = art

        try:
            self.validiereBewertung()
        except ValueError:
            self._bewertungsart = alte_art
            raise
        
    def setzeStatus(self, status: Status) -> None:
        """Ändert den Prüfungsstatus unter Beachtung der Bewertung."""

        if not isinstance(status, Status):
            raise TypeError("Ungültiger Prüfungsstatus.")

        if status == Status.ABGESCHLOSSEN:
            if self._bewertungsart == Bewertungsart.BENOTET:
                if self._note is None:
                    raise ValueError(
                        "Eine benotete Prüfung kann erst mit "
                        "eingetragener Note abgeschlossen werden."
                    )
            elif self._ergebnis is None:
                raise ValueError(
                    "Eine unbenotete Prüfung benötigt zum "
                    "Abschluss ein Prüfungsergebnis."
                )

        if status != Status.ABGESCHLOSSEN:
            if self._note is not None or self._ergebnis is not None:
                raise ValueError(
                    "Eine bereits bewertete Prüfung muss "
                    "den Status 'Abgeschlossen' haben."
                )

        self._status = status


    def setzeGeplantesPruefungsdatum(
        self,
        datum: date | None,
    ) -> None:
        """Legt das geplante Prüfungsdatum fest oder entfernt es."""

        if datum is not None and not isinstance(datum, date):
            raise TypeError(
                "Das Prüfungsdatum muss ein Datum oder None sein."
            )

        self._geplantes_pruefungsdatum = datum

class Bachelorarbeit:
    """Verwaltet den Status, die Termine und die Note der Bachelorarbeit."""

    def __init__(
        self,
        ects: int = 10,
        status: BachelorarbeitsStatus = BachelorarbeitsStatus.NOCH_NICHT_BEGONNEN,
        anmeldedatum: date | None = None,
        fristablaufdatum: date | None = None,
        startdatum: date | None = None,
        abgabedatum: date | None = None,
        note: Decimal | None = None,
    ):
        if type(ects) is not int or ects <= 0:
            raise ValueError("ECTS müssen eine positive ganze Zahl sein.")

        if not isinstance(status, BachelorarbeitsStatus):
            raise ValueError("Ungültiger Bachelorarbeitsstatus.")

        for datum in (
            anmeldedatum,
            fristablaufdatum,
            startdatum,
            abgabedatum,
        ):
            if datum is not None and not isinstance(datum, date):
                raise ValueError("Ungültiges Datum.")

        self._studium = None
        self._ects = ects
        self._status = status
        self._anmeldedatum = anmeldedatum
        self._fristablaufdatum = fristablaufdatum
        self._startdatum = startdatum
        self._abgabedatum = abgabedatum
        self._note = None

        if note is not None:
            self.setzeNote(note)

    @property
    def ects(self) -> int:
        return self._ects

    @property
    def note(self) -> Decimal | None:
        return self._note

    
    def setzeNote(self, note: Decimal | None) -> None:
        """Validiert die Note und synchronisiert den Status."""

        if note is None:
            self._note = None

            if self._status == BachelorarbeitsStatus.BENOTET:
                self._status = BachelorarbeitsStatus.EINGEREICHT

            return

        try:
            wert = Decimal(str(note))
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError("Ungültiger Notenwert.")

        if not wert.is_finite() or not Decimal("1.0") <= wert <= Decimal("5.0"):
            raise ValueError("Die Note muss zwischen 1.0 und 5.0 liegen.")

        self._note = wert
        self._status = BachelorarbeitsStatus.BENOTET


    def berechneVerbleibendeTage(self) -> int | None:
        """Berechnet die verbleibenden Tage bis zum Fristablauf."""
        if self._fristablaufdatum is None:
            return None

        return (self._fristablaufdatum - date.today()).days

    
    def setzeStatus(
        self,
        status: BachelorarbeitsStatus,
    ) -> None:
        """Ändert den Status unter Berücksichtigung der Note."""

        if not isinstance(status, BachelorarbeitsStatus):
            raise TypeError("Ungültiger Bachelorarbeitsstatus.")

        if (
            status == BachelorarbeitsStatus.BENOTET
            and self._note is None
        ):
            raise ValueError(
                "Der Status 'Benotet' erfordert eine Note."
            )

        if (
            status != BachelorarbeitsStatus.BENOTET
            and self._note is not None
        ):
            raise ValueError(
                "Entferne zuerst die Note, "
                "bevor du den Status änderst."
            )

        self._status = status


    def setzeTermine(
        self,
        anmeldedatum: date | None,
        fristablaufdatum: date | None,
        startdatum: date | None,
        abgabedatum: date | None,
    ) -> None:
        """Aktualisiert die Termine der Bachelorarbeit."""

        termine = [
            anmeldedatum,
            fristablaufdatum,
            startdatum,
            abgabedatum,
        ]

        if any(
            termin is not None and not isinstance(termin, date)
            for termin in termine
        ):
            raise TypeError(
                "Termine müssen Datumswerte oder None sein."
            )

        if (
            anmeldedatum is not None
            and startdatum is not None
            and startdatum < anmeldedatum
        ):
            raise ValueError(
                "Das Startdatum darf nicht vor "
                "dem Anmeldedatum liegen."
            )

        if (
            startdatum is not None
            and abgabedatum is not None
            and abgabedatum < startdatum
        ):
            raise ValueError(
                "Das Abgabedatum darf nicht vor "
                "dem Startdatum liegen."
            )

        self._anmeldedatum = anmeldedatum
        self._fristablaufdatum = fristablaufdatum
        self._startdatum = startdatum
        self._abgabedatum = abgabedatum

class Studium:
    """Verwaltet die Studienziele und die Modulhierarchie."""

    def __init__(
        self,
        studiengang: str,
        ziel_abschlussdatum: date,
        pruefungs_meilenstein: date,
        notenziel: Decimal,
    ):
        if not isinstance(studiengang, str) or not studiengang.strip():
            raise ValueError("Der Studiengang darf nicht leer sein.")

        if not isinstance(ziel_abschlussdatum, date):
            raise ValueError("Ungültiges Abschlussdatum.")

        if not isinstance(pruefungs_meilenstein, date):
            raise ValueError("Ungültiger Prüfungsmeilenstein.")

        if pruefungs_meilenstein > ziel_abschlussdatum:
            raise ValueError(
                "Der Prüfungsmeilenstein darf nicht nach "
                "dem Abschlussdatum liegen."
            )

        try:
            notenziel = Decimal(str(notenziel))
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError("Ungültiges Notenziel.")

        if not notenziel.is_finite() or not (
            Decimal("1.0") <= notenziel <= Decimal("5.0")
        ):
            raise ValueError(
                "Das Notenziel muss zwischen 1.0 und 5.0 liegen."
            )

        self._studiengang = studiengang
        self._zielAbschlussdatum = ziel_abschlussdatum
        self._pruefungsMeilenstein = pruefungs_meilenstein
        self._notenziel = notenziel

        self._topLevelModule = []
        self._bachelorarbeit = None

    
    def fuegeModulHinzu(self, modul: Modul) -> None:
        """Fügt ein Hauptmodul hinzu."""

        if not isinstance(modul, Modul):
            raise TypeError("Es muss ein Modul übergeben werden.")

        if modul._elternmodul is not None:
            raise ValueError(
                "Ein Untermodul darf nicht gleichzeitig "
                "als Hauptmodul geführt werden."
            )

        if getattr(modul, "_ist_top_level", False):
            raise ValueError(
                "Das Modul ist bereits als Hauptmodul zugeordnet."
            )

        self._topLevelModule.append(modul)
        modul._ist_top_level = True

    def ordneModulZu(
        self,
        modul: Modul,
        ziel: Uebermodul,
    ) -> None:
        """Ordnet ein Hauptmodul einem Übermodul zu."""

        if not isinstance(modul, Modul):
            raise TypeError("Ungültiges Modul.")

        if not isinstance(ziel, Uebermodul):
            raise TypeError("Das Ziel muss ein Übermodul sein.")

        if not any(
            hauptmodul is modul
            for hauptmodul in self._topLevelModule
        ):
            raise ValueError(
                "Nur Hauptmodule können neu zugeordnet werden."
            )

        if modul is ziel:
            raise ValueError(
                "Ein Übermodul kann sich nicht selbst enthalten."
            )

        if isinstance(modul, Uebermodul) and modul.enthaelt(ziel):
            raise ValueError(
                "Diese Zuordnung würde einen Zyklus erzeugen."
            )

        position = next(
            index
            for index, hauptmodul in enumerate(self._topLevelModule)
            if hauptmodul is modul
        )

        self._topLevelModule.pop(position)
        modul._ist_top_level = False

        try:
            ziel.fuegeUntermodulHinzu(modul)

        except Exception:
            self._topLevelModule.insert(position, modul)
            modul._ist_top_level = True
            raise

    
    def entferneModul(self, modul: Modul) -> None:
        """Entfernt ein Einzelmodul aus dem Studium."""

        if not isinstance(modul, Einzelmodul):
            raise TypeError(
                "Mit dieser Methode können nur Einzelmodule "
                "gelöscht werden."
            )

        # Fall 1: Modul liegt direkt im Studium
        if modul in self._topLevelModule:
            self._topLevelModule.remove(modul)
            modul._ist_top_level = False
            return

        # Fall 2: Modul gehört zu einem Übermodul
        elternmodul = modul._elternmodul

        if (
            elternmodul is not None
            and modul in elternmodul._untermodule
        ):
            # Prüfen, ob das Übermodul zu diesem Studium gehört
            def gehoert_zum_studium(aktuelles_modul):
                if aktuelles_modul in self._topLevelModule:
                    return True

                if aktuelles_modul._elternmodul is None:
                    return False

                return gehoert_zum_studium(
                    aktuelles_modul._elternmodul
                )

            if gehoert_zum_studium(elternmodul):
                elternmodul._untermodule.remove(modul)
                modul._elternmodul = None
                return

        raise ValueError(
            "Das Modul gehört nicht zu diesem Studium."
        )
    
    def entferneUebermodul(self, uebermodul: Uebermodul) -> None:
        """Entfernt ein Übermodul und erhält seine direkten Untermodule."""

        if not isinstance(uebermodul, Uebermodul):
            raise TypeError("Es muss ein Übermodul angegeben werden.")

        # Zunächst nur Haupt-Übermodule unterstützen
        if uebermodul not in self._topLevelModule:
            raise ValueError(
                "Nur Übermodule auf der obersten Ebene "
                "können gelöscht werden."
            )

        # Direkte Untermodule als eigenständige Hauptmodule übernehmen
        for untermodul in list(uebermodul._untermodule):
            uebermodul._untermodule.remove(untermodul)
            untermodul._elternmodul = None
            untermodul._ist_top_level = True
            self._topLevelModule.append(untermodul)

        # Leeres Übermodul entfernen
        self._topLevelModule.remove(uebermodul)
        uebermodul._ist_top_level = False


    def gibEinzelmodule(self) -> list[Einzelmodul]:
        """Ermittelt alle Einzelmodule aus der gesamten Hierarchie."""

        einzelmodule = []

        def durchlaufe(modul: Modul) -> None:
            if isinstance(modul, Einzelmodul):
                einzelmodule.append(modul)

            elif isinstance(modul, Uebermodul):
                for untermodul in modul._untermodule:
                    durchlaufe(untermodul)

        for modul in self._topLevelModule:
            durchlaufe(modul)

        return einzelmodule
    
    def berechneAktuellenNotendurchschnitt(self) -> Decimal | None:
        """Berechnet den ECTS-gewichteten Notendurchschnitt."""

        gewichtete_notensumme = Decimal("0")
        benotete_ects = 0

        for modul in self.gibEinzelmodule():
            pruefung = modul._pruefungsleistung

            if pruefung is None:
                continue

            if pruefung.bewertungsart != Bewertungsart.BENOTET:
                continue

            if pruefung.note is None:
                continue

            gewichtete_notensumme += (
                pruefung.note * modul.getEcts()
            )
            benotete_ects += modul.getEcts()

        if (
            self._bachelorarbeit is not None
            and self._bachelorarbeit.note is not None
        ):
            gewichtete_notensumme += (
                self._bachelorarbeit.note
                * self._bachelorarbeit.ects
            )
            benotete_ects += self._bachelorarbeit.ects

        if benotete_ects == 0:
            return None

        return gewichtete_notensumme / Decimal(benotete_ects)

    def berechneBenoetigtenNotendurchschnitt(self) -> "NotenzielErgebnis":
        """Berechnet die erforderliche Durchschnittsnote offener Leistungen."""

        bisherige_notensumme = Decimal("0")
        bisherige_ects = 0
        offene_ects = 0

        for modul in self.gibEinzelmodule():
            pruefung = modul._pruefungsleistung

            if pruefung is None:
                continue

            if pruefung.bewertungsart != Bewertungsart.BENOTET:
                continue

            ects = modul.getEcts()

            if pruefung.note is None:
                offene_ects += ects
            else:
                bisherige_notensumme += pruefung.note * ects
                bisherige_ects += ects

        if self._bachelorarbeit is not None:
            bachelorarbeit = self._bachelorarbeit

            if bachelorarbeit.note is None:
                offene_ects += bachelorarbeit.ects
            else:
                bisherige_notensumme += (
                    bachelorarbeit.note * bachelorarbeit.ects
                )
                bisherige_ects += bachelorarbeit.ects

        if offene_ects == 0:
            return NotenzielErgebnis(
                None,
                NotenzielStatus.KEINE_OFFENEN_LEISTUNGEN,
            )

        gesamte_ects = bisherige_ects + offene_ects

        benoetigter_durchschnitt = (
            self._notenziel * gesamte_ects - bisherige_notensumme
        ) / Decimal(offene_ects)

        if benoetigter_durchschnitt < Decimal("1.0"):
            return NotenzielErgebnis(
                benoetigter_durchschnitt,
                NotenzielStatus.NICHT_ERREICHBAR,
            )

        if benoetigter_durchschnitt >= Decimal("5.0"):
            return NotenzielErgebnis(
                benoetigter_durchschnitt,
                NotenzielStatus.BEREITS_GESICHERT,
            )

        return NotenzielErgebnis(
            benoetigter_durchschnitt,
            NotenzielStatus.BERECHNET,
        )


    
    def setzeBachelorarbeit(self, bachelorarbeit: Bachelorarbeit) -> None:
        """Ordnet eine Bachelorarbeit exklusiv einem Studium zu."""

        if not isinstance(bachelorarbeit, Bachelorarbeit):
            raise TypeError(
                "Es muss eine Bachelorarbeit übergeben werden."
            )

        if self._bachelorarbeit is not None:
            raise ValueError(
                "Diesem Studium ist bereits eine Bachelorarbeit zugeordnet."
            )

        if bachelorarbeit._studium is not None:
            raise ValueError(
                "Diese Bachelorarbeit gehört bereits zu einem Studium."
            )

        self._bachelorarbeit = bachelorarbeit
        bachelorarbeit._studium = self


class NotenzielErgebnis:
    """Speichert das Ergebnis der Notenzielberechnung."""

    def __init__(
        self,
        benoetigter_durchschnitt: Decimal | None,
        status: NotenzielStatus,
    ):
        if not isinstance(status, NotenzielStatus):
            raise ValueError("Ungültiger Notenzielstatus.")

        if benoetigter_durchschnitt is not None:
            try:
                benoetigter_durchschnitt = Decimal(
                    str(benoetigter_durchschnitt)
                )
            except (ValueError, TypeError, InvalidOperation):
                raise ValueError("Ungültiger Durchschnitt.")

            if not benoetigter_durchschnitt.is_finite():
                raise ValueError("Der Durchschnitt muss endlich sein.")

        self._benoetigterDurchschnitt = benoetigter_durchschnitt
        self._status = status

    @property
    def benoetigterDurchschnitt(self) -> Decimal | None:
        return self._benoetigterDurchschnitt

    @property
    def status(self) -> NotenzielStatus:
        return self._status


from enum import Enum


class Modulart(Enum):
    """Unterscheidet Pflicht- und Wahlpflichtmodule."""
    PFLICHT = "Pflicht"
    WAHLPFLICHT = "Wahlpflicht"


class Pruefungsart(Enum):
    """Legt die Art einer Prüfungsleistung fest."""
    KLAUSUR = "Klausur"
    PORTFOLIO = "Portfolio"
    PROJEKTBERICHT = "Projektbericht"
    MODULKLAUSUR = "Modulklausur"
    ADVANCED_WORKBOOK = "Advanced Workbook"
    FALLSTUDIE = "Fallstudie"
    SEMINARARBEIT = "Seminararbeit"


class Status(Enum):
    """Beschreibt den Bearbeitungsstand einer Prüfungsleistung."""
    NOCH_NICHT_BEGONNEN = "Noch nicht begonnen"
    IN_BEARBEITUNG = "In Bearbeitung"
    EINGEREICHT = "Eingereicht"
    ABGESCHLOSSEN = "Abgeschlossen"


class BachelorarbeitsStatus(Enum):
    """Beschreibt den Fortschritt der Bachelorarbeit."""
    NOCH_NICHT_BEGONNEN = "Noch nicht begonnen"
    ANGEMELDET = "Angemeldet"
    IN_BEARBEITUNG = "In Bearbeitung"
    EINGEREICHT = "Eingereicht"
    BENOTET = "Benotet"


class Bewertungsart(Enum):
    """Unterscheidet benotete und unbenotete Leistungen."""
    BENOTET = "Benotet"
    UNBENOTET = "Unbenotet"


class Pruefungsergebnis(Enum):
    """Beschreibt das Ergebnis einer Prüfungsleistung."""
    BESTANDEN = "Bestanden"
    NICHT_BESTANDEN = "Nicht bestanden"


class NotenzielStatus(Enum):
    """Beschreibt das Ergebnis der Notenzielberechnung."""
    BERECHNET = "Berechnet"
    KEINE_OFFENEN_LEISTUNGEN = "Keine offenen Leistungen"
    NICHT_ERREICHBAR = "Nicht erreichbar"
    BEREITS_GESICHERT = "Bereits gesichert"

from enum import Enum


class Modulart(Enum):
    PFLICHT = "Pflicht"
    WAHLPFLICHT = "Wahlpflicht"


class Bewertungsart(Enum):
    BENOTET = "Benotet"
    UNBENOTET = "Unbenotet"


class Status(Enum):
    NOCH_NICHT_BEGONNEN = "Noch nicht begonnen"
    IN_BEARBEITUNG = "In Bearbeitung"
    EINGEREICHT = "Eingereicht"
    ABGESCHLOSSEN = "Abgeschlossen"


class Pruefungsergebnis(Enum):
    BESTANDEN = "Bestanden"
    NICHT_BESTANDEN = "Nicht bestanden"


class Pruefungsleistung:
    def __init__(
        self,
        bewertungsart: Bewertungsart,
        status: Status,
        ergebnis: Pruefungsergebnis | None = None
    ):
        self.bewertungsart = bewertungsart
        self.status = status
        self.ergebnis = ergebnis


pruefung = Pruefungsleistung(
    Bewertungsart.UNBENOTET,
    Status.ABGESCHLOSSEN,
    Pruefungsergebnis.BESTANDEN
)

print("Bewertungsart:", pruefung.bewertungsart.value)
print("Status:", pruefung.status.value)
print("Ergebnis:", pruefung.ergebnis.value)

print(
    "Ist die Prüfungsleistung unbenotet?",
    pruefung.bewertungsart == Bewertungsart.UNBENOTET
)

print(
    "Ist die Prüfungsleistung bestanden?",
    pruefung.ergebnis == Pruefungsergebnis.BESTANDEN
)
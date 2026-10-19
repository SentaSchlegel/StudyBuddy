
from enum import Enum


class Bewertungsart(Enum):
    BENOTET = "Benotet"
    UNBENOTET = "Unbenotet"


class Pruefungsergebnis(Enum):
    BESTANDEN = "Bestanden"
    NICHT_BESTANDEN = "Nicht bestanden"


class Pruefungsleistung:
    def __init__(self, bewertungsart):
        self._bewertungsart = bewertungsart
        self._note = None
        self._ergebnis = None

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, wert):
        if wert is not None:
            if self._bewertungsart == Bewertungsart.UNBENOTET:
                raise ValueError(
                    "Unbenotete Leistungen dürfen keine Note haben."
                )

            if not isinstance(wert, (int, float)) or isinstance(wert, bool):
                raise ValueError("Die Note muss eine Zahl sein.")

            if not 1.0 <= wert <= 5.0:
                raise ValueError("Die Note muss zwischen 1.0 und 5.0 liegen.")

            if (
                self._ergebnis == Pruefungsergebnis.BESTANDEN
                and wert > 4.0
            ):
                raise ValueError(
                    "Eine nicht bestandene Note kann nicht als bestanden gelten."
                )

            if (
                self._ergebnis == Pruefungsergebnis.NICHT_BESTANDEN
                and wert <= 4.0
            ):
                raise ValueError(
                    "Eine bestandene Note kann nicht als nicht bestanden gelten."
                )

        self._note = wert

    @property
    def ergebnis(self):
        return self._ergebnis

    @ergebnis.setter
    def ergebnis(self, wert):
        if wert is not None and not isinstance(wert, Pruefungsergebnis):
            raise ValueError("Ungültiges Prüfungsergebnis.")

        if self._bewertungsart == Bewertungsart.BENOTET and wert is not None:
            if self._note is None:
                raise ValueError("Für das Ergebnis fehlt eine Note.")

            if (
                wert == Pruefungsergebnis.BESTANDEN
                and self._note > 4.0
            ) or (
                wert == Pruefungsergebnis.NICHT_BESTANDEN
                and self._note <= 4.0
            ):
                raise ValueError("Note und Prüfungsergebnis widersprechen sich.")

        self._ergebnis = wert


# TEST 1: Gültige benotete Prüfungsleistung
pruefung = Pruefungsleistung(Bewertungsart.BENOTET)
pruefung.note = 2.0
pruefung.ergebnis = Pruefungsergebnis.BESTANDEN

print("Gültige Note:", pruefung.note)
print("Gültiges Ergebnis:", pruefung.ergebnis.value)


# TEST 2: Ungültige Note
try:
    pruefung.note = 6.0
except ValueError as fehler:
    print("Ungültige Note verhindert:", fehler)


# TEST 3: Unbenotete Leistung mit Note
unbenotet = Pruefungsleistung(Bewertungsart.UNBENOTET)

try:
    unbenotet.note = 2.0
except ValueError as fehler:
    print("Widerspruch verhindert:", fehler)


# TEST 4: Widersprüchliches Prüfungsergebnis
try:
    pruefung.ergebnis = Pruefungsergebnis.NICHT_BESTANDEN
except ValueError as fehler:
    print("Widersprüchliches Ergebnis verhindert:", fehler)


# TEST 5: Gültige unbenotete Leistung
unbenotet.ergebnis = Pruefungsergebnis.BESTANDEN
print("Unbenotetes Ergebnis:", unbenotet.ergebnis.value)

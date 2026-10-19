
from decimal import Decimal

from studybuddy.modelle import Bachelorarbeit
from studybuddy.enums import BachelorarbeitsStatus


def test_bachelorarbeit_note_status():
    arbeit = Bachelorarbeit(ects=10)

    # Ohne Note darf der Status nicht "Benotet" sein.
    try:
        arbeit.setzeStatus(BachelorarbeitsStatus.BENOTET)
        assert False, "Ein ValueError wurde erwartet."
    except ValueError:
        pass

    # Eine Note setzt den Status automatisch.
    arbeit.setzeNote(Decimal("1.7"))

    assert arbeit.note == Decimal("1.7")
    assert arbeit._status == BachelorarbeitsStatus.BENOTET

    # Entfernen der Note setzt den Status zurück.
    arbeit.setzeNote(None)

    assert arbeit.note is None
    assert arbeit._status == BachelorarbeitsStatus.EINGEREICHT

    print("Alle Bachelorarbeits-Notentests erfolgreich!")


if __name__ == "__main__":
    test_bachelorarbeit_note_status()

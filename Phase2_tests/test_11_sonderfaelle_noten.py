
from decimal import Decimal


class Studium:
    def __init__(self, notenziel):
        self.notenziel = Decimal(str(notenziel))
        self.leistungen = []

    def fuege_leistung_hinzu(self, note, ects):
        if ects <= 0:
            raise ValueError("ECTS müssen positiv sein.")

        self.leistungen.append({
            "note": None if note is None else Decimal(str(note)),
            "ects": ects
        })

    def berechne_aktuellen_durchschnitt(self):
        benotete = [
            leistung for leistung in self.leistungen
            if leistung["note"] is not None
        ]

        if not benotete:
            return None

        gewichtete_summe = sum(
            leistung["note"] * leistung["ects"]
            for leistung in benotete
        )
        ects_summe = sum(leistung["ects"] for leistung in benotete)

        return gewichtete_summe / ects_summe

    def berechne_benoetigten_durchschnitt(self):
        benotete = [
            leistung for leistung in self.leistungen
            if leistung["note"] is not None
        ]
        offene = [
            leistung for leistung in self.leistungen
            if leistung["note"] is None
        ]

        if not offene:
            return None, "Keine offenen benoteten Leistungen"

        bisherige_summe = sum(
            leistung["note"] * leistung["ects"]
            for leistung in benotete
        )
        bisherige_ects = sum(leistung["ects"] for leistung in benotete)
        offene_ects = sum(leistung["ects"] for leistung in offene)

        gesamt_ects = bisherige_ects + offene_ects

        benoetigt = (
            self.notenziel * gesamt_ects - bisherige_summe
        ) / offene_ects

        if benoetigt < Decimal("1.0"):
            return None, "Notenziel rechnerisch nicht mehr erreichbar"

        if benoetigt > Decimal("5.0"):
            return None, "Notenziel bereits sicher erreicht"

        return benoetigt, "Berechnung erfolgreich"


# TEST 1: Noch keine Noten
studium_1 = Studium("2.5")
studium_1.fuege_leistung_hinzu(None, 5)

print(
    "Keine vorhandenen Noten:",
    studium_1.berechne_aktuellen_durchschnitt()
)


# TEST 2: Keine offenen benoteten Leistungen
studium_2 = Studium("2.5")
studium_2.fuege_leistung_hinzu("2.0", 5)

print(
    "Keine offenen Leistungen:",
    studium_2.berechne_benoetigten_durchschnitt()
)


# TEST 3: Notenziel nicht mehr erreichbar
studium_3 = Studium("1.5")
studium_3.fuege_leistung_hinzu("4.0", 20)
studium_3.fuege_leistung_hinzu(None, 5)

print(
    "Notenziel nicht erreichbar:",
    studium_3.berechne_benoetigten_durchschnitt()
)


# TEST 4: Normale Berechnung
studium_4 = Studium("2.5")
studium_4.fuege_leistung_hinzu("2.0", 10)
studium_4.fuege_leistung_hinzu(None, 10)

print(
    "Normale Berechnung:",
    studium_4.berechne_benoetigten_durchschnitt()
)

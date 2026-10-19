class BenoteteLeistung:
    def __init__(self, name, ects, note=None):
        self.name = name
        self.ects = ects
        self.note = note


class Studium:
    def __init__(self, notenziel):
        self.notenziel = notenziel
        self.leistungen = []

    def fuege_leistung_hinzu(self, leistung):
        self.leistungen.append(leistung)

    def berechne_aktuellen_notendurchschnitt(self):
        benotete_leistungen = [
            leistung
            for leistung in self.leistungen
            if leistung.note is not None
        ]

        gewichtete_notensumme = sum(
            leistung.note * leistung.ects
            for leistung in benotete_leistungen
        )

        benotete_ects = sum(
            leistung.ects
            for leistung in benotete_leistungen
        )

        if benotete_ects == 0:
            return None

        return gewichtete_notensumme / benotete_ects


studium = Studium(2.5)

studium.fuege_leistung_hinzu(
    BenoteteLeistung("Modul A", 5, 2.0)
)

studium.fuege_leistung_hinzu(
    BenoteteLeistung("Modul B", 5, 3.0)
)

studium.fuege_leistung_hinzu(
    BenoteteLeistung("Bachelorarbeit", 10, 1.5)
)

durchschnitt = studium.berechne_aktuellen_notendurchschnitt()

print("Aktueller Notendurchschnitt:", durchschnitt)
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

    def berechne_benoetigten_notendurchschnitt(self):
        benotete_leistungen = [
            leistung
            for leistung in self.leistungen
            if leistung.note is not None
        ]

        offene_leistungen = [
            leistung
            for leistung in self.leistungen
            if leistung.note is None
        ]

        aktuelle_notensumme = sum(
            leistung.note * leistung.ects
            for leistung in benotete_leistungen
        )

        offene_ects = sum(
            leistung.ects
            for leistung in offene_leistungen
        )

        gesamte_ects = sum(
            leistung.ects
            for leistung in self.leistungen
        )

        benoetigte_notensumme = (
            self.notenziel * gesamte_ects
            - aktuelle_notensumme
        )

        if offene_ects == 0:
            return None

        return benoetigte_notensumme / offene_ects


studium = Studium(2.5)

studium.fuege_leistung_hinzu(
    BenoteteLeistung("Modul A", 5, 2.0)
)

studium.fuege_leistung_hinzu(
    BenoteteLeistung("Modul B", 5, 3.0)
)

studium.fuege_leistung_hinzu(
    BenoteteLeistung("Modul C", 5)
)

studium.fuege_leistung_hinzu(
    BenoteteLeistung("Bachelorarbeit", 10)
)

benoetigter_durchschnitt = (
    studium.berechne_benoetigten_notendurchschnitt()
)

print(
    "Benötigter Durchschnitt für offene Leistungen:",
    round(benoetigter_durchschnitt, 2)
)
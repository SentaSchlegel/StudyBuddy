class Pruefungsleistung:
    def __init__(self, pruefungsart, status):
        self.pruefungsart = pruefungsart
        self.status = status


class Einzelmodul:
    def __init__(self, modulname, ects, pruefungsleistung):
        self.modulname = modulname
        self.ects = ects
        self.pruefungsleistung = pruefungsleistung


pruefung = Pruefungsleistung(
    "Portfolio",
    "In Bearbeitung"
)

modul = Einzelmodul(
    "Objektorientierte und funktionale Programmierung",
    5,
    pruefung
)

print("Modul:", modul.modulname)
print("ECTS:", modul.ects)
print("Prüfungsart:", modul.pruefungsleistung.pruefungsart)
print("Status:", modul.pruefungsleistung.status)

print(
    "Gehört die Prüfungsleistung zum Modul?",
    modul.pruefungsleistung is pruefung
)
class Modul:
    def __init__(self, modulname):
        self.modulname = modulname


class Uebermodul(Modul):
    def __init__(self, modulname):
        super().__init__(modulname)


class Einzelmodul(Modul):
    def __init__(self, modulname, ects, modulart):
        super().__init__(modulname)
        self.ects = ects
        self.modulart = modulart


uebermodul = Uebermodul("Wahlpflichtbereich A")

einzelmodul = Einzelmodul(
    "Objektorientierte und funktionale Programmierung",
    5,
    "PFLICHT"
)


print("Übermodul:", uebermodul.modulname)

print("Einzelmodul:", einzelmodul.modulname)
print("ECTS:", einzelmodul.ects)
print("Modulart:", einzelmodul.modulart)

print(
    "Einzelmodul ist ein Modul:",
    isinstance(einzelmodul, Modul)
)

print(
    "Übermodul ist ein Modul:",
    isinstance(uebermodul, Modul)
)
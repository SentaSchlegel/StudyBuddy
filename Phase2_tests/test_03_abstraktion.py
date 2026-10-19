from abc import ABC, abstractmethod


class Modul(ABC):
    def __init__(self, modulname):
        self.modulname = modulname

    @abstractmethod
    def get_ects(self):
        pass


class Uebermodul(Modul):
    def __init__(self, modulname, untermodule):
        super().__init__(modulname)
        self.untermodule = untermodule

    def get_ects(self):
        return sum(modul.get_ects() for modul in self.untermodule)


class Einzelmodul(Modul):
    def __init__(self, modulname, ects):
        super().__init__(modulname)
        self.ects = ects

    def get_ects(self):
        return self.ects


einzelmodul_1 = Einzelmodul("Modul A", 5)
einzelmodul_2 = Einzelmodul("Modul B", 5)

uebermodul = Uebermodul(
    "Wahlpflichtbereich",
    [einzelmodul_1, einzelmodul_2]
)

print("ECTS Einzelmodul:", einzelmodul_1.get_ects())
print("ECTS Übermodul:", uebermodul.get_ects())


try:
    modul = Modul("Direktes Modul")
except TypeError as fehler:
    print("Direkte Instanziierung verhindert:", fehler)
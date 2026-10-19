class Modul:
    def __init__(self, modulname):
        self.modulname = modulname


class Einzelmodul(Modul):
    def __init__(self, modulname, ects):
        super().__init__(modulname)
        self.ects = ects


class Uebermodul(Modul):
    def __init__(self, modulname):
        super().__init__(modulname)
        self.untermodule = []

    def enthaelt_modul(self, gesuchtes_modul):
        if self is gesuchtes_modul:
            return True

        for modul in self.untermodule:
            if modul is gesuchtes_modul:
                return True

            if isinstance(modul, Uebermodul):
                if modul.enthaelt_modul(gesuchtes_modul):
                    return True

        return False

    def fuege_untermodul_hinzu(self, modul):
        # Das Modul darf sich nicht selbst enthalten.
        if modul is self:
            raise ValueError(
                "Ein Übermodul darf sich nicht selbst enthalten."
            )

        # Auch indirekte Zyklen werden verhindert.
        if isinstance(modul, Uebermodul):
            if modul.enthaelt_modul(self):
                raise ValueError(
                    "Zyklische Modulzuordnung ist nicht erlaubt."
                )

        self.untermodule.append(modul)


wahlpflichtbereich = Uebermodul("Wahlpflichtbereich")
unterbereich = Uebermodul("Unterbereich")
einzelmodul = Einzelmodul("Data Analytics", 5)

wahlpflichtbereich.fuege_untermodul_hinzu(unterbereich)
unterbereich.fuege_untermodul_hinzu(einzelmodul)

print(
    "Normale Verschachtelung:",
    wahlpflichtbereich.untermodule[0].modulname
)

print(
    "Untermodul:",
    unterbereich.untermodule[0].modulname
)


try:
    unterbereich.fuege_untermodul_hinzu(wahlpflichtbereich)
except ValueError as fehler:
    print("Zyklus verhindert:", fehler)


try:
    wahlpflichtbereich.fuege_untermodul_hinzu(wahlpflichtbereich)
except ValueError as fehler:
    print("Selbstzuordnung verhindert:", fehler)
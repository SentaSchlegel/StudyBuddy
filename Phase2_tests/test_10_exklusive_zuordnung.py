
class Modul:
    def __init__(self, modulname):
        self.modulname = modulname
        self._elternmodul = None


class Uebermodul(Modul):
    def __init__(self, modulname):
        super().__init__(modulname)
        self.untermodule = []

    def enthaelt(self, gesuchtes_modul):
        for modul in self.untermodule:
            if modul is gesuchtes_modul:
                return True
            if isinstance(modul, Uebermodul):
                if modul.enthaelt(gesuchtes_modul):
                    return True
        return False

    def fuege_untermodul_hinzu(self, modul):
        if modul is self:
            raise ValueError("Ein Übermodul darf sich nicht selbst enthalten.")

        if modul._elternmodul is not None:
            raise ValueError(
                "Das Modul gehört bereits zu einem anderen Übermodul."
            )

        if isinstance(modul, Uebermodul) and modul.enthaelt(self):
            raise ValueError("Zyklische Modulzuordnung ist nicht erlaubt.")

        self.untermodule.append(modul)
        modul._elternmodul = self


class Pruefungsleistung:
    def __init__(self, pruefungsart):
        self.pruefungsart = pruefungsart
        self._einzelmodul = None


class Einzelmodul(Modul):
    def __init__(self, modulname):
        super().__init__(modulname)
        self.pruefungsleistung = None

    def setze_pruefungsleistung(self, pruefung):
        if pruefung._einzelmodul is not None and pruefung._einzelmodul is not self:
            raise ValueError(
                "Die Prüfungsleistung gehört bereits zu einem anderen Einzelmodul."
            )

        if self.pruefungsleistung is not None and self.pruefungsleistung is not pruefung:
            raise ValueError(
                "Das Einzelmodul besitzt bereits eine Prüfungsleistung."
            )

        self.pruefungsleistung = pruefung
        pruefung._einzelmodul = self


# TEST 1: Gültige Modulzuordnung
bereich_a = Uebermodul("Wahlpflichtbereich A")
bereich_b = Uebermodul("Wahlpflichtbereich B")
modul = Einzelmodul("Data Analytics")

bereich_a.fuege_untermodul_hinzu(modul)
print("Gültige Modulzuordnung:", modul.modulname)


# TEST 2: Doppelte Modulzuordnung
try:
    bereich_b.fuege_untermodul_hinzu(modul)
except ValueError as fehler:
    print("Doppelte Modulzuordnung verhindert:", fehler)


# TEST 3: Zyklus verhindern
unterbereich = Uebermodul("Unterbereich")
bereich_a.fuege_untermodul_hinzu(unterbereich)

try:
    unterbereich.fuege_untermodul_hinzu(bereich_a)
except ValueError as fehler:
    print("Zyklus verhindert:", fehler)


# TEST 4: Gültige Prüfungszuordnung
pruefung = Pruefungsleistung("Portfolio")
einzelmodul_a = Einzelmodul("Python")
einzelmodul_b = Einzelmodul("Datenbanken")

einzelmodul_a.setze_pruefungsleistung(pruefung)
print("Gültige Prüfungszuordnung:", pruefung.pruefungsart)


# TEST 5: Doppelte Prüfungszuordnung
try:
    einzelmodul_b.setze_pruefungsleistung(pruefung)
except ValueError as fehler:
    print("Doppelte Prüfungszuordnung verhindert:", fehler)

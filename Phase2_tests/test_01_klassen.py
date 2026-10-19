class Studium:
    def __init__(
        self,
        studiengang,
        ziel_abschlussdatum,
        pruefungs_meilenstein,
        notenziel
    ):
        self.studiengang = studiengang
        self.ziel_abschlussdatum = ziel_abschlussdatum
        self.pruefungs_meilenstein = pruefungs_meilenstein
        self.notenziel = notenziel


studium = Studium(
    "Wirtschaftsinformatik",
    "31.03.2027",
    "16.12.2026",
    2.5
)

print("Studiengang:", studium.studiengang)
print("Ziel Abschluss:", studium.ziel_abschlussdatum)
print("Prüfungsmeilenstein:", studium.pruefungs_meilenstein)
print("Notenziel:", studium.notenziel)
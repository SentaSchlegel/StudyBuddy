import streamlit as st
from datetime import date
from decimal import Decimal


from studybuddy.modelle import (
    Studium,
    Einzelmodul,
    Uebermodul,
    Pruefungsleistung,
    Bachelorarbeit,
)

from studybuddy.enums import (
    Modulart,
    Pruefungsart,
    Bewertungsart,
    Status,
    Pruefungsergebnis,
    BachelorarbeitsStatus,
)



class StudyBuddyView:
    """Stellt die Studiendaten in Streamlit dar."""

    def __init__(self, studium: Studium, repository):
        self._studium = studium
        self._repository = repository

    def zeigeDashboard(self) -> None:
        """Zeigt Studienfortschritt, Notendurchschnitt und anstehende Prüfungen."""
        st.title("🎓 StudyBuddy")
        st.subheader("Mein Studienfortschritt")

        st.write(f"Studiengang: {self._studium._studiengang}")

        aktueller_schnitt = (
            self._studium.berechneAktuellenNotendurchschnitt()
        )

        notenziel_ergebnis = (
            self._studium.berechneBenoetigtenNotendurchschnitt()
        )

        spalte1, spalte2 = st.columns(2)

        with spalte1:
            st.metric(
                "Aktueller Notendurchschnitt",
                (
                    f"{aktueller_schnitt:.2f}"
                    if aktueller_schnitt is not None
                    else "Noch keine Noten"
                ),
            )

        with spalte2:
            benoetigt = (
                notenziel_ergebnis.benoetigterDurchschnitt
            )

            st.metric(
                "Benötigter Notendurchschnitt",
                (
                    f"{benoetigt:.2f}"
                    if benoetigt is not None
                    else "Keine offenen Leistungen"
                ),
            )

        st.caption(
            f"Notenzielstatus: {notenziel_ergebnis.status.name}"
        )

        st.divider()

        st.subheader("Studienübersicht")


        
        # Alle Einzelmodule ermitteln
        module = self._studium.gibEinzelmodule()

        anzahl_module = len(module)

        abgeschlossene_module = sum(
            1
            for modul in module
            if (
                modul._pruefungsleistung is not None
                and modul._pruefungsleistung._status
                == Status.ABGESCHLOSSEN
            )
        )

        # Bachelorarbeit als eine zusätzliche Leistung zählen
        bachelorarbeit = self._studium._bachelorarbeit

        anzahl_leistungen = anzahl_module
        abgeschlossene_leistungen = abgeschlossene_module

        if bachelorarbeit is not None:
            anzahl_leistungen += 1

            if bachelorarbeit._status == BachelorarbeitsStatus.BENOTET:
                abgeschlossene_leistungen += 1

        offene_leistungen = (
            anzahl_leistungen - abgeschlossene_leistungen
        )

        fortschritt = (
            abgeschlossene_leistungen / anzahl_leistungen
            if anzahl_leistungen > 0
            else 0.0
        )


        spalte1, spalte2, spalte3 = st.columns(3)

        with spalte1:
            st.metric("Leistungen gesamt", anzahl_leistungen)

        with spalte2:
            st.metric("Abgeschlossen", abgeschlossene_leistungen)

        with spalte3:
            st.metric("Offen", offene_leistungen)

        st.write("**Fortschritt der erfassten Leistungen**")

        st.progress(
            fortschritt,
            text=f"{fortschritt * 100:.0f} % abgeschlossen",
        )

        st.subheader("Statusverteilung")

       
        status_anzahlen = {
            status.value: 0
            for status in Status
        }

        # Status der Einzelmodule zählen
        for modul in module:
            pruefung = modul._pruefungsleistung

            if pruefung is None:
                status_anzahlen[Status.NOCH_NICHT_BEGONNEN.value] += 1
            else:
                status_anzahlen[pruefung._status.value] += 1

        
        # Bachelorarbeit als zusätzliche Leistung zählen
        if bachelorarbeit is not None:
            if bachelorarbeit._status == BachelorarbeitsStatus.BENOTET:
                status_name = Status.ABGESCHLOSSEN.value

            elif bachelorarbeit._status == BachelorarbeitsStatus.EINGEREICHT:
                status_name = Status.EINGEREICHT.value

            elif bachelorarbeit._status in (
                BachelorarbeitsStatus.ANGEMELDET,
                BachelorarbeitsStatus.IN_BEARBEITUNG,
            ):
                status_name = Status.IN_BEARBEITUNG.value

            else:
                status_name = Status.NOCH_NICHT_BEGONNEN.value

            status_anzahlen[status_name] += 1

        # Nur tatsächlich vorkommende Status anzeigen
        status_anzahlen = {
            status: anzahl
            for status, anzahl in status_anzahlen.items()
            if anzahl > 0
        }


        if status_anzahlen:
            st.vega_lite_chart(
                {
                    "data": {
                        "values": [
                            {"Status": status, "Anzahl": anzahl}
                            for status, anzahl in status_anzahlen.items()
                        ]
                    },
                    "mark": {"type": "arc", "innerRadius": 55},
                    "encoding": {
                        "theta": {
                            "field": "Anzahl",
                            "type": "quantitative",
                        },
                        "color": {
                            "field": "Status",
                            "type": "nominal",
                        },
                        "tooltip": [
                            {"field": "Status", "type": "nominal"},
                            {"field": "Anzahl", "type": "quantitative"},
                        ],
                    },
                },
                use_container_width=True,
            )
        else:
            st.info("Noch keine Module für die Statusverteilung vorhanden.")

        st.write(
            f"Geplantes Abschlussdatum: "
            f"{self._studium._zielAbschlussdatum:%d.%m.%Y}"
        )

        st.divider()
        st.subheader("Nächste Prüfungen")

        # Alle offenen Prüfungen mit geplantem Datum sammeln
        naechste_pruefungen = []

        for modul in self._studium.gibEinzelmodule():
            pruefung = modul._pruefungsleistung

            if pruefung is None:
                continue

            if pruefung._status == Status.ABGESCHLOSSEN:
                continue

            if pruefung._geplantes_pruefungsdatum is None:
                continue

            naechste_pruefungen.append(
                (
                    pruefung._geplantes_pruefungsdatum,
                    modul.modulname,
                    pruefung._pruefungsart.value,
                    pruefung._status.value,
                )
            )

        # Bachelorarbeit bei den anstehenden Terminen berücksichtigen
        bachelorarbeit = self._studium._bachelorarbeit

        if (
            bachelorarbeit is not None
            and bachelorarbeit._fristablaufdatum is not None
            and bachelorarbeit._abgabedatum is None
            and bachelorarbeit._status
            not in (
                BachelorarbeitsStatus.EINGEREICHT,
                BachelorarbeitsStatus.BENOTET,
            )
        ):
            naechste_pruefungen.append(
                (
                    bachelorarbeit._fristablaufdatum,
                    "Bachelorarbeit",
                    "Abgabefrist",
                    bachelorarbeit._status.value,
                )
            )

        # Früheste Prüfung zuerst
        naechste_pruefungen.sort(key=lambda eintrag: eintrag[0])

        if not naechste_pruefungen:
            st.info("Keine anstehenden Prüfungen eingetragen.")

        else:
            for datum, modulname, pruefungsart, status in naechste_pruefungen:
                with st.container(border=True):
                    st.write(f"**{modulname}**")
                    st.write(f"Prüfungsart: {pruefungsart}")
                    st.write(f"Datum: {datum:%d.%m.%Y}")
                    st.caption(f"Status: {status}")

    
    def zeigeModule(self) -> None:
        """Ermöglicht die Verwaltung und hierarchische Zuordnung von Modulen."""
        st.header("Meine Module")

        st.subheader("Neues Modul hinzufügen")

        with st.form("neues_modul"):
            modulname = st.text_input("Modulname")

            modulart = st.selectbox(
                "Modulart",
                options=list(Modulart),
                format_func=lambda art: art.value,
            )

            ects = st.number_input(
                "ECTS",
                min_value=1,
                max_value=30,
                value=5,
                step=1,
            )

            pruefungsart = st.selectbox(
                "Prüfungsart",
                options=list(Pruefungsart),
                format_func=lambda art: art.value,
            )

            bewertungsart = st.selectbox(
                "Bewertungsart",
                options=list(Bewertungsart),
                format_func=lambda art: art.value,
            )

            speichern = st.form_submit_button(
                "Modul speichern",
                type="primary",
            )

        if speichern:
            try:
                modul = Einzelmodul(
                    modulname,
                    modulart,
                    int(ects),
                )

                pruefung = Pruefungsleistung(
                    pruefungsart,
                    bewertungsart,
                )

                modul.setzePruefungsleistung(pruefung)
                self._studium.fuegeModulHinzu(modul)

                self._repository.speichereStudium(
                    self._studium
                )

                st.success(
                    f"Modul '{modulname}' wurde gespeichert!"
                )

                st.rerun()

            except ValueError as fehler:
                st.error(str(fehler))

        st.divider()
        
        st.subheader("Neues Übermodul hinzufügen")

        with st.form("neues_uebermodul"):
            name_uebermodul = st.text_input(
                "Name des Übermoduls"
            )

            uebermodul_speichern = st.form_submit_button(
                "Übermodul speichern"
            )

        if uebermodul_speichern:
            try:
                uebermodul = Uebermodul(name_uebermodul)

                self._studium.fuegeModulHinzu(uebermodul)

                self._repository.speichereStudium(
                    self._studium
                )

                st.rerun()

            except ValueError as fehler:
                st.error(str(fehler))

        st.divider()

        st.subheader("Vorhandene Module")

        module = self._studium.gibEinzelmodule()

        if not module:
            st.info("Noch keine Module vorhanden.")

        else:
            for modul in module:
                with st.container(border=True):
                    st.write(f"**{modul.modulname}**")
                    st.write(f"ECTS: {modul.getEcts()}")
                    st.write(
                        f"Modulart: {modul._modulart.value}"
                    )

        st.subheader("Übermodule")

        uebermodule = [
            modul
            for modul in self._studium._topLevelModule
            if isinstance(modul, Uebermodul)
        ]

        if not uebermodule:
            st.info("Noch keine Übermodule vorhanden.")

        for modul in uebermodule:
            with st.container(border=True):
                st.write(f"**{modul.modulname}**")
                st.write(f"ECTS gesamt: {modul.getEcts()}")

        st.divider()

        st.subheader("Modulstruktur")

        def zeige_modulbaum(modul, ebene=0):
            einrueckung = "　" * ebene

            if isinstance(modul, Uebermodul):
                st.write(
                    f"{einrueckung}📁 **{modul.modulname}** "
                    f"({modul.getEcts()} ECTS)"
                )

                for untermodul in modul._untermodule:
                    zeige_modulbaum(untermodul, ebene + 1)

            else:
                st.write(
                    f"{einrueckung}📄 {modul.modulname} "
                    f"({modul.getEcts()} ECTS)"
                )

        for hauptmodul in self._studium._topLevelModule:
            zeige_modulbaum(hauptmodul)

        st.divider()

        st.subheader("Module zuordnen")

        alle_module = []

        def sammle_module(modul):
            alle_module.append(modul)

            if isinstance(modul, Uebermodul):
                for untermodul in modul._untermodule:
                    sammle_module(untermodul)

        for hauptmodul in self._studium._topLevelModule:
            sammle_module(hauptmodul)

        uebermodule = [
            modul
            for modul in alle_module
            if isinstance(modul, Uebermodul)
        ]

        freie_module = [
            modul
            for modul in self._studium._topLevelModule
            if modul not in uebermodule
        ]

        if not uebermodule or not freie_module:
            st.info("Keine passenden Module zur Zuordnung vorhanden.")

        else:
            
            with st.form("module_zuordnen"):
                ziel_index = st.selectbox(
                    "Übermodul auswählen",
                    options=range(len(uebermodule)),
                    format_func=lambda i: uebermodule[i].modulname,
                )

                quelle_index = st.selectbox(
                    "Modul zuordnen",
                    options=range(len(freie_module)),
                    format_func=lambda i: freie_module[i].modulname,
                )

                zuordnen = st.form_submit_button(
                    "Modul zuordnen"
                )

            if zuordnen:
                try:
                    # Immer Objekte aus dem aktuellen Studium verwenden
                    ziel = uebermodule[ziel_index]
                    quelle = freie_module[quelle_index]

                    self._studium.ordneModulZu(
                        quelle,
                        ziel,
                    )

                    self._repository.speichereStudium(
                        self._studium
                    )

                    st.rerun()

                except (ValueError, TypeError) as fehler:
                    st.error(str(fehler))


        st.divider()
        st.subheader("Übermodul bearbeiten")

        bearbeitbare_uebermodule = []

        def sammle_uebermodule(modul):
            if isinstance(modul, Uebermodul):
                bearbeitbare_uebermodule.append(modul)

                for untermodul in modul._untermodule:
                    sammle_uebermodule(untermodul)

        for hauptmodul in self._studium._topLevelModule:
            sammle_uebermodule(hauptmodul)

        if not bearbeitbare_uebermodule:
            st.info("Keine Übermodule zum Bearbeiten vorhanden.")

        else:
            uebermodul_index = st.selectbox(
                "Welches Übermodul möchtest du bearbeiten?",
                options=range(len(bearbeitbare_uebermodule)),
                format_func=lambda i: (
                    bearbeitbare_uebermodule[i].modulname
                ),
                key="uebermodul_bearbeiten_auswahl",
            )

            uebermodul = bearbeitbare_uebermodule[uebermodul_index]

            with st.form("uebermodul_bearbeiten"):
                neuer_name = st.text_input(
                    "Neuer Name des Übermoduls",
                    value=uebermodul.modulname,
                )

                speichern = st.form_submit_button(
                    "Übermoduländerungen speichern",
                    type="primary",
                )

            if speichern:
                try:
                    uebermodul.setzeModulname(neuer_name)

                    self._repository.speichereStudium(
                        self._studium
                    )

                    st.rerun()

                except (ValueError, TypeError) as fehler:
                    st.error(str(fehler))

        st.divider()
        st.subheader("Einzelmodul bearbeiten")

        bearbeitbare_module = self._studium.gibEinzelmodule()

        if not bearbeitbare_module:
            st.info("Keine Einzelmodule zum Bearbeiten vorhanden.")

        else:
            modul_index = st.selectbox(
                "Welches Modul möchtest du bearbeiten?",
                options=range(len(bearbeitbare_module)),
                format_func=lambda i: bearbeitbare_module[i].modulname,
                key="modul_bearbeiten_auswahl",
            )

            modul = bearbeitbare_module[modul_index]

            with st.form(
                f"modul_bearbeiten_{modul_index}"
            ):
                neuer_name = st.text_input(
                    "Modulname",
                    value=modul.modulname,
                )

                neue_modulart = st.selectbox(
                    "Modulart",
                    options=list(Modulart),
                    index=list(Modulart).index(modul._modulart),
                    format_func=lambda art: art.value,
                )

                neue_ects = st.number_input(
                    "ECTS",
                    min_value=1,
                    max_value=30,
                    value=modul.getEcts(),
                    step=1,
                )

                speichern = st.form_submit_button(
                    "Moduländerungen speichern",
                    type="primary",
                )

            if speichern:
                try:
                    modul.setzeModulname(neuer_name)
                    modul.setzeModulart(neue_modulart)
                    modul.setzeEcts(int(neue_ects))

                    self._repository.speichereStudium(
                        self._studium
                    )

                    st.rerun()

                except (ValueError, TypeError) as fehler:
                    st.error(str(fehler))

        st.divider()
        st.subheader("Einzelmodul löschen")

        loeschbare_module = self._studium.gibEinzelmodule()

        if not loeschbare_module:
            st.info("Keine Einzelmodule zum Löschen vorhanden.")

        else:
            modul_index = st.selectbox(
                "Welches Modul möchtest du löschen?",
                options=range(len(loeschbare_module)),
                format_func=lambda i: loeschbare_module[i].modulname,
                key="modul_loeschen_auswahl",
            )

            zu_loeschendes_modul = loeschbare_module[modul_index]

            bestaetigung = st.checkbox(
                f"Ich möchte '{zu_loeschendes_modul.modulname}' "
                "endgültig löschen.",
                key=f"loeschen_bestaetigen_{modul_index}",
            )

            if st.button(
                "Modul endgültig löschen",
                type="primary",
                disabled=not bestaetigung,
            ):
                try:
                    self._studium.entferneModul(
                        zu_loeschendes_modul
                    )

                    self._repository.speichereStudium(
                        self._studium
                    )

                    st.rerun()

                except (ValueError, TypeError) as fehler:
                    st.error(str(fehler))
        
        st.divider()
        st.subheader("Übermodul löschen")

        loeschbare_uebermodule = [
            modul
            for modul in self._studium._topLevelModule
            if isinstance(modul, Uebermodul)
        ]

        if not loeschbare_uebermodule:
            st.info("Keine Übermodule zum Löschen vorhanden.")

        else:
            uebermodul_index = st.selectbox(
                "Welches Übermodul möchtest du löschen?",
                options=range(len(loeschbare_uebermodule)),
                format_func=lambda i: (
                    loeschbare_uebermodule[i].modulname
                ),
                key="uebermodul_loeschen_auswahl",
            )

            zu_loeschendes_uebermodul = (
                loeschbare_uebermodule[uebermodul_index]
            )

            st.info(
                "Die enthaltenen Module bleiben erhalten "
                "und werden zu eigenständigen Hauptmodulen."
            )

            bestaetigung = st.checkbox(
                f"Ich möchte das Übermodul "
                f"'{zu_loeschendes_uebermodul.modulname}' löschen.",
                key=f"uebermodul_loeschen_{uebermodul_index}",
            )

            if st.button(
                "Übermodul endgültig löschen",
                disabled=not bestaetigung,
                key="uebermodul_loeschen_button",
            ):
                try:
                    self._studium.entferneUebermodul(
                        zu_loeschendes_uebermodul
                    )

                    self._repository.speichereStudium(
                        self._studium
                    )

                    st.rerun()

                except (ValueError, TypeError) as fehler:
                    st.error(str(fehler))
      
    
    def zeigeBachelorarbeit(self) -> None:
        """Zeigt die Verwaltung der Bachelorarbeit."""

        st.title("🎓 Meine Bachelorarbeit")

        bachelorarbeit = self._studium._bachelorarbeit

        if bachelorarbeit is None:
            st.subheader("Bachelorarbeit anlegen")

            st.write(
                "Erfasse zunächst die grundlegenden Daten "
                "deiner Bachelorarbeit."
            )

            with st.form("bachelorarbeit_anlegen"):
                ects = st.number_input(
                    "ECTS der Bachelorarbeit",
                    min_value=1,
                    max_value=60,
                    value=10,
                    step=1,
                )

                speichern = st.form_submit_button(
                    "Bachelorarbeit anlegen",
                    type="primary",
                )

            if speichern:
                try:
                    bachelorarbeit = Bachelorarbeit(
                        ects=int(ects),
                    )

                    self._studium.setzeBachelorarbeit(
                        bachelorarbeit
                    )

                    self._repository.speichereStudium(
                        self._studium
                    )

                    st.rerun()

                except (ValueError, TypeError) as fehler:
                    st.error(str(fehler))

        else:
            st.subheader("Übersicht")

            spalte1, spalte2 = st.columns(2)

            with spalte1:
                st.metric(
                    "ECTS",
                    bachelorarbeit.ects,
                )

            with spalte2:
                st.metric(
                    "Status",
                    bachelorarbeit._status.value,
                )

            st.success(
                "Deine Bachelorarbeit wurde angelegt."
            )
            if bachelorarbeit.note is not None:
                st.metric(
                    "Bachelorarbeitsnote",
                    f"{bachelorarbeit.note:.2f}",
                )
            else:
                st.caption(
                    "Bachelorarbeitsnote: Noch nicht vorhanden"
                )
            st.subheader("Wichtige Termine")

            termine = [
                ("Anmeldedatum", bachelorarbeit._anmeldedatum),
                ("Startdatum", bachelorarbeit._startdatum),
                ("Abgabefrist", bachelorarbeit._fristablaufdatum),
                ("Tatsächliche Abgabe", bachelorarbeit._abgabedatum),
            ]

            for bezeichnung, termin in termine:
                if termin is not None:
                    st.write(
                        f"**{bezeichnung}:** {termin:%d.%m.%Y}"
                    )
                else:
                    st.write(
                        f"**{bezeichnung}:** Noch nicht festgelegt"
                    )

            st.divider()
            st.subheader("Countdown zur Abgabefrist")

            verbleibende_tage = (
                bachelorarbeit.berechneVerbleibendeTage()
            )

            if bachelorarbeit._abgabedatum is not None:
                st.success(
                    "Die Bachelorarbeit wurde bereits abgegeben."
                )

            elif verbleibende_tage is None:
                st.info(
                    "Lege eine Abgabefrist fest, "
                    "um den Countdown anzuzeigen."
                )

            elif verbleibende_tage > 0:
                st.metric(
                    "Verbleibende Tage",
                    verbleibende_tage,
                )

            elif verbleibende_tage == 0:
                st.warning(
                    "Heute ist die Abgabefrist!"
                )

            else:
                st.error(
                    f"Die Abgabefrist ist seit "
                    f"{abs(verbleibende_tage)} Tagen überschritten."
                )

            
            st.divider()
            st.subheader("Bachelorarbeitsnote")

            note_aktiv = st.checkbox(
                "Note der Bachelorarbeit eintragen",
                value=bachelorarbeit.note is not None,
                key="ba_note_aktiv",
            )

            with st.form("bachelorarbeit_note"):
                note = st.number_input(
                    "Note",
                    min_value=1.0,
                    max_value=5.0,
                    value=(
                        float(bachelorarbeit.note)
                        if bachelorarbeit.note is not None
                        else 2.0
                    ),
                    step=0.1,
                    format="%.2f",
                    disabled=not note_aktiv,
                )

                note_speichern = st.form_submit_button(
                    "Bachelorarbeitsnote speichern",
                    type="primary",
                )

            if note_speichern:
                try:
                    if note_aktiv:
                        bachelorarbeit.setzeNote(
                            Decimal(str(note))
                        )
                    else:
                        bachelorarbeit.setzeNote(None)

                    self._repository.speichereStudium(
                        self._studium
                    )

                    st.rerun()

                except (ValueError, TypeError) as fehler:
                    st.error(str(fehler))

            st.divider()
            st.subheader("Bachelorarbeit bearbeiten")

            # Checkboxen außerhalb des Formulars:
            # Änderungen werden sofort angezeigt.
            anmeldedatum_aktiv = st.checkbox(
                "Anmeldedatum festlegen",
                value=bachelorarbeit._anmeldedatum is not None,
                key="ba_anmeldedatum_aktiv",
            )

            frist_aktiv = st.checkbox(
                "Abgabefrist festlegen",
                value=bachelorarbeit._fristablaufdatum is not None,
                key="ba_frist_aktiv",
            )

            startdatum_aktiv = st.checkbox(
                "Startdatum festlegen",
                value=bachelorarbeit._startdatum is not None,
                key="ba_startdatum_aktiv",
            )

            abgabedatum_aktiv = st.checkbox(
                "Tatsächliches Abgabedatum festlegen",
                value=bachelorarbeit._abgabedatum is not None,
                key="ba_abgabedatum_aktiv",
            )

            with st.form("bachelorarbeit_bearbeiten"):
                neuer_status = st.selectbox(
                    "Status der Bachelorarbeit",
                    options=list(BachelorarbeitsStatus),
                    index=list(BachelorarbeitsStatus).index(
                        bachelorarbeit._status
                    ),
                    format_func=lambda status: status.value,
                )

                st.write("**Wichtige Termine**")

                anmeldedatum = st.date_input(
                    "Anmeldedatum",
                    value=bachelorarbeit._anmeldedatum or date.today(),
                    disabled=not anmeldedatum_aktiv,
                )

                fristablaufdatum = st.date_input(
                    "Abgabefrist",
                    value=bachelorarbeit._fristablaufdatum or date.today(),
                    disabled=not frist_aktiv,
                )

                startdatum = st.date_input(
                    "Startdatum",
                    value=bachelorarbeit._startdatum or date.today(),
                    disabled=not startdatum_aktiv,
                )

                abgabedatum = st.date_input(
                    "Tatsächliches Abgabedatum",
                    value=bachelorarbeit._abgabedatum or date.today(),
                    disabled=not abgabedatum_aktiv,
                )

                speichern = st.form_submit_button(
                    "Änderungen speichern",
                    type="primary",
                )

            if speichern:
                try:
                    bachelorarbeit.setzeTermine(
                        anmeldedatum if anmeldedatum_aktiv else None,
                        fristablaufdatum if frist_aktiv else None,
                        startdatum if startdatum_aktiv else None,
                        abgabedatum if abgabedatum_aktiv else None,
                    )

                    if bachelorarbeit.note is not None:
                        neuer_status = BachelorarbeitsStatus.BENOTET

                    bachelorarbeit.setzeStatus(neuer_status)

                    self._repository.speichereStudium(
                        self._studium
                    )

                    st.rerun()

                except (ValueError, TypeError) as fehler:
                    st.error(str(fehler))



    
    def bearbeiteModul(self) -> None:
        """Ermöglicht die Bearbeitung von Prüfungsstatus, Terminen und Ergebnissen."""
        st.header("Prüfungsleistungen bearbeiten")

        module = self._studium.gibEinzelmodule()

        if not module:
            st.info("Bitte lege zuerst ein Einzelmodul an.")
            return

        # Modul über einen Index auswählen
        modul_index = st.selectbox(
            "Modul auswählen",
            options=range(len(module)),
            format_func=lambda i: module[i].modulname,
        )

        modul = module[modul_index]
        pruefung = modul._pruefungsleistung

        if pruefung is None:
            st.warning(
                "Für dieses Modul ist keine Prüfungsleistung hinterlegt."
            )
            return

        # Drei Bereiche wie in der Skizze
        spalte1, spalte2, spalte3 = st.columns(3)

        with spalte1:
            st.subheader("Modul")
            st.write(f"**{modul.modulname}**")
            st.write(f"{modul.getEcts()} ECTS")

        
        with spalte2:
            st.subheader("Prüfungsdetails")

            st.write(
                f"Prüfungsart: {pruefung._pruefungsart.value}"
            )

            st.write(
                f"Bewertungsart: {pruefung.bewertungsart.value}"
            )

            if pruefung._geplantes_pruefungsdatum is not None:
                st.write(
                    "Geplantes Prüfungsdatum: "
                    f"{pruefung._geplantes_pruefungsdatum:%d.%m.%Y}"
                )
            else:
                st.write("Geplantes Prüfungsdatum: Nicht festgelegt")
                        
            if pruefung.bewertungsart == Bewertungsart.BENOTET:
                if pruefung.note is not None:
                    st.write(
                        f"**Note: {pruefung.note:.2f}**"
                    )
                else:
                    st.write("Note: Noch nicht eingetragen")

            elif pruefung.ergebnis is not None:
                st.write(
                    f"Prüfungsergebnis: {pruefung.ergebnis.value}"
                )
            else:
                st.write("Prüfungsergebnis: Noch nicht eingetragen")

        with spalte3:
            st.subheader("Status")
            st.write(pruefung._status.value)

        st.divider()

        
        # Checkbox außerhalb des Formulars:
        # Die Datumseingabe reagiert dadurch sofort.
        datum_vorhanden = st.checkbox(
            "Geplantes Prüfungsdatum festlegen",
            value=(
                pruefung._geplantes_pruefungsdatum is not None
            ),
            key=f"datum_aktiv_{modul_index}",
        )
        note_eintragen = False

        if pruefung.bewertungsart == Bewertungsart.BENOTET:
            note_eintragen = st.checkbox(
                "Note eintragen",
                value=pruefung.note is not None,
                key=f"note_aktiv_{modul_index}",
            )
        with st.form("pruefung_bearbeiten"):
            status = st.selectbox(
                "Neuer Prüfungsstatus",
                options=list(Status),
                index=list(Status).index(pruefung._status),
                format_func=lambda wert: wert.value,
            )

            geplantes_datum = st.date_input(
                "Geplantes Prüfungsdatum",
                value=(
                    pruefung._geplantes_pruefungsdatum
                    or date.today()
                ),
                disabled=not datum_vorhanden,
            )
            st.subheader("Prüfungsergebnis")

            if pruefung.bewertungsart == Bewertungsart.BENOTET:

                note = st.number_input(
                    "Note",
                    min_value=1.0,
                    max_value=5.0,
                    value=(
                        float(pruefung.note)
                        if pruefung.note is not None
                        else 2.0
                    ),
                    step=0.1,
                    disabled=not note_eintragen,
                )

            else:
                ergebnis = st.selectbox(
                    "Prüfungsergebnis",
                    options=list(Pruefungsergebnis),
                    format_func=lambda wert: wert.value,
                )

            speichern = st.form_submit_button(
                "Änderungen speichern",
                type="primary",
            )

        
        if speichern:
            try:
                pruefung.setzeGeplantesPruefungsdatum(
                    geplantes_datum if datum_vorhanden else None
                )

                if pruefung.bewertungsart == Bewertungsart.BENOTET:
                    if note_eintragen:
                        pruefung.setzeNote(Decimal(str(note)))
                        pruefung.setzeStatus(Status.ABGESCHLOSSEN)
                    else:
                        pruefung.setzeNote(None)
                        pruefung.setzeStatus(status)

                else:
                    pruefung.setzeErgebnis(ergebnis)
                    pruefung.setzeStatus(Status.ABGESCHLOSSEN)

                self._repository.speichereStudium(
                    self._studium
                )

                st.rerun()

            except (ValueError, TypeError) as fehler:
                st.error(str(fehler))





import streamlit as st

from studybuddy.repository import DatenbankRepository
from studybuddy.view import StudyBuddyView


def main():
    """Startet StudyBuddy und steuert die Einrichtung sowie die Seitennavigation."""
    st.set_page_config(
        page_title="StudyBuddy",
        page_icon="🎓",
        layout="wide",
    )

    repository = DatenbankRepository("studybuddy.db")

    try:
        studium = repository.ladeStudium()

    
    except ValueError:
        from datetime import date
        from decimal import Decimal
        from studybuddy.modelle import Studium

        st.title("🎓 Willkommen bei StudyBuddy!")
        st.write("Richte zuerst dein Studium ein.")

        with st.form("studium_einrichten"):
            studiengang = st.text_input(
                "Studiengang",
                value="Wirtschaftsinformatik",
            )

            abschlussdatum = st.date_input(
                "Geplantes Abschlussdatum",
                value=date(2027, 3, 31),
            )

            meilenstein = st.date_input(
                "Prüfungs-Meilenstein",
                value=date(2026, 12, 16),
            )

            notenziel = st.number_input(
                "Gewünschter Notendurchschnitt",
                min_value=1.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )

            speichern = st.form_submit_button(
                "Studium erstellen",
                type="primary",
            )

        if speichern:
            try:
                studium = Studium(
                    studiengang=studiengang,
                    ziel_abschlussdatum=abschlussdatum,
                    pruefungs_meilenstein=meilenstein,
                    notenziel=Decimal(str(notenziel)),
                )

                repository.speichereStudium(studium)
                st.rerun()

            except ValueError as fehler:
                st.error(str(fehler))

        return


    view = StudyBuddyView(studium, repository)

    seite = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Module", "Prüfungen bearbeiten", "Bachelorarbeit",],
    )

    if seite == "Dashboard":
        view.zeigeDashboard()

    elif seite == "Module":
        view.zeigeModule()

    elif seite == "Prüfungen bearbeiten":
        view.bearbeiteModul()

    elif seite == "Bachelorarbeit":
        view.zeigeBachelorarbeit()


if __name__ == "__main__":
    main()

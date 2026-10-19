import sqlite3
import streamlit as st

st.title("StudyBuddy 🎓")
st.subheader("Daten aus der SQLite-Datenbank")

# Verbindung zur Datenbank herstellen
verbindung = sqlite3.connect("studybuddy.db")
cursor = verbindung.cursor()

# Prüfungsleistungen aus der Datenbank auslesen
cursor.execute("""
SELECT id, modulname, pruefungsart, status, note
FROM pruefungsleistung
""")

pruefungsleistungen = cursor.fetchall()
verbindung.close()

# Anzahl der gespeicherten Prüfungsleistungen anzeigen
st.metric("Gespeicherte Prüfungsleistungen", len(pruefungsleistungen))

# Daten auf der Oberfläche darstellen
for pruefung in pruefungsleistungen:
    id, modulname, pruefungsart, status, note = pruefung

    st.write(f"**{modulname}**")
    st.write(f"Prüfungsart: {pruefungsart}")
    st.write(f"Status: {status}")

    if note is None:
        st.write("Note: noch nicht vorhanden")
    else:
        st.write(f"Note: {note}")

    st.divider()
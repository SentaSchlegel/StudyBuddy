import streamlit as st

st.title("StudyBuddy 🎓")
st.subheader("Mein Studienfortschritt")

st.metric("Aktueller Notendurchschnitt", "2,47")
st.metric("Benotete Prüfungen", "14")

st.write("Status einer Prüfungsleistung:")

status = st.selectbox(
    "Status auswählen",
    ["Noch nicht begonnen", "In Bearbeitung", "Eingereicht", "Benotet"]
)

if st.button("Status übernehmen"):
    st.success(f"Status wurde auf „{status}“ gesetzt.")
import streamlit as st

# Titel van de Streamlit app
st.title("Streamlit App met Twee Tabbladen")

# Maak twee tabbladen
tab1, tab2 = st.tabs(["Tabblad 1", "Tabblad 2"])

# Inhoud voor Tabblad 1
with tab1:
    st.header("Tabblad 1")
    st.write("Dit is het eerste tabblad. Voeg hier je inhoud toe.")

# Inhoud voor Tabblad 2
with tab2:
    st.header("Tabblad 2")
    st.write("Dit is het tweede tabblad. Voeg hier je inhoud toe.")

import streamlit as st
import pandas as pd
import gerir_agenda
    
def main():
    st.title("Calendário d'Os Cinco")
    st.image("foto_benedita.png", use_column_width=True)

    menu = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["Menu Principal", "Gerir Agenda"]
    )
    
    if menu == "Menu Principal":
        st.subheader("Bem-vindo ao Calendário d'Os Cinco")
    elif menu == "Gerir Agenda":
        gerir_agenda.gerir()

if __name__ == "__main__":
    main()

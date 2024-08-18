import streamlit as st
import pandas as pd
import gerir_agenda
import visualizar_agendas
    
def main():
    st.title("Calendário d'Os Cinco")
    st.image("foto_benedita.png", use_column_width=True)

    menu = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["Menu Principal", "Gerir Agenda", "Visualizar Agendas"]
    )
    
    st.write("Selecione os blocos de horários em que deseja adicionar tarefas:")

    if menu == "Menu Principal":
        st.subheader("Bem-vindo ao Calendário d'Os Cinco")
    elif menu == "Gerir Agenda":
        gerir_agenda.gerir()
    elif menu == "Visualizar Agendas":
        visualizar_agendas.show()

if __name__ == "__main__":
    main()

import streamlit as st
import gere_agendas
import visualizar

def main():
    st.title("Aplicação Agenda - Calendário Os Cinco")
    st.image("foto_benedita.png", use_column_width=True)

    menu = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["Menu Principal", "Gerir Agenda Pessoal", "Visualizar Agendas"]
    )

    if menu == "Menu Principal":
        st.subheader("Bem-vindo ao Calendário d'Os Cinco")
    elif menu == "Gerir Agenda Pessoal":
        gere_agendas.gerir()
    elif menu == "Visualizar Agendas":
        visualizar.show()

if __name__ == "__main__":
    main()

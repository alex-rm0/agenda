import streamlit as st
import pandas as pd
import os

# Função para carregar agendas existentes
def carregar_agendas():
    if os.path.exists("agendas.txt"):
        agendas = []
        with open("agendas.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 5:
                    agendas.append({
                        "Utilizador": parts[0],
                        "Cor": parts[1],
                        "Dia": parts[2],
                        "Hora": parts[3],
                        "Tarefa": parts[4]
                    })
        return pd.DataFrame(agendas)
    else:
        return pd.DataFrame(columns=["Utilizador", "Cor", "Dia", "Hora", "Tarefa"])

# Função para exibir a agenda
def show():
    st.subheader("Visualizar Agendas")
    
    agendas = carregar_agendas()
    if not agendas.empty:
        dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        tabela = pd.DataFrame(index=[f"{hora:02d}:00" for hora in range(8, 20)], columns=dias_da_semana)

        for _, row in agendas.iterrows():
            tabela.at[row["Hora"], row["Dia"]] = f'{row["Utilizador"]}: {row["Tarefa"]}'

        st.table(tabela)
    else:
        st.info("Nenhuma agenda foi criada ainda.")

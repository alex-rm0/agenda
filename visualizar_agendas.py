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
                        "Hora_Inicio": parts[3],
                        "Hora_Fim": parts[4],
                        "Tarefa": parts[5]
                    })
        return pd.DataFrame(agendas)
    else:
        return pd.DataFrame(columns=["Utilizador", "Cor", "Dia", "Hora_Inicio", "Hora_Fim", "Tarefa"])

# Função para exibir a agenda
def show():
    st.subheader("Visualizar Agendas")
    
    agendas = carregar_agendas()
    if not agendas.empty:
        dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        horas = [f"{hora:02d}:00" for hora in range(8, 20)]
        
        tabela = pd.DataFrame(index=horas, columns=dias_da_semana)
        tabela.index.name = 'Hora'
        
        for _, row in agendas.iterrows():
            hora_inicio = row["Hora_Inicio"]
            hora_fim = row["Hora_Fim"]
            dia = row["Dia"]
            tarefa = f'{row["Utilizador"]}: {row["Tarefa"]}'
            
            if hora_inicio in tabela.index:
                tabela.at[hora_inicio, dia] = tarefa
            
            # Caso a tarefa se estenda por várias horas
            start_index = horas.index(hora_inicio)
            end_index = horas.index(hora_fim)
            for idx in range(start_index, end_index):
                tabela.at[horas[idx], dia] = tarefa

        st.table(tabela)
    else:
        st.info("Nenhuma agenda foi criada ainda.")

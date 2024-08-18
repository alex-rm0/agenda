import streamlit as st
import pandas as pd
import os

# Função para carregar agendas existentes
def carregar_agendas():
    if os.path.exists("agendas.csv"):
        return pd.read_csv("agendas.csv", index_col=0)
    else:
        return pd.DataFrame(columns=["Utilizador", "Cor", "Dia", "Hora", "Tarefa"])

# Função para salvar agendas
def salvar_agendas(df):
    df.to_csv("agendas.csv")

# Função para criar uma nova agenda
def criar_agenda():
    utilizador = st.text_input("Digite seu nome:")
    cor = st.color_picker("Escolha uma cor para sua agenda:")
    
    if st.button("Criar Agenda"):
        if utilizador and cor:
            agendas = carregar_agendas()
            if utilizador in agendas["Utilizador"].unique():
                st.warning("Este utilizador já tem uma agenda.")
            else:
                st.success(f"Agenda criada para {utilizador} com a cor {cor}.")
        else:
            st.error("Por favor, preencha todos os campos.")

# Função para selecionar uma agenda existente
def selecionar_agenda():
    agendas = carregar_agendas()
    utilizador = st.selectbox("Selecione sua agenda:", agendas["Utilizador"].unique())
    return utilizador

# Função para gerenciar a agenda selecionada
def gerir_agenda(utilizador):
    st.subheader(f"Gerenciando a agenda de {utilizador}")
    dia = st.selectbox("Selecione o dia da semana:", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
    hora = st.selectbox("Selecione o horário:", [f"{hora:02d}:00" for hora in range(8, 20)])
    tarefa = st.text_input("Descrição da tarefa:")
    
    if st.button("Adicionar Tarefa"):
        if tarefa:
            agendas = carregar_agendas()
            nova_tarefa = pd.DataFrame([[utilizador, agendas.loc[agendas['Utilizador'] == utilizador, 'Cor'].iloc[0], dia, hora, tarefa]],
                                       columns=["Utilizador", "Cor", "Dia", "Hora", "Tarefa"])
            agendas = pd.concat([agendas, nova_tarefa], ignore_index=True)
            salvar_agendas(agendas)
            st.success(f"Tarefa '{tarefa}' adicionada para {dia} às {hora}.")
        else:
            st.error("Por favor, preencha todos os campos.")

# Função principal para gerenciamento
def gerir():
    opcao = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["Criar Nova Agenda", "Selecionar Agenda Existente"]
    )
    
    if opcao == "Criar Nova Agenda":
        criar_agenda()
    elif opcao == "Selecionar Agenda Existente":
        utilizador = selecionar_agenda()
        if utilizador:
            gerir_agenda(utilizador)

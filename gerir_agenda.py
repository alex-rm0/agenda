import streamlit as st
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
        return agendas
    else:
        return []

# Função para salvar agendas
def salvar_agendas(agendas):
    with open("agendas.txt", "w") as file:
        for agenda in agendas:
            file.write(f"{agenda['Utilizador']}|{agenda['Cor']}|{agenda['Dia']}|{agenda['Hora']}|{agenda['Tarefa']}\n")

# Função para criar uma nova agenda
def criar_agenda():
    utilizador = st.text_input("Digite seu nome:")
    cor = st.color_picker("Escolha uma cor para sua agenda:")
    
    if st.button("Criar Agenda"):
        if utilizador and cor:
            agendas = carregar_agendas()
            if any(agenda["Utilizador"] == utilizador for agenda in agendas):
                st.warning("Este utilizador já tem uma agenda.")
            else:
                st.success(f"Agenda criada para {utilizador} com a cor {cor}.")
        else:
            st.error("Por favor, preencha todos os campos.")

# Função para selecionar uma agenda existente
def selecionar_agenda():
    agendas = carregar_agendas()
    utilizadores = set(agenda["Utilizador"] for agenda in agendas)
    utilizador = st.selectbox("Selecione sua agenda:", list(utilizadores))
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
            cor = next((agenda["Cor"] for agenda in agendas if agenda["Utilizador"] == utilizador), None)
            if cor:
                nova_tarefa = {
                    "Utilizador": utilizador,
                    "Cor": cor,
                    "Dia": dia,
                    "Hora": hora,
                    "Tarefa": tarefa
                }
                agendas.append(nova_tarefa)
                salvar_agendas(agendas)
                st.success(f"Tarefa '{tarefa}' adicionada para {dia} às {hora}.")
            else:
                st.error("Cor da agenda não encontrada.")
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

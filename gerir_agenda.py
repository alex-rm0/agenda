import streamlit as st
import os

# Função para carregar usuários
def carregar_usuarios():
    if os.path.exists("users.txt"):
        usuarios = []
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    usuarios.append({
                        "Utilizador": parts[0],
                        "Cor": parts[1]
                    })
        return usuarios
    else:
        return []

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
                        "Dia": parts[1],
                        "Hora_Inicio": parts[2],
                        "Hora_Fim": parts[3],
                        "Tarefa": parts[4]
                    })
        return agendas
    else:
        return []

# Função para salvar usuários
def salvar_usuarios(usuarios):
    with open("users.txt", "w") as file:
        for usuario in usuarios:
            file.write(f"{usuario['Utilizador']}|{usuario['Cor']}\n")

# Função para salvar agendas
def salvar_agendas(agendas):
    with open("agendas.txt", "w") as file:
        for agenda in agendas:
            file.write(f"{agenda['Utilizador']}|{agenda['Dia']}|{agenda['Hora_Inicio']}|{agenda['Hora_Fim']}|{agenda['Tarefa']}\n")

# Função para criar uma nova agenda
def criar_agenda():
    utilizador = st.text_input("Digite seu nome:")
    cor = st.color_picker("Escolha uma cor para sua agenda:")
    
    if st.button("Criar Agenda"):
        if utilizador and cor:
            usuarios = carregar_usuarios()
            if any(usuario["Utilizador"] == utilizador for usuario in usuarios):
                st.warning("Este utilizador já tem uma agenda.")
            else:
                # Adiciona o novo usuário à lista de usuários
                novos_usuarios = usuarios + [{
                    "Utilizador": utilizador,
                    "Cor": cor
                }]
                salvar_usuarios(novos_usuarios)
                st.success(f"Agenda criada para {utilizador} com a cor {cor}.")
        else:
            st.error("Por favor, preencha todos os campos.")

# Função para selecionar uma agenda existente
def selecionar_agenda():
    usuarios = carregar_usuarios()
    utilizadores = set(usuario["Utilizador"] for usuario in usuarios)
    utilizador = st.selectbox("Selecione sua agenda:", list(utilizadores))
    return utilizador

# Função para gerenciar a agenda selecionada
def gerir_agenda(utilizador):
    st.subheader(f"Gerenciando a agenda de {utilizador}")
    dia = st.selectbox("Selecione o dia da semana:", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
    hora_inicio = st.selectbox("Selecione a hora de início:", [f"{hora:02d}:00" for hora in range(8, 20)])
    hora_fim = st.selectbox("Selecione a hora de fim:", [f"{hora:02d}:00" for hora in range(8, 20)])
    tarefa = st.text_input("Descrição da tarefa:")
    
    if st.button("Adicionar Tarefa"):
        if tarefa and hora_inicio and hora_fim:
            if hora_inicio >= hora_fim:
                st.error("A hora de início deve ser antes da hora de fim.")
            else:
                agendas = carregar_agendas()
                nova_tarefa = {
                    "Utilizador": utilizador,
                    "Dia": dia,
                    "Hora_Inicio": hora_inicio,
                    "Hora_Fim": hora_fim,
                    "Tarefa": tarefa
                }
                agendas.append(nova_tarefa)
                salvar_agendas(agendas)
                st.success(f"Tarefa '{tarefa}' adicionada para {dia} das {hora_inicio} às {hora_fim}.")
        else:
            st.error("Por favor, preencha todos os campos.")

    # Exibir e permitir edição ou remoção de tarefas
    st.subheader("Gerenciar Tarefas")
    tarefas = [agenda for agenda in carregar_agendas() if agenda["Utilizador"] == utilizador]
    if tarefas:
        tarefa_editar = st.selectbox("Selecione uma tarefa para editar ou remover:", [f"{t['Dia']} {t['Hora_Inicio']} - {t['Hora_Fim']} - {t['Tarefa']}" for t in tarefas])
        if tarefa_editar:
            tarefa_selecionada = next(t for t in tarefas if f"{t['Dia']} {t['Hora_Inicio']} - {t['Hora_Fim']} - {t['Tarefa']}" == tarefa_editar)
            
            with st.form("Editar Tarefa"):
                novo_dia = st.selectbox("Novo dia:", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"], index=["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"].index(tarefa_selecionada["Dia"]))
                nova_hora_inicio = st.selectbox("Nova hora de início:", [f"{hora:02d}:00" for hora in range(8, 20)], index=[f"{hora:02d}:00" for hora in range(8, 20)].index(tarefa_selecionada["Hora_Inicio"]))
                nova_hora_fim = st.selectbox("Nova hora de fim:", [f"{hora:02d}:00" for hora in range(8, 20)], index=[f"{hora:02d}:00" for hora in range(8, 20)].index(tarefa_selecionada["Hora_Fim"]))
                nova_tarefa = st.text_input("Nova descrição da tarefa:", value=tarefa_selecionada["Tarefa"])
                submitted = st.form_submit_button("Atualizar Tarefa")

                if submitted:
                    if nova_tarefa and nova_hora_inicio and nova_hora_fim:
                        if nova_hora_inicio >= nova_hora_fim:
                            st.error("A nova hora de início deve ser antes da nova hora de fim.")
                        else:
                            agendas = carregar_agendas()
                            agendas = [t for t in agendas if not (t['Dia'] == tarefa_selecionada['Dia'] and t['Hora_Inicio'] == tarefa_selecionada['Hora_Inicio'] and t['Hora_Fim'] == tarefa_selecionada['Hora_Fim'] and t['Tarefa'] == tarefa_selecionada['Tarefa'] and t['Utilizador'] == utilizador)]
                            agendas.append({
                                "Utilizador": utilizador,
                                "Dia": novo_dia,
                                "Hora_Inicio": nova_hora_inicio,
                                "Hora_Fim": nova_hora_fim,
                                "Tarefa": nova_tarefa
                            })
                            salvar_agendas(agendas)
                            st.success("Tarefa atualizada com sucesso!")
                    else:
                        st.error("Por favor, preencha todos os campos.")
                
                # Usar st.form_submit_button() para remover a tarefa
                if st.form_submit_button("Remover Tarefa"):
                    agendas = carregar_agendas()
                    agendas = [t for t in agendas if not (t['Dia'] == tarefa_selecionada['Dia'] and t['Hora_Inicio'] == tarefa_selecionada['Hora_Inicio'] and t['Hora_Fim'] == tarefa_selecionada['Hora_Fim'] and t['Tarefa'] == tarefa_selecionada['Tarefa'] and t['Utilizador'] == utilizador)]
                    salvar_agendas(agendas)
                    st.success("Tarefa removida com sucesso!")

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

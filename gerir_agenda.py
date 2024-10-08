import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

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
        return pd.DataFrame(agendas)
    else:
        return pd.DataFrame(columns=["Utilizador", "Dia", "Hora_Inicio", "Hora_Fim", "Tarefa"])

# Função para salvar usuários
def salvar_usuarios(usuarios):
    with open("users.txt", "w") as file:
        for usuario in usuarios:
            file.write(f"{usuario['Utilizador']}|{usuario['Cor']}\n")

# Função para salvar agendas
def salvar_agendas(agendas):
    with open("agendas.txt", "w") as file:
        for _, row in agendas.iterrows():
            file.write(f"{row['Utilizador']}|{row['Dia']}|{row['Hora_Inicio']}|{row['Hora_Fim']}|{row['Tarefa']}\n")

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
                # Utilizar pd.concat em vez de append
                agendas = pd.concat([agendas, pd.DataFrame([nova_tarefa])], ignore_index=True)
                salvar_agendas(agendas)
                st.success(f"Tarefa '{tarefa}' adicionada para {dia} das {hora_inicio} às {hora_fim}.")
        else:
            st.error("Por favor, preencha todos os campos.")

    # Exibir e permitir remoção de tarefas
    st.subheader("Remover Tarefas")
    agendas_df = carregar_agendas()
    tarefas = agendas_df[agendas_df["Utilizador"] == utilizador].to_dict('records')

    if tarefas:
        tarefa_remover = st.selectbox("Selecione uma tarefa para remover:", [f"{t['Dia']} {t['Hora_Inicio']} - {t['Hora_Fim']} - {t['Tarefa']}" for t in tarefas])
        if tarefa_remover:
            tarefa_selecionada = next(t for t in tarefas if f"{t['Dia']} {t['Hora_Inicio']} - {t['Hora_Fim']} - {t['Tarefa']}" == tarefa_remover)
            
            if st.button("Remover Tarefa"):
                agendas = carregar_agendas()
                agendas = agendas[~((agendas['Dia'] == tarefa_selecionada['Dia']) &
                                    (agendas['Hora_Inicio'] == tarefa_selecionada['Hora_Inicio']) &
                                    (agendas['Hora_Fim'] == tarefa_selecionada['Hora_Fim']) &
                                    (agendas['Tarefa'] == tarefa_selecionada['Tarefa']) &
                                    (agendas['Utilizador'] == utilizador))]
                salvar_agendas(agendas)
                st.success("Tarefa removida com sucesso!")

# Função para obter a data do início da semana
def inicio_da_semana(data, semana):
    start_date = data - timedelta(days=data.weekday())  # Segunda-feira da semana atual
    start_date += timedelta(weeks=semana - 1)  # Ajusta para a semana selecionada
    return start_date

# Função para visualizar todas as agendas
def visualizar_agendas():
    st.subheader("Visualizar Todas as Agendas")

    semanas = [1, 2, 3, 4]
    semana_selecionada = st.selectbox("Selecione a semana:", semanas)

    data_atual = datetime.now()
    inicio_semana = inicio_da_semana(data_atual, semana_selecionada)
    fim_semana = inicio_semana + timedelta(days=6)

    st.write(f"Visualizando a semana de {inicio_semana.strftime('%d/%m/%Y')} a {fim_semana.strftime('%d/%m/%Y')}")

    agendas = carregar_agendas()
    usuarios = carregar_usuarios()
    
    if not agendas.empty:
        dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        horas = [f"{hora:02d}:00" for hora in range(8, 20)]
        tabela = pd.DataFrame(index=horas, columns=dias_da_semana)

        # Cria um dicionário para mapear utilizadores para suas cores
        cor_usuarios = {usuario['Utilizador']: usuario['Cor'] for usuario in usuarios}

        for _, row in agendas.iterrows():
            dia = row["Dia"]
            hora_inicio = row["Hora_Inicio"]
            hora_fim = row["Hora_Fim"]
            tarefa = f'{row["Utilizador"]}: {row["Tarefa"]}'
            cor = cor_usuarios.get(row["Utilizador"], "#FFFFFF")  # Pega a cor do utilizador ou branco como padrão
            
            data_tarefa = datetime.strptime(f'{dia} {hora_inicio}', '%A %H:%M')
            if inicio_semana <= data_tarefa <= fim_semana:
                if dia in tabela.columns:
                    if hora_inicio in tabela.index:
                        start_index = tabela.index.get_loc(hora_inicio)
                        end_index = tabela.index.get_loc(hora_fim)
                        for idx in range(start_index, end_index + 1):
                            # Se a célula já contém uma tarefa, adiciona a nova tarefa com uma quebra de linha
                            existing_content = tabela.at[tabela.index[idx], dia]
                            if pd.notna(existing_content):
                                tabela.at[tabela.index[idx], dia] = existing_content + f"<br><span style='color:{cor};'>{tarefa}</span>"
                            else:
                                tabela.at[tabela.index[idx], dia] = f"<span style='color:{cor};'>{tarefa}</span>"

        # Exibir tabela com estilo
        st.markdown(tabela.to_html(escape=False, render_links=True), unsafe_allow_html=True)
    else:
        st.info("Nenhuma agenda foi criada ainda.")

# Função principal para gerenciamento
def gerir():
    opcao = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["Criar Nova Agenda", "Selecionar Agenda", "Visualizar Agendas"]
    )
    
    if opcao == "Criar Nova Agenda":
        criar_agenda()
    elif opcao == "Selecionar Agenda":
        utilizador = selecionar_agenda()
        if utilizador:
            gerir_agenda(utilizador)
    elif opcao == "Visualizar Agendas":
        visualizar_agendas()


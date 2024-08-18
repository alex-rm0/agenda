import streamlit as st
import pandas as pd

# Função para criar a tabela de horários
def criar_tabela_horarios():
    dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    horarios = [f"{hora:02d}:00" for hora in range(8, 20)]  # Horário das 08:00 às 19:00

    tabela = pd.DataFrame(index=horarios, columns=dias_da_semana)
    return tabela

# Função para selecionar horários
def selecionar_horarios(tabela):
    for dia in tabela.columns:
        st.write(f"### {dia}")
        for hora in tabela.index:
            if st.checkbox(f"{hora} - {dia}", key=f"{hora}-{dia}"):
                tarefa = st.text_input(f"Tarefa para {hora} - {dia}", key=f"input-{hora}-{dia}")
                tabela.loc[hora, dia] = tarefa

# Função principal
def main():
    st.title("Agenda Semanal Interativa")

    st.write("Selecione os blocos de horários em que deseja adicionar tarefas:")

    # Criar e exibir a tabela de horários
    tabela_horarios = criar_tabela_horarios()

    # Selecionar horários e adicionar tarefas
    selecionar_horarios(tabela_horarios)

    # Mostrar a tabela final com as tarefas
    st.write("### Agenda Atualizada:")
    st.dataframe(tabela_horarios.fillna(""))

if __name__ == "__main__":
    main()

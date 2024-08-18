import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# Função para criar a tabela de horários
def criar_tabela_horarios():
    dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    horarios = [f"{hora:02d}:00" for hora in range(8, 20)]  # Horário das 08:00 às 19:00

    # Cria um DataFrame vazio
    tabela = pd.DataFrame(index=horarios, columns=dias_da_semana)
    return tabela

# Função principal
def main():
    st.title("Agenda Semanal Interativa - Estilo Calendário")

    # Criar e exibir a tabela de horários
    tabela_horarios = criar_tabela_horarios()

    # Configurações do grid
    gb = GridOptionsBuilder.from_dataframe(tabela_horarios)
    gb.configure_default_column(editable=True)  # Permite edição das células
    gb.configure_grid_options(domLayout='normal')

    # Cria o grid interativo
    grid_response = AgGrid(
        tabela_horarios,
        gridOptions=gb.build(),
        editable=True,  # Permite editar a célula diretamente no grid
        theme='blue',  # Estilo do grid
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
    )

    # Obtém a tabela editada
    tabela_editada = grid_response['data']
    st.write("### Agenda Atualizada:")
    st.dataframe(tabela_editada)

    # Salvando a tabela editada em um CSV (opcional)
    if st.button("Salvar Agenda"):
        tabela_editada.to_csv("agenda_semanal.csv", index=True)
        st.success("Agenda salva com sucesso!")

if __name__ == "__main__":
    main()

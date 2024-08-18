def criar_tabela_horarios():
    dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    horarios = [f"{hora:02d}:00" for hora in range(8, 20)]  # Horário das 08:00 às 19:00

    tabela = pd.DataFrame(index=horarios, columns=dias_da_semana)
    return tabela

def gerir():
  return

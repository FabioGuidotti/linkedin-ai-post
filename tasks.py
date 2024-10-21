from crewai import Task

def criar_tarefa_pesquisa(agente):
    return Task(
        description="Pesquise as notícias mais relevantes sobre IA da última semana. Foque em avanços significativos, lançamentos de produtos, descobertas científicas e tendências emergentes.",
        agent=agente,
        expected_output="Uma lista com 5 notícias relevantes sobre IA da última semana, incluindo um breve resumo de cada uma."
    )

def criar_tarefa_escrita(agente):
    return Task(
        description="Com base nas notícias pesquisadas, crie um post envolvente para o LinkedIn que resuma as principais novidades do mundo da IA. O post deve ser informativo, conciso e estimular o engajamento.",
        agent=agente,
        expected_output="Um post para o LinkedIn com no máximo 1300 caracteres, formatado adequadamente e pronto para ser publicado."
    )

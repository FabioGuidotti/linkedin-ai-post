from crewai import Task
from datetime import date, timedelta

def criar_tarefa_pesquisa(agente, data_atual=date.today()):
    data_inicial = data_atual - timedelta(days=7)
    return Task(
        description=f"Pesquise as notícias mais relevantes sobre IA no período de {data_inicial.strftime('%d/%m/%Y')} até {data_atual.strftime('%d/%m/%Y')}. Foque em avanços significativos, lançamentos de produtos, descobertas científicas e tendências emergentes.",
        agent=agente,
        expected_output="Uma lista com 5 notícias relevantes sobre IA do período especificado, incluindo um resumo completo de cada uma e um link de referência para cada notícia."
    )

def criar_tarefa_escrita(agente):
    return Task(
        description="Com base nas notícias pesquisadas, crie um post envolvente para o LinkedIn que resuma as principais novidades do mundo da IA. O post deve ser informativo, conciso e estimular o engajamento.",
        agent=agente,
        expected_output="Um post para o LinkedIn com no máximo 1300 caracteres, formatado adequadamente e pronto para ser publicado e com links para cada notícia pesquisada."
    )

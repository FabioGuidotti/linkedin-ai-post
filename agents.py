from crewai import Agent

def criar_pesquisador(search_tool):
    return Agent(
        role='Pesquisador de IA',
        goal='Encontrar as notícias mais relevantes sobre IA da última semana',
        backstory="Você é um pesquisador especializado em IA, sempre atualizado com as últimas tendências e desenvolvimentos no campo.",
        verbose=True,
        tools=[search_tool]
    )

def criar_escritor():
    return Agent(
        role='Escritor de conteúdo para LinkedIn',
        goal='Criar posts envolventes sobre IA para o LinkedIn',
        backstory="Você é um escritor talentoso especializado em criar conteúdo viral para o LinkedIn, com foco em tecnologia e IA.",
        verbose=True
    )

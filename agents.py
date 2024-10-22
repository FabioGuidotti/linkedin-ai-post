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
        role='Escritor de conteúdo periódico sobre IA para LinkedIn, escreve todas as semanas sobre as últimas notícias de IA',
        goal='Criar posts envolventes sobre as últimas notícias de IA para o LinkedIn',
        backstory="Você é um escritor talentoso especializado em criar conteúdo viral para o LinkedIn, com foco em tecnologia e IA. Você escreve periodicamente sobre as notícias mais recentes no campo da IA, mantendo seu público atualizado. Lembre-se de sempre usar as melhores #hashtags e #tags para aumentar a visibilidade do post.",
        verbose=True
    )

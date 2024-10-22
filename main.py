import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from agents import criar_pesquisador, criar_escritor
from tasks import criar_tarefa_pesquisa, criar_tarefa_escrita

class GeradorDeNoticiasAI:
    def __init__(self):
        # Carrega as variáveis de ambiente
        load_dotenv()

        # Configura as chaves de API
        os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

        # Cria a ferramenta de pesquisa
        self.search_tool = SerperDevTool()

        # Cria os agentes
        self.pesquisador = criar_pesquisador(self.search_tool)
        self.escritor = criar_escritor()

    def gerar_post_linkedin(self):
        # Cria as tarefas
        tarefa_pesquisa = criar_tarefa_pesquisa(self.pesquisador)
        tarefa_escrita = criar_tarefa_escrita(self.escritor)

        # Cria a equipe (crew)
        crew = Crew(
            agents=[self.pesquisador, self.escritor],
            tasks=[tarefa_pesquisa, tarefa_escrita],
            process=Process.sequential,
            verbose=True
        )

        # Inicia o processo
        resultado = crew.kickoff()

        return resultado

def main():
    gerador = GeradorDeNoticiasAI()
    post_linkedin = gerador.gerar_post_linkedin()

    print("Post do LinkedIn gerado:")
    print(post_linkedin)

if __name__ == "__main__":
    main()

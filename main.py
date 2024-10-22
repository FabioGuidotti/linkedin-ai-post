from image_generator import GeradorImagemAI
from news_generator import GeradorDeNoticiasAI
import os
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave de API do OpenAI das variáveis de ambiente
api_key_openai = os.getenv("OPENAI_API_KEY")


# Gera uma notícia
gerador = GeradorDeNoticiasAI()
post_linkedin = gerador.gerar_post_linkedin()

# Adiciona um alerta ao texto, informando que é uma notícia gerada por IA
post_linkedin_final = f"🚨 Conteúdo gerado 100% por inteligência artificial 🚨\n\n{post_linkedin}"

print("Post do LinkedIn gerado:")
print(post_linkedin)

# Cria uma instância da classe GeradorImagemAI
gerador = GeradorImagemAI(api_key_openai)

# Gera uma imagem para o post do LinkedIn
descricao, url_imagem = gerador.gerar_imagem_ai(post_linkedin)

print("Descrição gerada:", descricao)
print("URL da imagem gerada:", url_imagem)

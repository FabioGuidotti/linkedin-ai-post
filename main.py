from image_generator import GeradorImagemAI
from news_generator import GeradorDeNoticiasAI
from linkedin_poster import LinkedInPoster
import os
from dotenv import load_dotenv
import requests


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave de API do OpenAI das variáveis de ambiente
api_key_openai = os.getenv("OPENAI_API_KEY")


# Gera uma notícia
gerador = GeradorDeNoticiasAI()
post_linkedin = gerador.gerar_post_linkedin()

# Adiciona um alerta ao texto, informando que é uma notícia gerada por IA
post_linkedin_final = f"[NOTÍCIAS DO MUNDO DA AI GERADO POR AI]\n\n{post_linkedin}\n\n**Conteúdo gerado 100% por inteligência artificial, as notícias podem conter erros."

print("Post do LinkedIn gerado:")
print(post_linkedin_final)

# Cria uma instância da classe GeradorImagemAI
gerador = GeradorImagemAI(api_key_openai)

# Gera uma imagem para o post do LinkedIn
descricao, url_imagem = gerador.gerar_imagem_ai(post_linkedin)

print("Descrição gerada:", descricao)
print("URL da imagem gerada:", url_imagem)

# baixa a imagem da url e salva localmente
resposta = requests.get(url_imagem)
if resposta.status_code == 200:
    with open("imagem.png", "wb") as f:
        f.write(resposta.content)

    # salva diretorio da imagem
    diretorio_imagem = os.path.join(os.getcwd(), "imagem.png")
    print(f"Imagem salva em: {diretorio_imagem}")
else:
    print(f"Erro ao baixar a imagem: {resposta.status_code}")


# posta no linkedin
poster = LinkedInPoster()

if poster.autenticar():
    resultado = poster.postar_texto_com_imagem(post_linkedin_final, diretorio_imagem)
    print(f"Resultado do post: {resultado}")
else:
    print("Erro ao autenticar no LinkedIn")
import requests
from linkedin_api import Linkedin

# Configurações
CLIENT_ID = 'seu_client_id'
CLIENT_SECRET = 'seu_client_secret'
REDIRECT_URI = 'http://localhost:8000'  # Use uma URL de redirecionamento válida

# Autenticação
api = Linkedin(CLIENT_ID, CLIENT_SECRET)

# Função para criar post com texto e imagem
def criar_post_linkedin(texto, caminho_imagem):
    # Fazer upload da imagem
    imagem_id = api.upload_image(caminho_imagem)

    # Criar o post
    post = {
        "author": f"urn:li:person:{api.get_user_profile()['id']}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": texto
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": "Descrição da imagem"
                        },
                        "media": imagem_id,
                        "title": {
                            "text": "Título da imagem"
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # Enviar o post
    response = api.make_post(post)
    return response

# Exemplo de uso
texto_post = "Este é um post de teste criado com Python e IA!"
caminho_imagem = "caminho/para/sua/imagem.jpg"

resposta = criar_post_linkedin(texto_post, caminho_imagem)
print(f"Post criado com sucesso: {resposta}")
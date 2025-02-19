import requests
from urllib.parse import urlencode
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os

class LinkedInPoster:
    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")    
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.redirect_uri = os.getenv("LINKEDIN_REDIRECT_URI")  # Certifique-se de que esta variável de ambiente use HTTPS
        self.access_token = None
        self.base_url = "https://api.linkedin.com/v2"

    def autenticar(self):
        """
        Realiza o fluxo de autenticação 3-legged OAuth.
        """
        auth_code = self._obter_codigo_autorizacao()
        if not auth_code:
            print("Falha ao obter o código de autorização.")
            return False

        if self._trocar_codigo_por_token(auth_code):
            print("Autenticação 3-legged OAuth concluída com sucesso.")
            return True
        else:
            print("Falha na autenticação 3-legged OAuth.")
            return False

    def _obter_codigo_autorizacao(self):
        """
        Passo 1 do 3-legged OAuth: Obter código de autorização
        """
        auth_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid,profile,w_member_social,email"  
        }
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(auth_params)}"

        print(f"URL de autorização: {auth_url}")
        
        webbrowser.open(auth_url)

        # Use HTTP por padrão
        server = HTTPServer(('localhost', 8000), AuthCodeHandler)
        
        server_thread = threading.Thread(target=server.handle_request)
        server_thread.start()
        server_thread.join()

        if AuthCodeHandler.auth_code:
            print("Código de autorização obtido com sucesso.")
        else:
            print("Falha ao obter o código de autorização.")

        return AuthCodeHandler.auth_code

    def _trocar_codigo_por_token(self, auth_code):
        """
        Passo 2 do 3-legged OAuth: Trocar o código de autorização por um token de acesso
        """
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(token_url, data=data, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            if self.access_token:
                self._configurar_headers()
                return True
            else:
                print("Falha ao obter o token de acesso.")
                return False
        except Exception as e:
            print(f"Erro ao trocar o código por token: {str(e)}")
            return False

    def _configurar_headers(self):
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def _obter_id_pessoa(self):
        try:
            profile_url = f"{self.base_url}/userinfo"
            response = requests.get(profile_url, headers=self.headers)
            response.raise_for_status()
            profile_data = response.json()
            return profile_data.get('sub')
        except Exception as e:
            print(f"Erro ao obter ID da pessoa: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Resposta da API: {e.response.text}")
            return None

    def postar_texto_com_imagem(self, texto, diretorio_imagem):
        try:
            asset = self._fazer_upload_imagem(diretorio_imagem)
            
            if not asset:
                print("Falha ao fazer upload da imagem.")
                return None

            author = self._obter_id_pessoa()
            if not author:
                print("Falha ao obter o ID do autor.")
                return None

            post_url = f"{self.base_url}/ugcPosts"
            
            payload = {
                "author": f"urn:li:person:{author}",
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
                                    "text": "Imagem da postagem"
                                },
                                "media": asset,
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

            response = requests.post(post_url, headers=self.headers, json=payload)
            response.raise_for_status()

            print(f"Postagem realizada com sucesso. ID: {response.headers.get('x-restli-id')}")
            return response.headers.get('x-restli-id')

        except Exception as e:
            print(f"Erro ao fazer a postagem: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Resposta da API: {e.response.text}")
            return None

    def _fazer_upload_imagem(self, diretorio_imagem):
        try:
            init_url = f"{self.base_url}/assets?action=registerUpload"
            init_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{self._obter_id_pessoa()}",
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }
            init_response = requests.post(init_url, headers=self.headers, json=init_payload)
            init_response.raise_for_status()
            init_data = init_response.json()

            upload_url = init_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            with open(diretorio_imagem, 'rb') as image:
                files = {'file': image}
                upload_response = requests.post(upload_url, files=files)
                upload_response.raise_for_status()

            return init_data['value']['asset']

        except Exception as e:
            print(f"Erro ao fazer upload da imagem: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Resposta da API: {e.response.text}")
            return None

class AuthCodeHandler(BaseHTTPRequestHandler):
    auth_code = None

    def do_GET(self):
        query = self.path.split('?', 1)[-1]
        params = dict(param.split('=') for param in query.split('&'))
        AuthCodeHandler.auth_code = params.get('code')
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Autorizacao concluida. Voce pode fechar esta janela.")
        print(f"Código de autorização recebido: {AuthCodeHandler.auth_code}")

    def log_message(self, format, *args):
        return  # Silencia os logs do servidor


## testes locais
'''
poster = LinkedInPoster()

if poster.autenticar():
    resultado = poster.postar_texto_com_imagem("teste testes", "C:\\GIT\\linkedin-ai-post\\imagem.png")
    print(f"Resultado do post: {resultado}")
else:
    print("Erro ao autenticar no LinkedIn")
'''

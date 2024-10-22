from openai import OpenAI
import requests

class GeradorImagemAI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def gerar_descricao(self, texto):
        prompt = f"Crie uma descrição detalhada de uma imagem com poucos elementos visuais, a descrição será usado no modelo DALL-E 3 para gerar a imagem, por isso deve ter no maximo 500 caracteres. Use o seguinte texto para criar a descrição: '{texto}'"
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente criativo especializado criar artes para o LinkedIn."},
                {"role": "user", "content": prompt}
            ]
        )
        descricao = response.choices[0].message.content.strip()
        return descricao[:1000]  # Garante que a descrição não ultrapasse 1000 caracteres

    def gerar_imagem(self, descricao):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=descricao,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        
        print(f"Imagem gerada: {image_url}")

        return image_url

    def gerar_imagem_ai(self, texto):
        descricao = self.gerar_descricao(texto)
        imagem = self.gerar_imagem(descricao)
        return descricao, imagem

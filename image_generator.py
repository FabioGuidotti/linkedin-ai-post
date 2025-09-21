from openai import OpenAI
import requests
import os
import base64
from PIL import Image
from io import BytesIO

class GeradorImagemAI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def gerar_descricao(self, texto):
        prompt = f"""Crie uma imagem para uma postagem no LinkedIn com base no seguinte texto de publicação:

"{texto}"

A imagem deve refletir o tema principal do texto. Usar poucos elementos visuais, ter um estilo adequado para redes sociais voltadas ao mundo da tecnologia."""
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é uma IA especializada em gerar  descrições de imagens cativantes e profissionais para acompanhar publicações em redes sociais. Seu trabalho interpretar profundamente o texto fornecido e criar imagens que complementem o texto fornecido, atraindo a atenção de profissionais e se adequando ao estilo corporativo do LinkedIn. Suas criações devem ser alinhadas com a mensagem da publicação. A imagem deve ser criativa e colorida."},
                {"role": "user", "content": prompt}
            ]
        )
        descricao = response.choices[0].message.content.strip()

        print(f"Descrição gerada: {descricao}")

        return descricao[:1000]  # Garante que a descrição não ultrapasse 1000 caracteres

    def gerar_imagem(self, descricao):
        response = self.client.images.generate(
            model="gpt-image-1",
            prompt=descricao,
            size="1024x1024"
        )
        image_data = base64.b64decode(response.data[0].b64_json)
        image = Image.open(BytesIO(image_data))
        
        # Salvar a imagem localmente
        output_path = "imagem_gerada.png"
        image.save(output_path)
        
        print(f"Imagem gerada e salva em: {output_path}")

        return output_path

    def gerar_imagem_ai(self, texto):
        descricao = self.gerar_descricao(texto)
        imagem = self.gerar_imagem(descricao)
        return descricao, imagem

if __name__ == "__main__":
    gerador = GeradorImagemAI(api_key=os.getenv("OPENAI_API_KEY"))
    texto = "Como a IA está mudando a forma como as empresas funcionam"
    descricao, imagem = gerador.gerar_imagem_ai(texto)

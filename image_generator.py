from openai import OpenAI
import requests

class GeradorImagemAI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def gerar_descricao(self, texto):
        prompt = f"""Crie uma imagem para uma postagem no LinkedIn com base no seguinte texto de publicação:

"{texto}"

A imagem deve refletir o tema principal do texto. Usar poucos elementos visuais, ter um estilo adequado para redes sociais voltadas ao mundo da tecnologia."""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é uma IA especializada em gerar  descrições deimagens cativantes e profissionais para acompanhar publicações em redes sociais. Seu trabalho interpretar profundamente o texto fornecido e criar imagens que complementem o texto fornecido, atraindo a atenção de profissionais e se adequando ao estilo corporativo do LinkedIn. Suas criações devem ser alinhadas com a mensagem da publicação. A imagem não podem conter textos."},
                {"role": "user", "content": prompt}
            ]
        )
        descricao = response.choices[0].message.content.strip()

        print(f"Descrição gerada: {descricao}")

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

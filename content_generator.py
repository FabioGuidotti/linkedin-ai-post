#!/usr/bin/env python3
"""
Módulo para geração de conteúdo (notícias e imagens)
Separa a lógica de geração de conteúdo da postagem
"""

from news_generator import GeradorDeNoticiasAI
from image_generator import GeradorImagemAI
from history_manager import HistoryManager
import os
from datetime import datetime

class ContentGenerator:
    def __init__(self, api_key_openai):
        self.api_key_openai = api_key_openai
        self.history_manager = HistoryManager()
        
        # Inicializa geradores
        self.news_generator = GeradorDeNoticiasAI()
        self.image_generator = GeradorImagemAI(api_key_openai)
    
    def generate_content(self, save_to_history=True):
        """
        Gera conteúdo completo (notícias + imagem)
        
        Args:
            save_to_history (bool): Se deve salvar no histórico
            
        Returns:
            dict: Dicionário com todo o conteúdo gerado
        """
        print("🚀 Iniciando geração de conteúdo...")
        
        # Gera notícias
        print("📰 Gerando notícias sobre IA...")
        post_linkedin = self.news_generator.gerar_post_linkedin()
        
        # Adiciona alerta de IA
        post_linkedin_final = f"[NOTÍCIAS DO MUNDO DA AI GERADO POR AI]\n\n{post_linkedin}\n\n**Conteúdo gerado 100% por inteligência artificial, as notícias podem conter erros."
        
        print("✅ Post do LinkedIn gerado:")
        print("-" * 50)
        print(post_linkedin_final)
        print("-" * 50)
        
        # Gera imagem
        print("🎨 Gerando imagem para o post...")
        descricao, path_imagem = self.image_generator.gerar_imagem_ai(post_linkedin)
        
        print("✅ Descrição da imagem gerada:")
        print(descricao)
        
        # Cria pasta para histórico se solicitado
        post_folder = None
        if save_to_history:
            print("📁 Criando pasta para histórico...")
            post_folder = self.history_manager.create_post_folder()
            print(f"📂 Pasta criada: {post_folder}")
            
            # Salva no histórico
            diretorio_imagem = os.path.join(os.getcwd(), path_imagem)
            self.history_manager.save_post_content(
                post_folder=post_folder,
                post_text=post_linkedin_final,
                image_path=diretorio_imagem,
                description=descricao
            )
            print(f"💾 Conteúdo salvo em: {post_folder}")
        
        # Retorna conteúdo gerado
        content = {
            "post_text": post_linkedin_final,
            "original_post": post_linkedin,
            "image_description": descricao,
            "image_path": path_imagem,
            "full_image_path": os.path.join(os.getcwd(), path_imagem),
            "post_folder": post_folder,
            "generated_at": datetime.now().isoformat()
        }
        
        print(f"🖼️ Imagem salva em: {content['full_image_path']}")
        print("✅ Conteúdo gerado com sucesso!")
        
        return content
    
    def generate_news_only(self):
        """Gera apenas as notícias, sem imagem"""
        print("📰 Gerando apenas notícias...")
        post_linkedin = self.news_generator.gerar_post_linkedin()
        post_linkedin_final = f"[NOTÍCIAS DO MUNDO DA AI GERADO POR AI]\n\n{post_linkedin}\n\n**Conteúdo gerado 100% por inteligência artificial, as notícias podem conter erros."
        
        print("✅ Notícias geradas:")
        print("-" * 50)
        print(post_linkedin_final)
        print("-" * 50)
        
        return {
            "post_text": post_linkedin_final,
            "original_post": post_linkedin,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_image_only(self, post_text):
        """Gera apenas a imagem para um texto específico"""
        print("🎨 Gerando imagem...")
        descricao, path_imagem = self.image_generator.gerar_imagem_ai(post_text)
        
        print("✅ Imagem gerada:")
        print(f"📝 Descrição: {descricao}")
        print(f"🖼️ Caminho: {os.path.join(os.getcwd(), path_imagem)}")
        
        return {
            "image_description": descricao,
            "image_path": path_imagem,
            "full_image_path": os.path.join(os.getcwd(), path_imagem),
            "generated_at": datetime.now().isoformat()
        }
    
    def get_history(self):
        """Retorna o histórico de posts"""
        return self.history_manager.list_posts()
    
    def get_post_content(self, folder_name):
        """Recupera conteúdo de um post específico"""
        return self.history_manager.get_post_content(folder_name)

if __name__ == "__main__":
    # Teste do módulo
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY não encontrada no .env")
        exit(1)
    
    generator = ContentGenerator(api_key)
    
    print("🧪 Testando geração de conteúdo...")
    content = generator.generate_content(save_to_history=True)
    
    print("\n📊 Resumo do conteúdo gerado:")
    print(f"📝 Tamanho do post: {len(content['post_text'])} caracteres")
    print(f"🖼️ Imagem: {content['image_path']}")
    print(f"📁 Pasta: {content['post_folder']}")

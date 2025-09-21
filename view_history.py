#!/usr/bin/env python3
"""
Script para visualizar e gerenciar o histórico de postagens
"""

from history_manager import HistoryManager
import argparse
from datetime import datetime

def list_posts():
    """Lista todos os posts do histórico"""
    history = HistoryManager()
    posts = history.list_posts()
    
    if not posts:
        print("📭 Nenhum post encontrado no histórico.")
        return
    
    print(f"📊 Histórico de Postagens ({len(posts)} posts encontrados):")
    print("=" * 80)
    
    for i, post in enumerate(posts, 1):
        metadata = post["metadata"]
        created_at = datetime.fromisoformat(metadata["created_at"])
        formatted_date = created_at.strftime("%d/%m/%Y %H:%M:%S")
        
        print(f"\n{i}. {post['folder']}")
        print(f"   📅 Data: {formatted_date}")
        print(f"   📝 Tamanho: {metadata['post_text_length']} caracteres")
        print(f"   🖼️ Tem imagem: {'Sim' if metadata['has_image'] else 'Não'}")
        print(f"   🔗 Postado no LinkedIn: {'Sim' if metadata.get('linkedin_posted', False) else 'Não'}")
        print(f"   📁 Pasta: {post['path']}")

def view_post(folder_name):
    """Visualiza o conteúdo de um post específico"""
    history = HistoryManager()
    base_dir = history.base_dir
    post_folder = base_dir / folder_name
    
    if not post_folder.exists():
        print(f"❌ Pasta '{folder_name}' não encontrada.")
        return
    
    content = history.get_post_content(post_folder)
    
    print(f"📖 Conteúdo do Post: {folder_name}")
    print("=" * 80)
    
    if "metadata" in content:
        metadata = content["metadata"]
        created_at = datetime.fromisoformat(metadata["created_at"])
        formatted_date = created_at.strftime("%d/%m/%Y %H:%M:%S")
        print(f"📅 Data: {formatted_date}")
        print(f"📝 Tamanho: {metadata['post_text_length']} caracteres")
        print(f"🖼️ Tem imagem: {'Sim' if metadata['has_image'] else 'Não'}")
        print(f"🔗 Postado no LinkedIn: {'Sim' if metadata.get('linkedin_posted', False) else 'Não'}")
        if metadata.get('linkedin_result'):
            print(f"📋 Resultado LinkedIn: {metadata['linkedin_result']}")
        print()
    
    if "post_text" in content:
        print("📝 TEXTO DO POST:")
        print("-" * 40)
        print(content["post_text"])
        print("-" * 40)
    
    if "image_description" in content:
        print("\n🎨 DESCRIÇÃO DA IMAGEM:")
        print("-" * 40)
        print(content["image_description"])
        print("-" * 40)
    
    if "images" in content and content["images"]:
        print(f"\n🖼️ IMAGENS ({len(content['images'])}):")
        for img in content["images"]:
            print(f"   - {img}")

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de Histórico de Postagens")
    parser.add_argument("--list", "-l", action="store_true", help="Lista todos os posts")
    parser.add_argument("--view", "-v", type=str, help="Visualiza um post específico (nome da pasta)")
    parser.add_argument("--latest", action="store_true", help="Visualiza o post mais recente")
    
    args = parser.parse_args()
    
    if args.list:
        list_posts()
    elif args.view:
        view_post(args.view)
    elif args.latest:
        history = HistoryManager()
        posts = history.list_posts()
        if posts:
            latest_post = posts[0]  # O mais recente é o primeiro da lista
            view_post(latest_post["folder"])
        else:
            print("📭 Nenhum post encontrado no histórico.")
    else:
        # Se nenhum argumento for fornecido, lista todos os posts
        list_posts()

if __name__ == "__main__":
    main()

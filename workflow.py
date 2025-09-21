#!/usr/bin/env python3
"""
Script de workflow completo para geração e publicação de conteúdo
Usa módulos separados para geração de conteúdo e publicação
"""

import os
import argparse
from dotenv import load_dotenv
from content_generator import ContentGenerator
from linkedin_publisher import LinkedInPublisher
from view_history import list_posts, view_post

def generate_and_publish(api_key, save_to_history=True, publish=True):
    """
    Gera conteúdo e publica no LinkedIn
    
    Args:
        api_key (str): Chave da API OpenAI
        save_to_history (bool): Se deve salvar no histórico
        publish (bool): Se deve publicar no LinkedIn
    """
    print("🚀 Iniciando workflow completo...")
    
    # Gera conteúdo
    generator = ContentGenerator(api_key)
    content = generator.generate_content(save_to_history=save_to_history)
    
    if not content:
        print("❌ Falha na geração de conteúdo")
        return False
    
    # Publica se solicitado
    if publish:
        publisher = LinkedInPublisher()
        result = publisher.publish_content(content, update_history=True)
        
        if result["success"]:
            print("🎉 Workflow concluído com sucesso!")
            return True
        else:
            print(f"❌ Falha na publicação: {result.get('error', 'Erro desconhecido')}")
            return False
    else:
        print("✅ Conteúdo gerado (não publicado)")
        return True

def generate_only(api_key, save_to_history=True):
    """Gera apenas conteúdo, sem publicar"""
    print("📝 Gerando apenas conteúdo...")
    
    generator = ContentGenerator(api_key)
    content = generator.generate_content(save_to_history=save_to_history)
    
    if content:
        print("✅ Conteúdo gerado com sucesso!")
        return True
    else:
        print("❌ Falha na geração de conteúdo")
        return False

def publish_from_history(folder_name):
    """Publica conteúdo de um post do histórico"""
    print(f"📖 Publicando post do histórico: {folder_name}")
    
    publisher = LinkedInPublisher()
    result = publisher.publish_from_history(folder_name)
    
    if result["success"]:
        print("✅ Post publicado com sucesso!")
        return True
    else:
        print(f"❌ Falha na publicação: {result.get('error', 'Erro desconhecido')}")
        return False

def publish_unpublished():
    """Publica todos os posts não publicados"""
    print("📋 Publicando posts não publicados...")
    
    publisher = LinkedInPublisher()
    unpublished = publisher.list_unpublished_posts()
    
    if not unpublished:
        print("📭 Nenhum post não publicado encontrado")
        return True
    
    print(f"📊 Encontrados {len(unpublished)} posts não publicados")
    
    success_count = 0
    for post in unpublished:
        print(f"\n📝 Publicando: {post['folder']}")
        result = publisher.publish_from_history(post['folder'])
        
        if result["success"]:
            success_count += 1
            print("✅ Publicado com sucesso!")
        else:
            print(f"❌ Falha: {result.get('error', 'Erro desconhecido')}")
    
    print(f"\n📊 Resultado: {success_count}/{len(unpublished)} posts publicados")
    return success_count == len(unpublished)

def show_status():
    """Mostra status dos posts"""
    print("📊 Status dos posts:")
    
    publisher = LinkedInPublisher()
    posts = publisher.history_manager.list_posts()
    
    if not posts:
        print("📭 Nenhum post encontrado")
        return
    
    published = 0
    unpublished = 0
    
    for post in posts:
        metadata = post["metadata"]
        if metadata.get("linkedin_posted", False):
            published += 1
        else:
            unpublished += 1
    
    print(f"✅ Publicados: {published}")
    print(f"⏳ Não publicados: {unpublished}")
    print(f"📊 Total: {len(posts)}")

def main():
    parser = argparse.ArgumentParser(description="Workflow de Geração e Publicação de Conteúdo")
    
    # Comandos principais
    parser.add_argument("--generate", "-g", action="store_true", 
                       help="Gera conteúdo e publica no LinkedIn")
    parser.add_argument("--generate-only", action="store_true", 
                       help="Gera apenas conteúdo, sem publicar")
    parser.add_argument("--publish", "-p", type=str, 
                       help="Publica post específico do histórico (nome da pasta)")
    parser.add_argument("--publish-all", action="store_true", 
                       help="Publica todos os posts não publicados")
    
    # Comandos de visualização
    parser.add_argument("--list", "-l", action="store_true", 
                       help="Lista todos os posts")
    parser.add_argument("--view", "-v", type=str, 
                       help="Visualiza post específico")
    parser.add_argument("--latest", action="store_true", 
                       help="Visualiza post mais recente")
    parser.add_argument("--status", action="store_true", 
                       help="Mostra status dos posts")
    
    # Opções
    parser.add_argument("--no-history", action="store_true", 
                       help="Não salva no histórico")
    parser.add_argument("--no-publish", action="store_true", 
                       help="Não publica no LinkedIn")
    parser.add_argument("--menu", "-m", action="store_true", 
                       help="Abre menu interativo")
    
    args = parser.parse_args()
    
    # Carrega variáveis de ambiente
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Se --menu foi especificado ou nenhum argumento foi passado, abre menu interativo
    if args.menu or len(sys.argv) == 1:
        from menu_interativo import InteractiveMenu
        menu = InteractiveMenu()
        menu.run()
        return
    
    if not api_key and (args.generate or args.generate_only):
        print("❌ OPENAI_API_KEY não encontrada no .env")
        return
    
    # Executa comandos
    if args.generate:
        generate_and_publish(api_key, 
                           save_to_history=not args.no_history, 
                           publish=not args.no_publish)
    
    elif args.generate_only:
        generate_only(api_key, save_to_history=not args.no_history)
    
    elif args.publish:
        publish_from_history(args.publish)
    
    elif args.publish_all:
        publish_unpublished()
    
    elif args.list:
        list_posts()
    
    elif args.view:
        view_post(args.view)
    
    elif args.latest:
        from view_history import main as view_main
        view_main()
    
    elif args.status:
        show_status()
    
    else:
        # Comportamento padrão: abre menu interativo
        from menu_interativo import InteractiveMenu
        menu = InteractiveMenu()
        menu.run()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script interativo para geração e publicação de conteúdo
Menu com opções numeradas para facilitar o uso
"""

import os
import sys
from dotenv import load_dotenv
from content_generator import ContentGenerator
from linkedin_publisher import LinkedInPublisher
from view_history import list_posts, view_post
from datetime import datetime

class InteractiveMenu:
    def __init__(self):
        # Carrega variáveis de ambiente
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Inicializa módulos se API key estiver disponível
        self.generator = None
        self.publisher = None
        
        if self.api_key:
            self.generator = ContentGenerator(self.api_key)
            self.publisher = LinkedInPublisher()
    
    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        """Mostra cabeçalho do menu"""
        print("=" * 60)
        print("🤖 SISTEMA DE GERAÇÃO E PUBLICAÇÃO DE CONTEÚDO IA")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
    
    def show_main_menu(self):
        """Mostra menu principal"""
        print("📋 MENU PRINCIPAL")
        print("-" * 30)
        print("1. 🚀 Gerar e Publicar Post Completo")
        print("2. 📝 Gerar Apenas Conteúdo (sem publicar)")
        print("3. 🎨 Gerar Apenas Notícias (sem imagem)")
        print("4. 🖼️ Gerar Apenas Imagem (para texto existente)")
        print("5. 📤 Publicar Post do Histórico")
        print("6. 📤 Publicar Todos os Posts Não Publicados")
        print("7. 📊 Ver Status dos Posts")
        print("8. 📋 Listar Posts do Histórico")
        print("9. 👁️ Visualizar Post Específico")
        print("10. 👁️ Ver Post Mais Recente")
        print("11. ⚙️ Configurações")
        print("0. 🚪 Sair")
        print("-" * 30)
    
    def get_user_choice(self, max_option):
        """Obtém escolha do usuário"""
        while True:
            try:
                choice = input(f"👉 Escolha uma opção (0-{max_option}): ").strip()
                choice = int(choice)
                if 0 <= choice <= max_option:
                    return choice
                else:
                    print(f"❌ Opção inválida! Digite um número entre 0 e {max_option}")
            except ValueError:
                print("❌ Digite um número válido!")
            except KeyboardInterrupt:
                print("\n👋 Saindo...")
                sys.exit(0)
    
    def wait_for_enter(self):
        """Aguarda usuário pressionar Enter"""
        input("\n⏸️ Pressione Enter para continuar...")
    
    def option_1_generate_and_publish(self):
        """Opção 1: Gerar e publicar post completo"""
        print("\n🚀 GERANDO E PUBLICANDO POST COMPLETO")
        print("-" * 40)
        
        if not self.generator:
            print("❌ OPENAI_API_KEY não encontrada!")
            return
        
        try:
            # Gera conteúdo
            content = self.generator.generate_content(save_to_history=True)
            
            if not content:
                print("❌ Falha na geração de conteúdo")
                return
            
            # Publica
            result = self.publisher.publish_content(content, update_history=True)
            
            if result["success"]:
                print("\n🎉 Post gerado e publicado com sucesso!")
                print(f"📁 Salvo em: {content['post_folder']}")
            else:
                print(f"\n❌ Falha na publicação: {result.get('error', 'Erro desconhecido')}")
                print("💡 Conteúdo foi salvo no histórico mesmo com falha na publicação")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_2_generate_only(self):
        """Opção 2: Gerar apenas conteúdo"""
        print("\n📝 GERANDO APENAS CONTEÚDO")
        print("-" * 35)
        
        if not self.generator:
            print("❌ OPENAI_API_KEY não encontrada!")
            return
        
        try:
            content = self.generator.generate_content(save_to_history=True)
            
            if content:
                print("\n✅ Conteúdo gerado com sucesso!")
                print(f"📁 Salvo em: {content['post_folder']}")
                print(f"📝 Tamanho: {len(content['post_text'])} caracteres")
                print(f"🖼️ Imagem: {content['image_path']}")
            else:
                print("❌ Falha na geração de conteúdo")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_3_generate_news_only(self):
        """Opção 3: Gerar apenas notícias"""
        print("\n📰 GERANDO APENAS NOTÍCIAS")
        print("-" * 35)
        
        if not self.generator:
            print("❌ OPENAI_API_KEY não encontrada!")
            return
        
        try:
            content = self.generator.generate_news_only()
            
            print("\n✅ Notícias geradas com sucesso!")
            print(f"📝 Tamanho: {len(content['post_text'])} caracteres")
            print("\n📄 CONTEÚDO GERADO:")
            print("-" * 30)
            print(content['post_text'])
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_4_generate_image_only(self):
        """Opção 4: Gerar apenas imagem"""
        print("\n🎨 GERANDO APENAS IMAGEM")
        print("-" * 35)
        
        if not self.generator:
            print("❌ OPENAI_API_KEY não encontrada!")
            return
        
        print("📝 Digite o texto para gerar a imagem:")
        text = input("👉 Texto: ").strip()
        
        if not text:
            print("❌ Texto não pode estar vazio!")
            return
        
        try:
            content = self.generator.generate_image_only(text)
            
            print("\n✅ Imagem gerada com sucesso!")
            print(f"🖼️ Caminho: {content['full_image_path']}")
            print(f"📝 Descrição: {content['image_description']}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_5_publish_from_history(self):
        """Opção 5: Publicar post do histórico"""
        print("\n📤 PUBLICAR POST DO HISTÓRICO")
        print("-" * 40)
        
        if not self.publisher:
            print("❌ LinkedInPublisher não inicializado!")
            return
        
        # Lista posts disponíveis
        posts = self.publisher.history_manager.list_posts()
        
        if not posts:
            print("📭 Nenhum post encontrado no histórico")
            return
        
        print("📋 Posts disponíveis:")
        for i, post in enumerate(posts[:10], 1):  # Mostra apenas os 10 mais recentes
            metadata = post["metadata"]
            created_at = datetime.fromisoformat(metadata["created_at"])
            formatted_date = created_at.strftime("%d/%m/%Y %H:%M")
            status = "✅ Publicado" if metadata.get("linkedin_posted", False) else "⏳ Não publicado"
            print(f"  {i}. {post['folder']} - {formatted_date} - {status}")
        
        print(f"  {len(posts) + 1}. 🔙 Voltar")
        
        choice = self.get_user_choice(len(posts) + 1)
        
        if choice == len(posts) + 1:
            return
        
        selected_post = posts[choice - 1]
        
        try:
            result = self.publisher.publish_from_history(selected_post['folder'])
            
            if result["success"]:
                print("\n✅ Post publicado com sucesso!")
            else:
                print(f"\n❌ Falha na publicação: {result.get('error', 'Erro desconhecido')}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def option_6_publish_all_unpublished(self):
        """Opção 6: Publicar todos os não publicados"""
        print("\n📤 PUBLICANDO TODOS OS POSTS NÃO PUBLICADOS")
        print("-" * 50)
        
        if not self.publisher:
            print("❌ LinkedInPublisher não inicializado!")
            return
        
        unpublished = self.publisher.list_unpublished_posts()
        
        if not unpublished:
            print("📭 Nenhum post não publicado encontrado")
            return
        
        print(f"📊 Encontrados {len(unpublished)} posts não publicados")
        print("⚠️ Deseja continuar? (s/N)")
        
        confirm = input("👉 ").strip().lower()
        if confirm not in ['s', 'sim', 'y', 'yes']:
            print("❌ Operação cancelada")
            return
        
        success_count = 0
        for i, post in enumerate(unpublished, 1):
            print(f"\n📝 Publicando {i}/{len(unpublished)}: {post['folder']}")
            
            try:
                result = self.publisher.publish_from_history(post['folder'])
                
                if result["success"]:
                    success_count += 1
                    print("✅ Publicado com sucesso!")
                else:
                    print(f"❌ Falha: {result.get('error', 'Erro desconhecido')}")
                    
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        print(f"\n📊 Resultado: {success_count}/{len(unpublished)} posts publicados")
    
    def option_7_show_status(self):
        """Opção 7: Ver status dos posts"""
        print("\n📊 STATUS DOS POSTS")
        print("-" * 25)
        
        if not self.publisher:
            print("❌ LinkedInPublisher não inicializado!")
            return
        
        posts = self.publisher.history_manager.list_posts()
        
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
        
        if posts:
            print(f"\n📅 Último post: {posts[0]['folder']}")
            last_metadata = posts[0]['metadata']
            created_at = datetime.fromisoformat(last_metadata["created_at"])
            print(f"🕐 Data: {created_at.strftime('%d/%m/%Y %H:%M:%S')}")
    
    def option_8_list_posts(self):
        """Opção 8: Listar posts do histórico"""
        print("\n📋 LISTANDO POSTS DO HISTÓRICO")
        print("-" * 40)
        list_posts()
    
    def option_9_view_specific_post(self):
        """Opção 9: Visualizar post específico"""
        print("\n👁️ VISUALIZAR POST ESPECÍFICO")
        print("-" * 35)
        
        if not self.publisher:
            print("❌ LinkedInPublisher não inicializado!")
            return
        
        posts = self.publisher.history_manager.list_posts()
        
        if not posts:
            print("📭 Nenhum post encontrado no histórico")
            return
        
        print("📋 Posts disponíveis:")
        for i, post in enumerate(posts[:10], 1):  # Mostra apenas os 10 mais recentes
            metadata = post["metadata"]
            created_at = datetime.fromisoformat(metadata["created_at"])
            formatted_date = created_at.strftime("%d/%m/%Y %H:%M")
            print(f"  {i}. {post['folder']} - {formatted_date}")
        
        print(f"  {len(posts) + 1}. 🔙 Voltar")
        
        choice = self.get_user_choice(len(posts) + 1)
        
        if choice == len(posts) + 1:
            return
        
        selected_post = posts[choice - 1]
        view_post(selected_post['folder'])
    
    def option_10_view_latest_post(self):
        """Opção 10: Ver post mais recente"""
        print("\n👁️ POST MAIS RECENTE")
        print("-" * 25)
        
        if not self.publisher:
            print("❌ LinkedInPublisher não inicializado!")
            return
        
        posts = self.publisher.history_manager.list_posts()
        
        if not posts:
            print("📭 Nenhum post encontrado no histórico")
            return
        
        latest_post = posts[0]  # O mais recente é o primeiro
        view_post(latest_post['folder'])
    
    def option_11_settings(self):
        """Opção 11: Configurações"""
        print("\n⚙️ CONFIGURAÇÕES")
        print("-" * 20)
        
        print(f"🔑 OPENAI_API_KEY: {'✅ Configurada' if self.api_key else '❌ Não configurada'}")
        
        if self.publisher:
            unpublished = self.publisher.list_unpublished_posts()
            print(f"📊 Posts não publicados: {len(unpublished)}")
        
        print("\n📁 Estrutura de pastas:")
        print("  - historico_posts/ (histórico de posts)")
        print("  - imagem_gerada.png (imagem atual)")
        
        print("\n🔧 Para configurar variáveis de ambiente:")
        print("  - Crie um arquivo .env")
        print("  - Adicione: OPENAI_API_KEY=sua_chave")
        print("  - Adicione: SERPER_API_KEY=sua_chave")
    
    def run(self):
        """Executa o menu principal"""
        while True:
            self.clear_screen()
            self.show_header()
            self.show_main_menu()
            
            choice = self.get_user_choice(11)
            
            if choice == 0:
                print("\n👋 Obrigado por usar o sistema!")
                break
            elif choice == 1:
                self.option_1_generate_and_publish()
            elif choice == 2:
                self.option_2_generate_only()
            elif choice == 3:
                self.option_3_generate_news_only()
            elif choice == 4:
                self.option_4_generate_image_only()
            elif choice == 5:
                self.option_5_publish_from_history()
            elif choice == 6:
                self.option_6_publish_all_unpublished()
            elif choice == 7:
                self.option_7_show_status()
            elif choice == 8:
                self.option_8_list_posts()
            elif choice == 9:
                self.option_9_view_specific_post()
            elif choice == 10:
                self.option_10_view_latest_post()
            elif choice == 11:
                self.option_11_settings()
            
            self.wait_for_enter()

def main():
    """Função principal"""
    try:
        menu = InteractiveMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n👋 Saindo...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Módulo para publicação no LinkedIn
Separa a lógica de postagem da geração de conteúdo
"""

from linkedin_poster import LinkedInPoster
from history_manager import HistoryManager
import json
from pathlib import Path

class LinkedInPublisher:
    def __init__(self):
        self.poster = LinkedInPoster()
        self.history_manager = HistoryManager()
    
    def publish_content(self, content, update_history=True):
        """
        Publica conteúdo no LinkedIn
        
        Args:
            content (dict): Conteúdo gerado pelo ContentGenerator
            update_history (bool): Se deve atualizar o histórico
            
        Returns:
            dict: Resultado da publicação
        """
        print("🔗 Iniciando publicação no LinkedIn...")
        
        # Verifica se tem conteúdo necessário
        if not content.get("post_text"):
            return {
                "success": False,
                "error": "Nenhum texto de post fornecido"
            }
        
        # Tenta autenticar
        if not self.poster.autenticar():
            result = {
                "success": False,
                "error": "Falha na autenticação do LinkedIn"
            }
            print("❌ Erro ao autenticar no LinkedIn")
            return result
        
        # Publica o conteúdo
        image_path = content.get("full_image_path") if content.get("image_path") else None
        
        try:
            if image_path:
                print("📝 Publicando post com imagem...")
                resultado = self.poster.postar_texto_com_imagem(
                    content["post_text"], 
                    image_path
                )
            else:
                print("📝 Publicando post apenas com texto...")
                resultado = self.poster.postar_texto(content["post_text"])
            
            result = {
                "success": True,
                "result": resultado,
                "published_at": self._get_current_timestamp()
            }
            
            print(f"✅ Post publicado com sucesso!")
            print(f"📋 Resultado: {resultado}")
            
        except Exception as e:
            result = {
                "success": False,
                "error": f"Erro na publicação: {str(e)}"
            }
            print(f"❌ Erro na publicação: {e}")
        
        # Atualiza histórico se solicitado
        if update_history and content.get("post_folder"):
            self._update_history_metadata(content["post_folder"], result)
        
        return result
    
    def publish_from_history(self, folder_name):
        """
        Publica conteúdo de um post do histórico
        
        Args:
            folder_name (str): Nome da pasta do histórico
            
        Returns:
            dict: Resultado da publicação
        """
        print(f"📖 Carregando conteúdo do histórico: {folder_name}")
        
        # Constrói o caminho completo da pasta
        post_folder = self.history_manager.base_dir / folder_name
        
        # Carrega conteúdo do histórico
        content = self.history_manager.get_post_content(post_folder)
        
        if not content.get("post_text"):
            return {
                "success": False,
                "error": f"Post '{folder_name}' não encontrado ou sem texto"
            }
        
        # Prepara conteúdo para publicação
        publish_content = {
            "post_text": content["post_text"],
            "image_path": content["images"][0] if content.get("images") else None,
            "full_image_path": content["images"][0] if content.get("images") else None,
            "post_folder": folder_name
        }
        
        # Publica
        result = self.publish_content(publish_content, update_history=True)
        
        return result
    
    def _update_history_metadata(self, post_folder, publish_result):
        """Atualiza metadados do histórico com resultado da publicação"""
        try:
            metadata_file = Path(post_folder) / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                
                metadata["linkedin_posted"] = publish_result["success"]
                metadata["linkedin_result"] = publish_result.get("result", publish_result.get("error", ""))
                metadata["linkedin_published_at"] = publish_result.get("published_at", "")
                
                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                print(f"📝 Metadados atualizados em: {post_folder}")
        except Exception as e:
            print(f"⚠️ Erro ao atualizar metadados: {e}")
    
    def _get_current_timestamp(self):
        """Retorna timestamp atual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_publishing_status(self, folder_name):
        """
        Verifica status de publicação de um post
        
        Args:
            folder_name (str): Nome da pasta do histórico
            
        Returns:
            dict: Status da publicação
        """
        post_folder = self.history_manager.base_dir / folder_name
        content = self.history_manager.get_post_content(post_folder)
        metadata = content.get("metadata", {})
        
        return {
            "folder": folder_name,
            "posted": metadata.get("linkedin_posted", False),
            "result": metadata.get("linkedin_result", ""),
            "published_at": metadata.get("linkedin_published_at", ""),
            "has_content": bool(content.get("post_text"))
        }
    
    def list_unpublished_posts(self):
        """Lista posts que ainda não foram publicados"""
        posts = self.history_manager.list_posts()
        unpublished = []
        
        for post in posts:
            metadata = post["metadata"]
            if not metadata.get("linkedin_posted", False):
                unpublished.append({
                    "folder": post["folder"],
                    "created_at": metadata["created_at"],
                    "has_image": metadata.get("has_image", False)
                })
        
        return unpublished

if __name__ == "__main__":
    # Teste do módulo
    publisher = LinkedInPublisher()
    
    print("🧪 Testando módulo de publicação...")
    
    # Lista posts não publicados
    unpublished = publisher.list_unpublished_posts()
    print(f"📋 Posts não publicados: {len(unpublished)}")
    
    for post in unpublished:
        print(f"  - {post['folder']} ({post['created_at']})")

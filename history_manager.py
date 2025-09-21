import os
import json
from datetime import datetime
from pathlib import Path

class HistoryManager:
    def __init__(self, base_dir="historico_posts"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def create_post_folder(self):
        """Cria uma pasta para o post atual com timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        post_folder = self.base_dir / f"post_{timestamp}"
        post_folder.mkdir(exist_ok=True)
        return post_folder
    
    def save_post_content(self, post_folder, post_text, image_path=None, description=None):
        """Salva o conteúdo do post na pasta especificada"""
        # Salva o texto do post
        with open(post_folder / "post_text.txt", "w", encoding="utf-8") as f:
            f.write(post_text)
        
        # Salva a descrição da imagem se fornecida
        if description:
            with open(post_folder / "image_description.txt", "w", encoding="utf-8") as f:
                f.write(description)
        
        # Copia a imagem se existir
        if image_path and os.path.exists(image_path):
            import shutil
            image_name = Path(image_path).name
            shutil.copy2(image_path, post_folder / image_name)
        
        # Cria arquivo de metadados
        metadata = {
            "created_at": datetime.now().isoformat(),
            "post_text_length": len(post_text),
            "has_image": image_path is not None,
            "image_path": str(image_path) if image_path else None
        }
        
        with open(post_folder / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return post_folder
    
    def list_posts(self):
        """Lista todos os posts salvos"""
        posts = []
        for folder in self.base_dir.iterdir():
            if folder.is_dir() and folder.name.startswith("post_"):
                metadata_file = folder / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                        posts.append({
                            "folder": folder.name,
                            "path": str(folder),
                            "metadata": metadata
                        })
        return sorted(posts, key=lambda x: x["metadata"]["created_at"], reverse=True)
    
    def get_post_content(self, post_folder):
        """Recupera o conteúdo de um post específico"""
        folder_path = Path(post_folder)
        
        content = {}
        
        # Lê o texto do post
        post_text_file = folder_path / "post_text.txt"
        if post_text_file.exists():
            with open(post_text_file, "r", encoding="utf-8") as f:
                content["post_text"] = f.read()
        
        # Lê a descrição da imagem
        image_desc_file = folder_path / "image_description.txt"
        if image_desc_file.exists():
            with open(image_desc_file, "r", encoding="utf-8") as f:
                content["image_description"] = f.read()
        
        # Lê metadados
        metadata_file = folder_path / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                content["metadata"] = json.load(f)
        
        # Lista imagens na pasta
        image_files = [f for f in folder_path.iterdir() if f.suffix.lower() in ['.png', '.jpg', '.jpeg']]
        content["images"] = [str(f) for f in image_files]
        
        return content

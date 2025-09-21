#!/usr/bin/env python3
"""
Script principal - versão simplificada usando módulos separados
Para funcionalidades completas, use workflow.py
"""

from content_generator import ContentGenerator
from linkedin_publisher import LinkedInPublisher
import os
from dotenv import load_dotenv

def main():
    # Carrega as variáveis de ambiente
    load_dotenv()
    api_key_openai = os.getenv("OPENAI_API_KEY")
    
    if not api_key_openai:
        print("❌ OPENAI_API_KEY não encontrada no .env")
        return
    
    print("🚀 Iniciando geração e publicação de post...")
    print("💡 Para mais opções, use: python workflow.py --help")
    
    # Gera conteúdo
    generator = ContentGenerator(api_key_openai)
    content = generator.generate_content(save_to_history=True)
    
    if not content:
        print("❌ Falha na geração de conteúdo")
        return
    
    # Publica no LinkedIn
    publisher = LinkedInPublisher()
    result = publisher.publish_content(content, update_history=True)
    
    if result["success"]:
        print("🎉 Post gerado e publicado com sucesso!")
    else:
        print(f"❌ Falha na publicação: {result.get('error', 'Erro desconhecido')}")
        print("💡 Conteúdo foi salvo no histórico mesmo com falha na publicação")

if __name__ == "__main__":
    main()
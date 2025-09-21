#!/usr/bin/env python3
"""
Script principal - Menu Interativo
Inicia o sistema com menu de opções numeradas
"""

from menu_interativo import InteractiveMenu

def main():
    """Função principal - sempre abre o menu interativo"""
    print("🚀 Iniciando Sistema de Geração e Publicação de Conteúdo IA...")
    print("💡 Use Ctrl+C para sair a qualquer momento")
    print()
    
    try:
        menu = InteractiveMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n👋 Obrigado por usar o sistema!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Verifique se todas as dependências estão instaladas")

if __name__ == "__main__":
    main()

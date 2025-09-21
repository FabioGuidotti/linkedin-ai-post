# 🤖 LinkedIn AI Post - Sistema Completo de Geração e Publicação

## 🌟 Visão Geral

O **LinkedIn AI Post** é uma solução completa de automação para geração e publicação de conteúdo sobre inteligência artificial no LinkedIn. O sistema combina o poder da biblioteca CrewAI, OpenAI, DALL-E 3, SERPER e a API do LinkedIn para criar publicações envolventes e visualmente atraentes.

## ✨ Funcionalidades Principais

- 🚀 **Geração Automática de Conteúdo**: Notícias sobre IA usando CrewAI
- 🎨 **Criação de Imagens**: Imagens personalizadas com DALL-E 3
- 📚 **Histórico Organizado**: Sistema de pastas com data/hora
- 🎯 **Menu Interativo**: Interface amigável com opções numeradas
- 🔧 **Sistema Modular**: Módulos separados para geração e publicação
- 📊 **Gerenciamento de Status**: Controle completo de posts publicados/não publicados
- 🔄 **Recuperação de Falhas**: Republicar posts que falharam

## 🚀 Início Rápido

### 1. **Instalação**
```bash
# Clone o repositório
git clone https://github.com/FabioGuidotti/linkedin-ai-post.git
cd linkedin-ai-post

# Crie ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# Instale dependências
pip install -r requirements.txt
```

### 2. **Configuração**
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua_chave_openai
SERPER_API_KEY=sua_chave_serper
LINKEDIN_CLIENT_ID=seu_client_id
LINKEDIN_CLIENT_SECRET=seu_client_secret
```

### 3. **Execução**
```bash
# Método recomendado - Menu interativo
python start.py

# Ou use o workflow com parâmetros
python workflow.py --help
```

## 🎯 Menu Interativo

O sistema possui um menu interativo com 11 opções numeradas:

### **1. 🚀 Gerar e Publicar Post Completo**
- Gera notícias sobre IA
- Gera imagem para o post
- Salva no histórico
- Publica no LinkedIn
- **Ideal para**: Uso normal e produção

### **2. 📝 Gerar Apenas Conteúdo (sem publicar)**
- Gera notícias e imagem
- Salva no histórico
- NÃO publica no LinkedIn
- **Ideal para**: Desenvolvimento e teste

### **3. 🎨 Gerar Apenas Notícias (sem imagem)**
- Gera apenas o texto das notícias
- NÃO salva no histórico
- NÃO gera imagem
- **Ideal para**: Teste rápido de notícias

### **4. 🖼️ Gerar Apenas Imagem (para texto existente)**
- Solicita texto do usuário
- Gera imagem para o texto
- NÃO salva no histórico
- **Ideal para**: Gerar imagem para texto personalizado

### **5. 📤 Publicar Post do Histórico**
- Lista posts disponíveis
- Permite escolher qual publicar
- Mostra status de cada post
- **Ideal para**: Publicar posts que falharam

### **6. 📤 Publicar Todos os Posts Não Publicados**
- Encontra todos os posts não publicados
- Pergunta confirmação
- Publica todos automaticamente
- **Ideal para**: Recuperação em lote

### **7. 📊 Ver Status dos Posts**
- Mostra estatísticas gerais
- Conta posts publicados/não publicados
- Mostra último post criado
- **Ideal para**: Visão geral do sistema

### **8. 📋 Listar Posts do Histórico**
- Lista todos os posts salvos
- Mostra data e status
- **Ideal para**: Navegação no histórico

### **9. 👁️ Visualizar Post Específico**
- Lista posts disponíveis
- Permite escolher qual visualizar
- Mostra conteúdo completo
- **Ideal para**: Revisar posts anteriores

### **10. 👁️ Ver Post Mais Recente**
- Mostra o último post criado
- Visualização rápida
- **Ideal para**: Verificar último trabalho

### **11. ⚙️ Configurações**
- Mostra status das configurações
- Lista variáveis de ambiente
- Mostra estrutura de pastas
- **Ideal para**: Verificar configuração

### **0. 🚪 Sair**
- Encerra o programa

## 📁 Estrutura do Projeto

### **Scripts Principais**
```
projeto/
├── start.py                 # Script principal (menu interativo)
├── main.py                  # Script simples (gerar + publicar)
├── workflow.py              # Workflow com parâmetros + menu
├── menu_interativo.py       # Módulo do menu interativo
└── view_history.py          # Visualização do histórico
```

### **Módulos de Funcionalidade**
```
projeto/
├── content_generator.py     # Geração de conteúdo
├── linkedin_publisher.py    # Publicação no LinkedIn
├── history_manager.py       # Gerenciamento de histórico
├── news_generator.py        # Geração de notícias (CrewAI)
├── image_generator.py       # Geração de imagens (DALL-E)
└── linkedin_poster.py       # Integração com LinkedIn API
```

### **Sistema de Histórico**
```
historico_posts/
├── post_20250121_143022/
│   ├── post_text.txt          # Texto completo do post
│   ├── image_description.txt  # Descrição da imagem gerada
│   ├── metadata.json         # Metadados do post
│   └── imagem_gerada.png     # Imagem gerada
├── post_20250121_150145/
│   ├── post_text.txt
│   ├── image_description.txt
│   ├── metadata.json
│   └── imagem_gerada.png
└── ...
```

## 🔧 Uso Avançado

### **Comandos de Linha de Comando**
```bash
# Gerar e publicar
python workflow.py --generate

# Apenas gerar conteúdo
python workflow.py --generate-only

# Publicar post específico
python workflow.py --publish post_20250121_143022

# Publicar todos não publicados
python workflow.py --publish-all

# Listar posts
python workflow.py --list

# Ver status
python workflow.py --status

# Ver post específico
python workflow.py --view post_20250121_143022

# Ver post mais recente
python workflow.py --latest
```

### **Uso Programático**
```python
# Gerar conteúdo
from content_generator import ContentGenerator
generator = ContentGenerator(api_key)
content = generator.generate_content(save_to_history=True)

# Publicar conteúdo
from linkedin_publisher import LinkedInPublisher
publisher = LinkedInPublisher()
result = publisher.publish_content(content)
```

## 📊 Fluxos de Trabalho

### **🔄 Uso Diário (Produção)**
1. Execute `python start.py`
2. Escolha opção **1** (Gerar e Publicar)
3. Aguarde conclusão
4. Escolha opção **0** (Sair)

### **🧪 Desenvolvimento/Teste**
1. Execute `python start.py`
2. Escolha opção **2** (Gerar Apenas Conteúdo)
3. Verifique o resultado
4. Se satisfeito, escolha opção **5** (Publicar Post do Histórico)
5. Escolha o post desejado

### **🔧 Recuperação de Falhas**
1. Execute `python start.py`
2. Escolha opção **7** (Ver Status)
3. Se houver posts não publicados, escolha opção **6** (Publicar Todos)
4. Confirme a operação

### **📊 Análise e Revisão**
1. Execute `python start.py`
2. Escolha opção **8** (Listar Posts)
3. Para ver detalhes, escolha opção **9** (Visualizar Post Específico)
4. Escolha o post desejado

## 🎨 Interface Visual

### **Cabeçalho**
```
============================================================
🤖 SISTEMA DE GERAÇÃO E PUBLICAÇÃO DE CONTEÚDO IA
============================================================
📅 21/01/2025 14:30:22
```

### **Menu Principal**
```
📋 MENU PRINCIPAL
------------------------------
1. 🚀 Gerar e Publicar Post Completo
2. 📝 Gerar Apenas Conteúdo (sem publicar)
3. 🎨 Gerar Apenas Notícias (sem imagem)
4. 🖼️ Gerar Apenas Imagem (para texto existente)
5. 📤 Publicar Post do Histórico
6. 📤 Publicar Todos os Posts Não Publicados
7. 📊 Ver Status dos Posts
8. 📋 Listar Posts do Histórico
9. 👁️ Visualizar Post Específico
10. 👁️ Ver Post Mais Recente
11. ⚙️ Configurações
0. 🚪 Sair
------------------------------
👉 Escolha uma opção (0-11):
```

## 📋 Conteúdo de Cada Post

### **`post_text.txt`**
- Texto completo do post do LinkedIn
- Inclui hashtags e formatação
- Alerta de conteúdo gerado por IA

### **`image_description.txt`**
- Descrição detalhada da imagem gerada
- Instruções para criação visual
- Especificações de design

### **`metadata.json`**
```json
{
  "created_at": "2025-01-21T14:30:22.123456",
  "post_text_length": 1250,
  "has_image": true,
  "image_path": "C:\\GIT\\linkedin-ai-post\\imagem_gerada.png",
  "linkedin_posted": true,
  "linkedin_result": "Post publicado com sucesso",
  "linkedin_published_at": "2025-01-21T14:35:10.123456"
}
```

### **Imagens**
- Todas as imagens geradas são copiadas para a pasta do post
- Mantém backup mesmo se a imagem original for substituída
- Formato PNG otimizado para redes sociais

## 🔧 Configuração Detalhada

### **Variáveis de Ambiente Necessárias**
```env
# OpenAI (obrigatório)
OPENAI_API_KEY=sua_chave_openai

# SERPER (obrigatório para notícias)
SERPER_API_KEY=sua_chave_serper

# LinkedIn (opcional - para publicação)
LINKEDIN_CLIENT_ID=seu_client_id
LINKEDIN_CLIENT_SECRET=seu_client_secret
```

### **Como Obter as Chaves**

#### **OpenAI API Key**
1. Acesse [OpenAI Platform](https://platform.openai.com/)
2. Crie uma conta ou faça login
3. Vá para "API Keys"
4. Crie uma nova chave
5. Copie e cole no `.env`

#### **SERPER API Key**
1. Acesse [SERPER](https://serper.dev/)
2. Crie uma conta gratuita
3. Vá para "Dashboard"
4. Copie sua API key
5. Cole no `.env`

#### **LinkedIn API (Opcional)**
1. Acesse [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Crie uma nova aplicação
3. Configure o Redirect URI: `http://localhost:8000`
4. Copie Client ID e Client Secret
5. Cole no `.env`

## 🚨 Tratamento de Erros

### **Erros Comuns e Soluções**

#### **"OPENAI_API_KEY não encontrada"**
- Verifique se o arquivo `.env` existe
- Confirme se a chave está correta
- Reinicie o terminal após criar o `.env`

#### **"Falha na autenticação do LinkedIn"**
- Verifique Client ID e Client Secret
- Confirme se o Redirect URI está configurado
- Teste a autenticação manualmente

#### **"SERPER_API_KEY não encontrada"**
- Verifique se a chave está no `.env`
- Confirme se a conta SERPER está ativa
- Teste a chave no site da SERPER

#### **"Erro ao gerar imagem"**
- Verifique se a OPENAI_API_KEY está correta
- Confirme se tem créditos na conta OpenAI
- Teste com texto mais simples

### **Recuperação de Falhas**
- Conteúdo sempre salvo no histórico
- Possibilidade de republicar posts
- Logs detalhados de erros
- Sistema continua funcionando mesmo com falhas parciais

## 💡 Dicas de Uso

### **Para Iniciantes**
1. Comece com a opção **2** (Gerar Apenas Conteúdo)
2. Verifique o resultado antes de publicar
3. Use a opção **7** (Ver Status) para acompanhar
4. Mantenha backup do arquivo `.env`

### **Para Desenvolvimento**
1. Use a opção **2** para testar geração
2. Use a opção **4** para testar imagens
3. Use a opção **5** para publicar seletivamente
4. Monitore logs de erro

### **Para Produção**
1. Configure todas as chaves necessárias
2. Use a opção **1** para workflow completo
3. Monitore status regularmente
4. Use a opção **6** para recuperar falhas

## 🎉 Vantagens do Sistema

### ✅ **Facilidade de Uso**
- Menu interativo intuitivo
- Não precisa lembrar comandos
- Interface visual clara
- Navegação simples

### ✅ **Flexibilidade**
- Múltiplas opções de workflow
- Geração independente de publicação
- Recuperação de falhas
- Workflows personalizados

### ✅ **Organização**
- Histórico automático e organizado
- Metadados completos
- Backup seguro de conteúdo
- Estrutura consistente

### ✅ **Confiabilidade**
- Tratamento robusto de erros
- Recuperação automática
- Logs detalhados
- Sistema modular e testável

### ✅ **Escalabilidade**
- Módulos independentes
- Fácil adição de funcionalidades
- Suporte a outras redes sociais
- Integração com outros sistemas

## 📸 Exemplo de Resultado

Aqui está um exemplo de como o resultado final pode parecer no LinkedIn:

![Exemplo de Post](Publicação-Feed-LinkedIn.png)

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça suas alterações
4. Teste thoroughly
5. Submeta um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Se encontrar problemas:

1. Verifique a seção de **Tratamento de Erros**
2. Consulte as **Dicas de Uso**
3. Verifique as **Configurações**
4. Abra uma issue no GitHub

---

**Desenvolvido com ❤️ para automatizar e melhorar a presença no LinkedIn com conteúdo de IA de alta qualidade!**
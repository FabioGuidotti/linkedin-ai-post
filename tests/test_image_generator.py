import pytest
import os
import sys
from unittest.mock import Mock, patch

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root) 

from image_generator import GeradorImagemAI

@pytest.fixture
def mock_openai():
    with patch('image_generator.OpenAI') as mock_openai:
        yield mock_openai

@pytest.fixture
def gerador_imagem(mock_openai):
    return GeradorImagemAI('fake-api-key')

def test_init(mock_openai):
    gerador = GeradorImagemAI('test-key')
    mock_openai.assert_called_once_with(api_key='test-key')

def test_gerar_descricao(gerador_imagem, mock_openai):
    # Configurar o mock
    mock_response = Mock()
    mock_response.choices[0].message.content = "Uma descrição de teste"
    mock_openai.return_value.chat.completions.create.return_value = mock_response

    # Testar a função
    texto = "Texto de teste para LinkedIn"
    resultado = gerador_imagem.gerar_descricao(texto)

    # Verificar o resultado
    assert resultado == "Uma descrição de teste"
    mock_openai.return_value.chat.completions.create.assert_called_once()

def test_gerar_imagem(gerador_imagem, mock_openai):
    # Configurar o mock
    mock_response = Mock()
    mock_response.data = [Mock(url="https://exemplo.com/imagem.jpg")]
    mock_openai.return_value.images.generate.return_value = mock_response

    # Testar a função
    descricao = "Uma descrição de teste"
    resultado = gerador_imagem.gerar_imagem(descricao)

    # Verificar o resultado
    assert resultado == "https://exemplo.com/imagem.jpg"
    mock_openai.return_value.images.generate.assert_called_once_with(
        model="gpt-image-1",
        prompt=descricao,
        size="1024x1024"
    )

def test_gerar_imagem_ai_integracao(gerador_imagem, mock_openai):
    # Configurar os mocks
    mock_chat_response = Mock()
    mock_chat_response.choices[0].message.content = "Descrição gerada"
    mock_openai.return_value.chat.completions.create.return_value = mock_chat_response

    mock_image_response = Mock()
    mock_image_response.data = [Mock(url="https://exemplo.com/imagem.jpg")]
    mock_openai.return_value.images.generate.return_value = mock_image_response

    # Testar a função
    texto = "Texto de teste para LinkedIn"
    descricao, imagem = gerador_imagem.gerar_imagem_ai(texto)

    # Verificar os resultados
    assert descricao == "Descrição gerada"
    assert imagem == "https://exemplo.com/imagem.jpg"
    mock_openai.return_value.chat.completions.create.assert_called_once()
    mock_openai.return_value.images.generate.assert_called_once() 
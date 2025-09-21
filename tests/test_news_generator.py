import pytest
from unittest.mock import Mock, patch
from news_generator import GeradorDeNoticiasAI

@pytest.fixture
def mock_env_vars():
    with patch.dict('os.environ', {
        'SERPER_API_KEY': 'fake-serper-key',
        'OPENAI_API_KEY': 'fake-openai-key',
        'OPENAI_MODEL_NAME': 'gpt-4o-mini'
    }):
        yield

@pytest.fixture
def mock_dependencies():
    with patch('news_generator.SerperDevTool') as mock_serper, \
         patch('news_generator.criar_pesquisador') as mock_criar_pesquisador, \
         patch('news_generator.criar_escritor') as mock_criar_escritor, \
         patch('news_generator.Crew') as mock_crew, \
         patch('news_generator.load_dotenv') as mock_load_dotenv:
        
        # Configurar mocks
        mock_pesquisador = Mock(name='pesquisador')
        mock_escritor = Mock(name='escritor')
        mock_criar_pesquisador.return_value = mock_pesquisador
        mock_criar_escritor.return_value = mock_escritor
        
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = "Post do LinkedIn gerado com sucesso!"
        mock_crew.return_value = mock_crew_instance

        yield {
            'serper': mock_serper,
            'criar_pesquisador': mock_criar_pesquisador,
            'criar_escritor': mock_criar_escritor,
            'crew': mock_crew,
            'load_dotenv': mock_load_dotenv,
            'pesquisador': mock_pesquisador,
            'escritor': mock_escritor
        }

def test_init(mock_env_vars, mock_dependencies):
    # Testar a inicialização da classe
    gerador = GeradorDeNoticiasAI()
    
    # Verificar se as dependências foram inicializadas corretamente
    mock_dependencies['load_dotenv'].assert_called_once()
    mock_dependencies['serper'].assert_called_once()
    mock_dependencies['criar_pesquisador'].assert_called_once()
    mock_dependencies['criar_escritor'].assert_called_once()

def test_gerar_post_linkedin(mock_env_vars, mock_dependencies):
    # Criar instância do gerador
    gerador = GeradorDeNoticiasAI()
    
    # Testar a geração do post
    resultado = gerador.gerar_post_linkedin()
    
    # Verificar se o Crew foi configurado corretamente
    mock_dependencies['crew'].assert_called_once()
    crew_call_kwargs = mock_dependencies['crew'].call_args[1]
    
    # Verificar os agentes passados para o Crew
    assert mock_dependencies['pesquisador'] in crew_call_kwargs['agents']
    assert mock_dependencies['escritor'] in crew_call_kwargs['agents']
    
    # Verificar o resultado
    assert resultado == "Post do LinkedIn gerado com sucesso!"

@patch('news_generator.criar_tarefa_pesquisa')
@patch('news_generator.criar_tarefa_escrita')
def test_gerar_post_linkedin_tarefas(mock_criar_tarefa_escrita, mock_criar_tarefa_pesquisa, 
                                   mock_env_vars, mock_dependencies):
    # Configurar mocks das tarefas
    mock_tarefa_pesquisa = Mock(name='tarefa_pesquisa')
    mock_tarefa_escrita = Mock(name='tarefa_escrita')
    mock_criar_tarefa_pesquisa.return_value = mock_tarefa_pesquisa
    mock_criar_tarefa_escrita.return_value = mock_tarefa_escrita
    
    # Criar instância e gerar post
    gerador = GeradorDeNoticiasAI()
    resultado = gerador.gerar_post_linkedin()
    
    # Verificar se as tarefas foram criadas corretamente
    mock_criar_tarefa_pesquisa.assert_called_once_with(mock_dependencies['pesquisador'])
    mock_criar_tarefa_escrita.assert_called_once_with(mock_dependencies['escritor'])
    
    # Verificar se as tarefas foram passadas para o Crew
    crew_call_kwargs = mock_dependencies['crew'].call_args[1]
    assert mock_tarefa_pesquisa in crew_call_kwargs['tasks']
    assert mock_tarefa_escrita in crew_call_kwargs['tasks'] 
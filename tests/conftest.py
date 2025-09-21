import os
import sys
import pytest
from dotenv import load_dotenv

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Carrega as variáveis de ambiente para os testes
@pytest.fixture(autouse=True)
def load_env():
    load_dotenv()


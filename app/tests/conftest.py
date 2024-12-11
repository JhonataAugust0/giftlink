import os
import sys
import pytest
from dotenv import load_dotenv

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../app')
        )
    ),

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

    # Validação simples para garantir que as variáveis estão sendo carregadas
    assert os.environ.get("POSTGRES_USER") is not None, "POSTGRES_USER não foi carregado"
    assert os.environ.get("POSTGRES_PASSWORD") is not None, "POSTGRES_PASSWORD não foi carregado"
    assert os.environ.get("POSTGRES_DB") is not None, "POSTGRES_DB não foi carregado"
    assert os.environ.get("POSTGRES_URL") is not None, "POSTGRES_URL não foi carregado"
    assert os.environ.get("TORTOISE_MODELS_PATH") is not None, "TORTOISE_MODELS_PATH não foi carregado"

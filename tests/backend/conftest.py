import sys
import os
import pytest
from flask import Flask

# Adiciona o caminho do backend ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app import create_app

@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask."""
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

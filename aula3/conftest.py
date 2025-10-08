import pytest
import requests
import csv
import os


@pytest.fixture(scope="session")
def base_url():
    """Retorna a URL base para a API JSONPlaceholder."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="function")
def api_client():
    """Retorna um cliente de API (módulo requests)."""
    return requests


def carregar_casos_de_teste_csv(path):
    """Lê um arquivo CSV e retorna uma lista de dicionários."""
    # Garante que o caminho seja relativo ao arquivo conftest.py
    diretorio_atual = os.path.dirname(__file__)
    caminho_completo = os.path.join(diretorio_atual, path)

    casos = []
    with open(caminho_completo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            casos.append(row)
    return casos

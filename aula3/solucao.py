import pytest
from requests.auth import HTTPBasicAuth

from conftest import carregar_casos_de_teste_csv

# --- Teste Dinâmico com Dados de um Arquivo Externo ---

# Carrega os casos de teste do CSV para serem usados na parametrização
casos_de_teste = carregar_casos_de_teste_csv("casos_de_teste.csv")


@pytest.mark.api_test
@pytest.mark.parametrize("caso_de_teste", casos_de_teste)
def test_criar_post_dinamico(base_url, api_client, caso_de_teste):
    """
    Testa a criação de posts (recurso /posts) de forma dinâmica,
    lendo os casos de teste de um arquivo CSV.
    """
    # Prepara o payload com base na linha atual do CSV
    payload = {
        "title": caso_de_teste["title"],
        "body": caso_de_teste["body"],
        # Converte userId para int, tratando o caso de estar vazio no CSV
        "userId": int(caso_de_teste["userId"]) if caso_de_teste["userId"] else 1
    }
    expected_status = int(caso_de_teste["expected_status"])

    # Envia a requisição POST para criar um novo post
    response = api_client.post(f"{base_url}/posts", json=payload)

    # Valida o status code da resposta
    assert response.status_code == expected_status

    # Se a criação foi bem-sucedida (201), valida o conteúdo da resposta
    if response.status_code == 201:
        response_data = response.json()
        assert response_data["title"] == payload["title"]
        assert response_data["body"] == payload["body"]
        assert response_data["userId"] == payload["userId"]

# --- Refatoração dos Testes da Aula 2 com Fixtures ---


@pytest.mark.api_test
def test_get_comments_for_post(base_url, api_client):
    """Refatorado: Busca comentários e valida o postId."""
    params = {'postId': 1}
    response = api_client.get(f"{base_url}/comments", params=params)
    assert response.status_code == 200
    for comment in response.json():
        assert comment['postId'] == 1


@pytest.mark.api_test
def test_get_todos_for_user(base_url, api_client):
    """Refatorado: Busca tarefas de um usuário."""
    params = {'userId': 5}
    response = api_client.get(f"{base_url}/todos", params=params)
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.api_test
def test_count_albums_for_user(base_url, api_client):
    """Refatorado: Conta os álbuns de um usuário."""
    params = {'userId': 9}
    response = api_client.get(f"{base_url}/albums", params=params)
    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.api_test
def test_get_completed_todos_for_user(base_url, api_client):
    """Refatorado: Busca tarefas concluídas de um usuário."""
    params = {'userId': 1, 'completed': 'true'}
    response = api_client.get(f"{base_url}/todos", params=params)
    assert response.status_code == 200
    for todo in response.json():
        assert todo['completed'] is True


@pytest.mark.api_test
def test_custom_header(api_client):
    """Refatorado: Testa o envio de um header customizado."""
    headers = {'X-Custom-Header': 'MyValue'}
    response = api_client.get("https://httpbin.org/headers", headers=headers)
    assert response.status_code == 200
    assert response.json()['headers']['X-Custom-Header'] == 'MyValue'


@pytest.mark.api_test
def test_basic_auth_correct_credentials(api_client):
    """Refatorado: Testa autenticação básica com credenciais corretas."""
    response = api_client.get(
        "https://httpbin.org/basic-auth/user/passwd",
        auth=HTTPBasicAuth('user', 'passwd')
    )
    assert response.status_code == 200


@pytest.mark.api_test
def test_bearer_token_auth(api_client):
    """Refatorado: Testa autenticação com Bearer Token."""
    token = 'my-mock-token'
    headers = {'Authorization': f'Bearer {token}'}
    response = api_client.get("https://httpbin.org/bearer", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['authenticated'] is True
    assert data['token'] == token


@pytest.mark.api_test
def test_validate_user_data_types(base_url, api_client):
    """Refatorado: Valida os tipos de dados de um usuário."""
    response = api_client.get(f"{base_url}/users/1")
    assert response.status_code == 200
    user = response.json()
    assert isinstance(user['id'], int)
    assert isinstance(user['name'], str)
    assert isinstance(user['address'], dict)


@pytest.mark.api_test
def test_validate_photo_structure_in_album(base_url, api_client):
    """Refatorado: Valida a estrutura das fotos em um álbum."""
    response = api_client.get(f"{base_url}/albums/1/photos")
    assert response.status_code == 200
    for photo in response.json():
        assert 'albumId' in photo
        assert 'id' in photo
        assert 'title' in photo
        assert 'url' in photo
        assert 'thumbnailUrl' in photo

import requests
import pytest
from requests.auth import HTTPBasicAuth

# --- Desafios: Query Params ---

# 1. Busque todos os comentários do post com ID 2 e verifique se todos pertencem a esse post.


def test_get_comments_for_post_2():
    params = {'postId': 2}
    response = requests.get(
        "https://jsonplaceholder.typicode.com/comments", params=params)
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0
    for comment in comments:
        assert comment['postId'] == 2

# 2. Liste todas as tarefas (todos) do usuário com ID 5 e verifique se a lista não está vazia.


def test_get_todos_for_user_5():
    params = {'userId': 5}
    response = requests.get(
        "https://jsonplaceholder.typicode.com/todos", params=params)
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) > 0

# 3. Busque todos os álbuns do usuário com ID 9 e conte quantos ele tem (deve ser 10).


def test_count_albums_for_user_9():
    params = {'userId': 9}
    response = requests.get(
        "https://jsonplaceholder.typicode.com/albums", params=params)
    assert response.status_code == 200
    albums = response.json()
    assert len(albums) == 10

# 4. Liste todas as tarefas concluídas do usuário com ID 1 e verifique se todas estão de fato concluídas.


def test_get_completed_todos_for_user_1():
    params = {'userId': 1, 'completed': 'true'}
    response = requests.get(
        "https://jsonplaceholder.typicode.com/todos", params=params)
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) > 0
    for todo in todos:
        assert todo['completed'] is True

# --- Desafios: Headers ---

# 5. Envie uma requisição para httpbin.org/headers com um header customizado e valide.


def test_custom_header():
    headers = {'X-Custom-Header': 'MyValue'}
    response = requests.get("https://httpbin.org/headers", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['headers']['X-Custom-Header'] == 'MyValue'

# 6. Envie uma requisição para httpbin.org/response-headers para setar um header de resposta e verifique.


def test_custom_response_header():
    params = {'My-Test-Header': 'Hello'}
    response = requests.get(
        "https://httpbin.org/response-headers", params=params)
    assert response.status_code == 200
    assert 'My-Test-Header' in response.headers
    assert response.headers['My-Test-Header'] == 'Hello'

# 7. Envie uma requisição com um User-Agent customizado e valide.


def test_custom_user_agent():
    headers = {'User-Agent': 'My-Test-Agent/1.0'}
    response = requests.get("https://httpbin.org/headers", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['headers']['User-Agent'] == 'My-Test-Agent/1.0'

# 8. Envie múltiplos headers customizados e valide todos.


def test_multiple_custom_headers():
    headers = {
        'X-Header-1': 'Value1',
        'X-Header-2': 'Value2'
    }
    response = requests.get("https://httpbin.org/headers", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['headers']['X-Header-1'] == 'Value1'
    assert data['headers']['X-Header-2'] == 'Value2'

# --- Desafios: Autenticação ---

# 9. Teste o endpoint de Basic Auth com credenciais corretas.


def test_basic_auth_correct_credentials():
    response = requests.get(
        "https://httpbin.org/basic-auth/user/passwd", auth=HTTPBasicAuth('user', 'passwd'))
    assert response.status_code == 200

# 10. Teste o endpoint de Basic Auth com a senha errada.


def test_basic_auth_wrong_password():
    response = requests.get(
        "https://httpbin.org/basic-auth/user/passwd", auth=HTTPBasicAuth('user', 'wrongpass'))
    assert response.status_code == 401

# 11. Envie uma requisição com um Bearer Token válido.


def test_bearer_token_auth():
    token = 'my-mock-token'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get("https://httpbin.org/bearer", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['authenticated'] is True
    assert data['token'] == token

# 12. Envie uma requisição para /bearer sem autorização.


def test_bearer_token_no_auth_header():
    response = requests.get("https://httpbin.org/bearer")
    assert response.status_code == 401

# --- Desafios: Asserções Avançadas ---

# 13. Busque o usuário com ID 1 e valide os tipos de dados.


def test_validate_user_data_types():
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")
    assert response.status_code == 200
    user = response.json()
    assert isinstance(user['id'], int)
    assert isinstance(user['name'], str)
    assert isinstance(user['address'], dict)
    assert isinstance(user['company'], dict)

# 14. Para o usuário 1, verifique a estrutura do endereço.


def test_validate_user_address_structure():
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")
    assert response.status_code == 200
    user = response.json()
    assert 'street' in user['address']
    assert 'city' in user['address']
    assert 'zipcode' in user['address']

# 15. Busque o post com ID 10 e valide seu conteúdo.


def test_validate_post_content():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/10")
    assert response.status_code == 200
    post = response.json()
    assert isinstance(post['userId'], int)
    assert isinstance(post['id'], int)
    assert isinstance(post['title'], str) and post['title'] != ""
    assert isinstance(post['body'], str) and post['body'] != ""

# 16. Liste as fotos do álbum 1 e verifique a estrutura de cada foto.


def test_validate_photo_structure_in_album():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/albums/1/photos")
    assert response.status_code == 200
    photos = response.json()
    assert len(photos) > 0
    for photo in photos:
        assert 'albumId' in photo
        assert 'id' in photo
        assert 'title' in photo
        assert 'url' in photo
        assert 'thumbnailUrl' in photo

# 17. Verifique se o email do usuário 3 tem formato válido.


def test_validate_user_email_format():
    response = requests.get("https://jsonplaceholder.typicode.com/users/3")
    assert response.status_code == 200
    user = response.json()
    assert '@' in user['email']
    assert '.' in user['email'].split('@')[1]

# 18. Busque os comentários do post 5 e verifique se a lista não está vazia.


def test_comments_list_is_not_empty():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/5/comments")
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0

# 19. Para o primeiro comentário do post 5, valide os tipos de dados.


def test_validate_first_comment_data_types():
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/5/comments")
    assert response.status_code == 200
    comments = response.json()
    first_comment = comments[0]
    assert isinstance(first_comment['postId'], int)
    assert isinstance(first_comment['id'], int)
    assert isinstance(first_comment['name'], str)
    assert isinstance(first_comment['email'], str)
    assert isinstance(first_comment['body'], str)

# 20. Busque a tarefa com ID 199 e verifique se 'completed' é um booleano.


def test_validate_todo_completed_is_boolean():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/199")
    assert response.status_code == 200
    todo = response.json()
    assert isinstance(todo['completed'], bool)

import pytest
import requests

a = 1
b = 2
c = a + b

response = requests.get("https://api.github.com")
assert response.status_code == 200

# Passo 1: Requisição Simples


# def test_simple_request():
#     response = requests.get("https://api.github.com")
#     assert response.status_code == 200

# # Passo 2: Buscar um Usuário Específico


# def test_get_specific_user():
#     response = requests.get("https://api.github.com/users/octocat")
#     data = response.json()
#     assert data["login"] == "octocat"

# # Passo 3: Validar o Tipo do Usuário


# def test_validate_user_type():
#     response = requests.get("https://api.github.com/users/octocat")
#     data = response.json()
#     assert data["type"] == "User"

# # Passo 4: Requisição com ID de Repositório


# def test_get_repository_by_id():
#     response = requests.get("https://api.github.com/repositories/1296269")
#     data = response.json()
#     assert data["name"] == "Hello-World"

# # Passo 5: Lidando com Erros (Usuário Inexistente)


# def test_handle_nonexistent_user():
#     response = requests.get(
#         "https://api.github.com/users/usuarioquenaoexiste12345")
#     assert response.status_code == 404

# # Passo 6: Listar Repositórios de um Usuário


# def test_list_user_repositories():
#     params = {"per_page": 5}
#     response = requests.get(
#         "https://api.github.com/users/google/repos", params=params)
#     data = response.json()
#     assert len(data) == 5

# # Passo 7: Navegar pela Paginação de Seguidores


# def test_follower_pagination():
#     response = requests.get(
#         "https://api.github.com/users/microsoft/followers", params={"per_page": 2})
#     next_url = response.links.get('next', {}).get('url')
#     assert next_url is not None
#     response_next = requests.get(next_url)
#     assert response_next.status_code == 200

# # Passo 8: Contar Repositórios Públicos de um Usuário


# def test_count_public_repos():
#     response = requests.get("https://api.github.com/users/facebook")
#     data = response.json()
#     assert data['public_repos'] > 0

# # Passo 9: Encontrar uma Linguagem Específica em um Repositório


# def test_find_language_in_repo():
#     response = requests.get(
#         "https://api.github.com/repos/facebook/react/languages")
#     data = response.json()
#     assert "JavaScript" in data

# # Passo 10: Explorar outro Endpoint (Emojis)


# def test_explore_emojis_endpoint():
#     response = requests.get("https://api.github.com/emojis")
#     data = response.json()
#     assert "+1" in data

# # Passo 11: Validar Estrutura do JSON de um Repositório


# def test_validate_repo_json_structure():
#     response = requests.get("https://api.github.com/repos/torvalds/linux")
#     data = response.json()
#     assert "name" in data
#     assert "owner" in data
#     assert "language" in data

# # Passo 12: Comparar Atributos de Repositórios


# def test_compare_repo_attributes():
#     response_vscode = requests.get(
#         "https://api.github.com/repos/microsoft/vscode").json()
#     response_atom = requests.get(
#         "https://api.github.com/repos/atom/atom").json()
#     assert response_vscode['stargazers_count'] > response_atom['stargazers_count']

# # Passo 13: Buscar uma Licença


# def test_get_license():
#     response = requests.get("https://api.github.com/licenses/mit")
#     data = response.json()
#     assert data['name'] == "MIT License"

# # Passo 14: Listar todas as Licenças


# def test_list_all_licenses():
#     response = requests.get("https://api.github.com/licenses")
#     data = response.json()
#     assert len(data) > 0

# # Passo 15: Encontrar Repositórios com uma Licença Específica


# def test_find_repos_with_license():
#     params = {"q": "license:apache-2.0"}
#     response = requests.get(
#         "https://api.github.com/search/repositories", params=params)
#     data = response.json()
#     assert len(data['items']) > 0

# # Passo 16: Validar a Organização de um Repositório


# def test_validate_repo_organization():
#     response = requests.get("https://api.github.com/repos/moby/docker")
#     data = response.json()
#     assert data['owner']['login'] == 'moby'

# # Passo 17: Checar o Último Commit de um Repositório


# def test_check_last_commit():
#     response = requests.get(
#         "https://api.github.com/repos/tensorflow/tensorflow/commits")
#     data = response.json()
#     last_commit_message = data[0]['commit']['message']
#     assert len(last_commit_message) > 0

# # Passo 18: Verificar se um Usuário é uma Organização


# def test_check_if_user_is_organization():
#     response = requests.get("https://api.github.com/users/apple").json()
#     assert response['type'] == 'Organization'

# # Passo 19: Encontrar o Número de Contribuidores de um Repositório


# def test_get_contributor_count():
#     response = requests.get(
#         "https://api.github.com/repos/kubernetes/kubernetes/contributors", params={"per_page": 1})
#     links = response.links
#     last_page_url = links['last']['url']
#     num_contributors = int(last_page_url.split('page=')[-1])
#     assert num_contributors > 1000

# # Passo 20: Desafio Final - Juntar Tudo


# def get_user_summary(username):
#     url = f"https://api.github.com/users/{username.lower()}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return None
#     data = response.json()
#     summary = {
#         "login": data["login"],
#         "name": data.get("name"),
#         "public_repos": data.get("public_repos")
#     }
#     return summary


# def test_final_challenge():
#     torvalds_summary = get_user_summary("torvalds")
#     assert torvalds_summary['login'] == 'torvalds'
#     assert torvalds_summary['public_repos'] > 0


# # Passo 21: Criar um Novo Post (POST)
# def test_create_new_post():
#     new_post = {
#         "title": "foo",
#         "body": "bar",
#         "userId": 1
#     }
#     response = requests.post(
#         "https://jsonplaceholder.typicode.com/posts", json=new_post)
#     assert response.status_code == 201

# # Passo 22: Validar Dados do Post Criado


# def test_validate_created_post_data():
#     new_post = {
#         "title": "foo",
#         "body": "bar",
#         "userId": 1
#     }
#     response = requests.post(
#         "https://jsonplaceholder.typicode.com/posts", json=new_post)
#     data = response.json()
#     assert data["title"] == "foo"
#     assert data["body"] == "bar"

# # Passo 23: Atualizar um Post (PUT)


# def test_update_post():
#     updated_post = {
#         "id": 1,
#         "title": "foo_updated",
#         "body": "bar_updated",
#         "userId": 1
#     }
#     response = requests.put(
#         "https://jsonplaceholder.typicode.com/posts/1", json=updated_post)
#     assert response.status_code == 200

# # Passo 24: Validar a Atualização do Post


# def test_validate_post_update():
#     updated_post = {
#         "id": 1,
#         "title": "foo_updated",
#         "body": "bar_updated",
#         "userId": 1
#     }
#     response = requests.put(
#         "https://jsonplaceholder.typicode.com/posts/1", json=updated_post)
#     data = response.json()
#     assert data["title"] == "foo_updated"
#     assert data["body"] == "bar_updated"

# # Passo 25: Deletar um Post (DELETE)


# def test_delete_post():
#     response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
#     assert response.status_code == 200

# # Passo 26: Listar Todos os Usuários


# def test_list_all_users():
#     response = requests.get("https://jsonplaceholder.typicode.com/users")
#     data = response.json()
#     assert len(data) == 10

# # Passo 27: Buscar um Usuário Específico


# def test_get_specific_user_jsonplaceholder():
#     response = requests.get("https://jsonplaceholder.typicode.com/users/5")
#     data = response.json()
#     assert data["name"] == "Chelsey Dietrich"

# # Passo 28: Criar um Novo Comentário para um Post


# def test_create_new_comment():
#     new_comment = {
#         "postId": 1,
#         "name": "a name",
#         "email": "an.email@example.com",
#         "body": "a body"
#     }
#     response = requests.post(
#         "https://jsonplaceholder.typicode.com/posts/1/comments", json=new_comment)
#     assert response.status_code == 201

# # Passo 29: Listar Álbuns de um Usuário


# def test_list_user_albums():
#     response = requests.get(
#         "https://jsonplaceholder.typicode.com/users/3/albums")
#     data = response.json()
#     assert len(data) > 0

# # Passo 30: Listar Fotos de um Álbum


# def test_list_album_photos():
#     response = requests.get(
#         "https://jsonplaceholder.typicode.com/albums/2/photos")
#     data = response.json()
#     assert data[0]["title"] == "reprehenderit est deserunt velit ipsam"

# # Passo 31: Criar uma Nova Tarefa (Todo)


# def test_create_new_todo():
#     new_todo = {
#         "userId": 1,
#         "title": "Aprender Pytest",
#         "completed": False
#     }
#     response = requests.post(
#         "https://jsonplaceholder.typicode.com/todos", json=new_todo)
#     assert response.status_code == 201
#     data = response.json()
#     assert data["title"] == "Aprender Pytest"

# # Passo 32: Atualizar uma Tarefa (PATCH)


# def test_update_task_with_patch():
#     update = {"completed": True}
#     response = requests.patch(
#         "https://jsonplaceholder.typicode.com/todos/5", json=update)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["completed"] is True

# # Passo 33: Listar Tarefas Concluídas de um Usuário


# def test_list_completed_tasks():
#     params = {"userId": 1, "completed": "true"}
#     response = requests.get(
#         "https://jsonplaceholder.typicode.com/todos", params=params)
#     data = response.json()
#     assert len(data) > 0
#     for task in data:
#         assert task["completed"] is True

# # Passo 34: Validar Estrutura de um Comentário


# def test_validate_comment_structure():
#     response = requests.get("https://jsonplaceholder.typicode.com/comments/10")
#     data = response.json()
#     assert "postId" in data
#     assert "id" in data
#     assert "name" in data
#     assert "email" in data
#     assert "body" in data

# # Passo 35: Deletar um Comentário


# def test_delete_comment():
#     response = requests.delete(
#         "https://jsonplaceholder.typicode.com/comments/3")
#     assert response.status_code == 200

# # Passo 36: Criar um Post com Dados Inválidos


# def test_create_post_with_invalid_data():
#     response = requests.post(
#         "https://jsonplaceholder.typicode.com/posts", json={})
#     # JSONPlaceholder returns 201 even for empty body
#     assert response.status_code == 201

# # Passo 37: Buscar Posts de um Usuário Específico


# def test_get_posts_by_user():
#     response = requests.get(
#         "https://jsonplaceholder.typicode.com/users/7/posts")
#     data = response.json()
#     assert len(data) > 0
#     for post in data:
#         assert post["userId"] == 7

# # Passo 38: Atualizar o Email de um Usuário (PUT)


# def test_update_user_email():
#     user_response = requests.get(
#         "https://jsonplaceholder.typicode.com/users/2")
#     user_data = user_response.json()
#     user_data["email"] = "novo.email@example.com"

#     response = requests.put(
#         "https://jsonplaceholder.typicode.com/users/2", json=user_data)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["email"] == "novo.email@example.com"

# # Passo 39: Deletar um Álbum


# def test_delete_album():
#     response = requests.delete("https://jsonplaceholder.typicode.com/albums/4")
#     assert response.status_code == 200

# # Passo 40: Desafio Final com JSONPlaceholder


# def test_final_challenge_jsonplaceholder():
#     # Create a post
#     new_post = {"userId": 1, "title": "Final Challenge Post",
#                 "body": "This is the body."}
#     post_response = requests.post(
#         "https://jsonplaceholder.typicode.com/posts", json=new_post)
#     assert post_response.status_code == 201
#     post_data = post_response.json()
#     post_id = post_data["id"]

#     # Add a comment to the post
#     new_comment = {"postId": post_id, "name": "Challenge Comment",
#                    "email": "challenge@test.com", "body": "A comment for the challenge."}
#     comment_response = requests.post(
#         f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments", json=new_comment)
#     assert comment_response.status_code == 201

#     # Delete the post
#     delete_response = requests.delete(
#         f"https://jsonplaceholder.typicode.com/posts/{post_id}")
#     assert delete_response.status_code == 200

import json

import requests

from .config import GITHUB_API_URL


def parse_user(repositories: list) -> dict:
    """
    Retira o user_id e username do json de
    reposta do github e retorna no formato dict
    """
    owner = repositories[0]["owner"]
    return {"user_id": owner["id"], "username": owner["login"]}


def request_external_to_json(url: str) -> json:
    """
    Faz a requisição ao servidor externo (github),
    valida a resposta e retorna o json que esta no corpo
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_repositories_by_username(username: str) -> json:
    """
    Busca lista de repositórios no github por username
    """
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    return request_external_to_json(url)


def get_repository_by_username_and_name(username: str, repository_name: str) -> json:
    """
    Busca detalhe de um repositório no github por username e nome do repositório
    """
    url = f"{GITHUB_API_URL}/repos/{username}/{repository_name}"
    return request_external_to_json(url)

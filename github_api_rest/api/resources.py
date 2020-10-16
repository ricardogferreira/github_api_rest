from flask_restx import Resource
from requests.exceptions import ConnectionError, HTTPError

from github_api_rest.exceptions import DatabaseUserNotFoundError
from github_api_rest.main import api
from github_api_rest.use_cases import (get_repositories,
                                       get_repository_from_github)

from .reqparse import repository_args, repository_list_args


class Repository(Resource):
    def get(self, username: str, repository_name: str):
        """Mostra detalhes de um repositório do usuário,
        pode ser salvo no banco de dados local através do
        query param passado na url
        """
        args = repository_args()
        try:
            result = get_repository_from_github(username, repository_name, **args)
            return result, 200
        except (ConnectionError, HTTPError):
            return {"message": "Falha ao buscar o repositório no github"}, 400


class RepositoryList(Resource):
    def get(self):
        """Lista repositorios de um usuário, pode ser retornado via cache(db) ou
        diretamente no github
        """
        args = repository_list_args()
        try:
            result = get_repositories(**args)
            return result, 200
        except (ConnectionError, HTTPError):
            return {"message": "Falha ao buscar o usuário"}, 400
        except DatabaseUserNotFoundError:
            return {"message": "Usuário não encontrado na base de dados"}, 400


api.add_resource(RepositoryList, "/repositories")
api.add_resource(
    Repository, "/users/<string:username>/repositories/<string:repository_name>/"
)

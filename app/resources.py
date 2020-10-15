from flask_restx import Resource
from requests.exceptions import HTTPError

from app.exceptions import DatabaseUserNotFoundError
from app.main import api
from app.reqparse import repository_args, repository_list_args
from app.use_cases import get_repositories, get_repository_from_github


class Repository(Resource):
    def get(self, username: str, repository_name: str):
        args = repository_args()
        try:
            result = get_repository_from_github(username, repository_name, **args)
            return result, 200
        except HTTPError:
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
        except HTTPError:
            return {"message": "Falha ao buscar o usuário"}, 400
        except DatabaseUserNotFoundError:
            return {"message": "Usuário não encontrado na base de dados"}, 400


api.add_resource(RepositoryList, "/repositories")
api.add_resource(
    Repository, "/users/<string:username>/repositories/<string:repository_name>/"
)

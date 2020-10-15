from app.exceptions import DatabaseUserNotFoundError
from app.external import (get_repositories_by_username,
                          get_repository_by_username_and_name, parse_user)
from app.main import db
from app.models import Repository, User
from app.utils import (parse_repositories, parse_repository,
                       zip_user_repositories)


def save_repository(
    id, username: str, repository_name: str, parsed_repository: dict
) -> None:
    """
    Salva os dados do usuário e repositório no banco de dados.
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username, id=id)

    repository = Repository.query.filter_by(name=repository_name, user=user).first()
    repository = repository or Repository()

    for key, value in parsed_repository.items():
        setattr(repository, key, value)

    user.repositories.append(repository)
    db.session.add(user)
    db.session.commit()


def get_user_repositories_from_local(username: str) -> dict:
    """
    Busca usuário e repositorios no banco de dados a partir do username e retorna
    em uma estrutura de dicionário
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise DatabaseUserNotFoundError

    user_repositories = zip_user_repositories(
        {
            "user_id": user.id,
            "username": user.username,
        },
        parse_repositories(user.repositories),
    )

    return user_repositories


def get_user_and_repositories_from_github(username: str) -> dict:
    """
    Busca usuário e repositorios no github a partir do username e retorna
    em uma estrutura de dicionário
    """
    repositories = get_repositories_by_username(username)
    user = parse_user(repositories)
    repositories = parse_repositories(repositories)
    user_repositories = zip_user_repositories(user, repositories)
    return user_repositories


def get_repositories(username: str, from_local: bool) -> dict:
    "Retorna um dicionário com os dados do usuário e repositórios"

    if from_local:
        return get_user_repositories_from_local(username)

    return get_user_and_repositories_from_github(username)


def get_repository_from_github(
    username: str, repository_name: str, save_data: bool
) -> dict:
    """Busca repositorio a partir do username e repository_name no github e
    armazena no banco de dados e save_data for True
    """

    repository = get_repository_by_username_and_name(username, repository_name)
    parsed_repository = parse_repository(repository)
    if save_data:
        save_repository(
            repository["owner"]["id"], username, repository_name, parsed_repository
        )
    return parsed_repository

from .exceptions import (DatabaseRepositoryNotFoundError,
                         DatabaseUserNotFoundError)
from .external import (get_repositories_by_username,
                       get_repository_by_username_and_name, parse_user)
from .main import db
from .models import Repository, User
from .utils import parse_repositories, parse_repository, zip_user_repositories


def get_user_from_db(username: str) -> User:
    """Busca usuário no banco de dados"""
    user = User.query.filter_by(username=username).first()
    if not user:
        raise DatabaseUserNotFoundError
    return user


def get_repository_from_db(name: str, user: str) -> Repository:
    """Busca repositório no banco de dados"""
    repository = Repository.query.filter_by(name=name, user=user).first()
    if not repository:
        raise DatabaseRepositoryNotFoundError
    return repository


def save_changes(data):
    """Faz o commit das alterações"""
    db.session.add(data)
    db.session.commit()


def save_repository(
    id, username: str, repository_name: str, parsed_repository: dict
) -> None:
    """
    Salva os dados do usuário e repositório no banco de dados.
    """
    try:
        user = get_user_from_db(username)
    except DatabaseUserNotFoundError:
        user = User(username=username, id=id)

    try:
        repository = get_repository_from_db(name=repository_name, user=user)
    except DatabaseRepositoryNotFoundError:
        repository = Repository()

    for key, value in parsed_repository.items():
        setattr(repository, key, value)

    user.repositories.append(repository)
    save_changes(user)


def get_user_repositories_from_local(username: str) -> dict:
    """
    Busca usuário e repositorios no banco de dados a partir do username e retorna
    em uma estrutura de dicionário
    """
    user = get_user_from_db(username)
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

def zip_user_repositories(user: dict, repositories: dict) -> dict:
    """Faz a união do usuário e seus repositorios e retorna
    dentro de um dicionário"""
    user_repositories = user.copy()
    user_repositories["repositories"] = repositories
    return user_repositories


def parse_repository(repository) -> dict:
    """
    Faz um de-para dos campos e retorna um dicionário
    apenas com os campos necessário do repositório

    Pode receber por parametro um dict ou dicionário
    """

    from_to = {
        "name": "name",
        "url": "html_url",
        "access_type": "private",
        "created_at": "created_at",
        "updated_at": "updated_at",
        "size": "size",
        "stars": "stargazers_count",
        "watchers": "watchers_count",
    }
    if isinstance(repository, dict):
        return {key: repository[value] for key, value in from_to.items()}

    return {key: getattr(repository, key) for key in from_to.keys()}


def parse_repositories(repositories: list) -> list:
    """
    Faz o parse de uma lista de repositórios
    """
    repositories_ = []
    for repository in repositories:
        repositories_.append(parse_repository(repository))
    return repositories_

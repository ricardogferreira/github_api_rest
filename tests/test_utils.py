import collections

from app.utils import parse_repositories, parse_repository, zip_user_repositories


def test_zip_user_repositories(user, parsed_repositories, user_repositories):
    assert user_repositories == zip_user_repositories(user, parsed_repositories)


def test_parse_repository_with_dict(repository, parsed_repository):
    assert parse_repository(repository) == parsed_repository


def test_parse_repository_with_object(parsed_repository):
    Repository = collections.namedtuple("Repository", parsed_repository.keys())
    repository = Repository(**parsed_repository)
    assert parse_repository(repository) == parsed_repository


def test_parse_repositories_with_list_of_objects(parsed_repositories):
    Repository = collections.namedtuple("Repository", parsed_repositories[0].keys())
    repositories = []
    for item in parsed_repositories:
        repositories.append(Repository(**item))
    assert parse_repositories(repositories) == parsed_repositories


def test_parse_repository_with_list_of_dicts(repositories, parsed_repositories):
    assert parse_repositories(repositories) == parsed_repositories
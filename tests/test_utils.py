import collections

from app.utils import (parse_repositories, parse_repository,
                       zip_user_repositories)


def test_zip_user_repositories():
    user = {"test1": "test1", "test2": "test2"}
    repositories = [{"name": "test1"}, {"name": "test2"}]
    expected_user_repositories = user
    expected_user_repositories["repositories"] = repositories
    assert expected_user_repositories == zip_user_repositories(user, repositories)


def test_parse_repository_with_dict():
    repository = {
        "name": "test-repository-1",
        "html_url": "https://test.com/test-repository-1",
        "private": False,
        "created_at": "2020-03-05T01:40:36Z",
        "updated_at": "2020-04-05T07:41:10Z",
        "size": "123",
        "stargazers_count": "135",
        "watchers_count": "120",
    }

    expected = {
        "name": "test-repository-1",
        "url": "https://test.com/test-repository-1",
        "access_type": False,
        "created_at": "2020-03-05T01:40:36Z",
        "updated_at": "2020-04-05T07:41:10Z",
        "size": "123",
        "stars": "135",
        "watchers": "120",
    }

    assert parse_repository(repository) == expected


def test_parse_repository_with_object():

    expected = {
        "name": "test-repository-1",
        "url": "https://test.com/test-repository-1",
        "access_type": False,
        "created_at": "2020-03-05T01:40:36Z",
        "updated_at": "2020-04-05T07:41:10Z",
        "size": "123",
        "stars": "135",
        "watchers": "120",
    }
    Repository = collections.namedtuple("Repository", expected.keys())
    repository = Repository(**expected)
    assert parse_repository(repository) == expected


def test_parse_repositories_with_list_of_objects():
    expected = [
        {
            "name": "test-repository-1",
            "url": "https://test.com/test-repository-1",
            "access_type": False,
            "created_at": "2020-03-05T01:40:36Z",
            "updated_at": "2020-04-05T07:41:10Z",
            "size": "123",
            "stars": "135",
            "watchers": "120",
        },
        {
            "name": "test-repository-2",
            "url": "https://test.com/test-repository-2",
            "access_type": False,
            "created_at": "2019-03-05T01:40:36Z",
            "updated_at": "2029-01-05T07:41:10Z",
            "size": "123",
            "stars": "135",
            "watchers": "120",
        },
    ]

    Repository = collections.namedtuple("Repository", expected[0].keys())
    repositories = []
    for item in expected:
        repositories.append(Repository(**item))
    assert parse_repositories(repositories) == expected


def test_parse_repository_with_list_of_dicts():
    repositories = [
        {
            "name": "test-repository-1",
            "html_url": "https://test.com/test-repository-1",
            "private": False,
            "created_at": "2020-03-05T01:40:36Z",
            "updated_at": "2020-04-05T07:41:10Z",
            "size": "123",
            "stargazers_count": "135",
            "watchers_count": "120",
        },
        {
            "name": "test-repository-2",
            "html_url": "https://test.com/test-repository-2",
            "private": False,
            "created_at": "2019-03-05T01:40:36Z",
            "updated_at": "2019-04-10T07:50:10Z",
            "size": "140",
            "stargazers_count": "150",
            "watchers_count": "0",
        },
    ]

    expected = [
        {
            "name": "test-repository-1",
            "url": "https://test.com/test-repository-1",
            "access_type": False,
            "created_at": "2020-03-05T01:40:36Z",
            "updated_at": "2020-04-05T07:41:10Z",
            "size": "123",
            "stars": "135",
            "watchers": "120",
        },
        {
            "name": "test-repository-2",
            "url": "https://test.com/test-repository-2",
            "access_type": False,
            "created_at": "2019-03-05T01:40:36Z",
            "updated_at": "2019-04-10T07:50:10Z",
            "size": "140",
            "stars": "150",
            "watchers": "0",
        },
    ]

    assert parse_repositories(repositories) == expected
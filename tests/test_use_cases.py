from unittest import mock

import pytest

from github_api_rest.use_cases import (
    get_repositories,
    get_repository_from_github,
    get_user_and_repositories_from_github,
    get_user_repositories_from_local,
    save_changes,
    save_repository,
)

from github_api_rest.exceptions import (
    DatabaseRepositoryNotFoundError,
    DatabaseUserNotFoundError,
)


class UserMock:
    def __init__(self, id, username, repositories):
        self.id = id
        self.username = username
        self.repositories = repositories


def test_get_repositories_using_local_data(username, mocker):
    get_user_repositories_from_local_mock = mocker.patch(
        "github_api_rest.use_cases.get_user_repositories_from_local"
    )

    get_repositories(username, from_local=True)

    assert get_user_repositories_from_local_mock.called


def test_get_repositories_using_github_data(username, mocker):
    get_user_and_repositories_from_github_mock = mocker.patch(
        "github_api_rest.use_cases.get_user_and_repositories_from_github"
    )

    get_repositories(username, from_local=False)

    assert get_user_and_repositories_from_github_mock.called


def test_get_user_and_repositories_from_github(
    repositories, parsed_repositories, username, user, user_repositories, mocker
):

    get_repositories_by_username_mock = mocker.patch(
        "github_api_rest.use_cases.get_repositories_by_username",
        return_value=repositories,
    )
    parse_user_mock = mocker.patch(
        "github_api_rest.use_cases.parse_user", return_value=user
    )
    parse_repositories_mock = mocker.patch(
        "github_api_rest.use_cases.parse_repositories", return_value=parsed_repositories
    )
    zip_user_repositories_mock = mocker.patch(
        "github_api_rest.use_cases.zip_user_repositories",
        return_value=user_repositories,
    )

    user_and_repositories = get_user_and_repositories_from_github(username)

    get_repositories_by_username_mock.assert_called_with(username)
    parse_user_mock.assert_called_with(repositories)
    parse_repositories_mock.assert_called_with(repositories)
    zip_user_repositories_mock.assert_called_with(user, parsed_repositories)
    assert user_and_repositories == user_repositories


def test_get_repository_from_github_with_save_data(
    parsed_repository, repository, repository_name, username, mocker
):
    get_repository_by_username_and_name_mock = mocker.patch(
        "github_api_rest.use_cases.get_repository_by_username_and_name",
        return_value=repository,
    )

    parse_repository_mock = mocker.patch(
        "github_api_rest.use_cases.parse_repository", return_value=parsed_repository
    )

    save_repository_mock = mocker.patch("github_api_rest.use_cases.save_repository")

    get_repository_from_github(username, repository_name, save_data=True)

    get_repository_by_username_and_name_mock.assert_called_with(
        username, repository_name
    )
    parse_repository_mock.assert_called_with(repository)
    assert save_repository_mock.called


def test_get_repository_from_github_without_save_data(
    repository, parsed_repository, repository_name, username, mocker
):
    save_data = False
    get_repository_by_username_and_name_mock = mocker.patch(
        "github_api_rest.use_cases.get_repository_by_username_and_name",
        return_value=repository,
    )

    parse_repository_mock = mocker.patch(
        "github_api_rest.use_cases.parse_repository", return_value=parsed_repository
    )

    save_repository_mock = mocker.patch("github_api_rest.use_cases.save_repository")

    get_repository_from_github(username, repository_name, save_data)

    get_repository_by_username_and_name_mock.assert_called_with(
        username, repository_name
    )
    parse_repository_mock.assert_called_with(repository)
    assert save_repository_mock.not_called


def test_get_user_repositories_from_local(
    user_id, username, parsed_repositories, user, user_repositories, mocker
):
    user_mock = UserMock(user_id, username, parsed_repositories)
    get_user_from_db_mock = mocker.patch(
        "github_api_rest.use_cases.get_user_from_db", return_value=user_mock
    )

    zip_user_repositories_mock = mocker.patch(
        "github_api_rest.use_cases.zip_user_repositories",
        return_value=user_repositories,
    )

    parse_repositories_mock = mocker.patch(
        "github_api_rest.use_cases.parse_repositories",
        return_value=parsed_repositories,
    )

    assert get_user_repositories_from_local(username) == user_repositories
    get_user_from_db_mock.assert_called_with(username)
    parse_repositories_mock.assert_called_with(user_mock.repositories)
    zip_user_repositories_mock.assert_called_with(user, parsed_repositories)


def test_save_changes(user_id, username, repositories, mocker):
    db_mock = mocker.patch(
        "github_api_rest.use_cases.db",
    )
    db_mock = mocker.patch(
        "github_api_rest.use_cases.db",
    )

    user_mock = UserMock(user_id, username, repositories)
    save_changes(user_mock)

    db_mock.session.add.assert_called_with(user_mock)
    assert db_mock.session.commit.called


def test_save_repository(user_id, username, repository_name, parsed_repository, mocker):
    repositories_mock = mock.Mock()
    user_mock = UserMock(user_id, username, repositories_mock)
    get_user_from_db_mock = mocker.patch(
        "github_api_rest.use_cases.get_user_from_db", return_value=user_mock
    )

    get_repository_from_db_mock = mocker.patch(
        "github_api_rest.use_cases.get_repository_from_db",
    )

    save_changes_mock = mocker.patch(
        "github_api_rest.use_cases.save_changes",
    )

    save_repository(user_id, username, repository_name, parsed_repository)

    get_user_from_db_mock.assert_called_with(username)
    get_repository_from_db_mock.assert_called_with(name=repository_name, user=user_mock)
    assert repositories_mock.append.called
    save_changes_mock.assert_called_with(user_mock)


def test_save_repository_with_user_error(
    user_id, username, repository_name, parsed_repository, mocker
):
    get_user_from_db_mock = mocker.patch("github_api_rest.use_cases.get_user_from_db")
    mocker.patch(
        "github_api_rest.use_cases.get_repository_from_db",
    )

    mocker.patch(
        "github_api_rest.use_cases.save_changes",
    )
    get_user_from_db_mock.side_effect = DatabaseUserNotFoundError()
    UserMock = mocker.patch("github_api_rest.use_cases.User")

    save_repository(user_id, username, repository_name, parsed_repository)

    assert UserMock.called


def test_save_repository_with_repository_error(
    user_id, username, repository_name, parsed_repository, mocker
):
    mocker.patch("github_api_rest.use_cases.get_user_from_db")
    get_repository_from_db_mock = mocker.patch(
        "github_api_rest.use_cases.get_repository_from_db",
    )

    mocker.patch(
        "github_api_rest.use_cases.save_changes",
    )
    get_repository_from_db_mock.side_effect = DatabaseRepositoryNotFoundError()
    RepositoryMock = mocker.patch("github_api_rest.use_cases.Repository")

    save_repository(user_id, username, repository_name, parsed_repository)

    assert RepositoryMock.called

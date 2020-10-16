from unittest.mock import Mock

import pytest
from requests.exceptions import HTTPError

from github_api_rest.external import (
    get_repositories_by_username,
    get_repository_by_username_and_name,
    parse_user,
    request_external_to_json,
)


def test_parse_user(user, repositories):
    assert parse_user(repositories) == user


def test_get_repositories_by_username(username, repositories, mocker):
    expected_return = repositories
    request_external_to_json_mock = mocker.patch(
        "github_api_rest.external.request_external_to_json", return_value=expected_return
    )
    repositories = get_repositories_by_username(username)
    request_external_to_json_mock.assert_called_with(
        "https://api.github.com/users/test123/repos"
    )
    assert repositories == expected_return


def test_get_repository_by_username_and_name(
    username, repository_name, repository, mocker
):
    expected_return = repository
    request_external_to_json_mock = mocker.patch(
        "github_api_rest.external.request_external_to_json", return_value=expected_return
    )
    repository = get_repository_by_username_and_name(username, repository_name)
    request_external_to_json_mock.assert_called_with(
        "https://api.github.com/repos/test123/test_repository1"
    )

    assert repository == expected_return


def test_request_external_to_json(mocker):
    expected_return = {"test": "test"}

    response_mock = Mock()
    raise_for_status_mock = Mock()
    response_mock.raise_for_status = raise_for_status_mock
    response_mock.json.return_value = expected_return
    get_mock = mocker.patch("requests.get", return_value=response_mock)

    url = "https://api.test.com/test"
    response_json = request_external_to_json(url)

    get_mock.assert_called_with(url)
    assert raise_for_status_mock.called
    assert response_json == expected_return


def test_request_external_to_json_raise_error(mocker):
    response_mock = Mock()
    raise_for_status_mock = Mock()
    raise_for_status_mock.side_effect = HTTPError(Mock(status=404), "not found")
    response_mock.raise_for_status = raise_for_status_mock
    mocker.patch("requests.get", return_value=response_mock)

    with pytest.raises(HTTPError):
        url = "https://api.test.com/test"
        request_external_to_json(url)

    assert response_mock.json.not_called
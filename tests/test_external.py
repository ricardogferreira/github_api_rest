from unittest.mock import Mock

import pytest
from requests.exceptions import HTTPError

from app.external import (
    parse_user,
    get_repositories_by_username,
    get_repository_by_username_and_name,
    request_external_to_json,
)


def test_parse_user():
    expected = {"user_id": 123, "username": "test123"}
    repository = {"owner": {"id": 123, "login": "test123"}}
    repositories = [repository]
    assert parse_user(repositories) == expected


def test_get_repositories_by_username(mocker):
    username = "test123"
    expected_return = [{"test": "test"}, {"test2": "test2"}]
    request_external_to_json_mocked = mocker.patch(
        "app.external.request_external_to_json", return_value=expected_return
    )
    repositories = get_repositories_by_username(username)
    request_external_to_json_mocked.assert_called_with(
        "https://api.github.com/users/test123/repos"
    )
    assert repositories == expected_return


def test_get_repository_by_username_and_name(mocker):
    username = "test123"
    repository_name = "repository_test123"
    expected_return = {"test": "test"}
    request_external_to_json_mocked = mocker.patch(
        "app.external.request_external_to_json", return_value=expected_return
    )
    repository = get_repository_by_username_and_name(username, repository_name)
    request_external_to_json_mocked.assert_called_with(
        "https://api.github.com/repos/test123/repository_test123"
    )

    assert repository == expected_return


def test_request_external_to_json(mocker):
    expected_return = {"test": "test"}

    response_mocked = Mock()
    raise_for_status_mocked = Mock()
    response_mocked.raise_for_status = raise_for_status_mocked
    response_mocked.json.return_value = expected_return
    get_mocked = mocker.patch("requests.get", return_value=response_mocked)

    url = "https://api.test.com/test"
    response_json = request_external_to_json(url)

    get_mocked.assert_called_with(url)
    assert raise_for_status_mocked.called
    assert response_json == expected_return


def test_request_external_to_json_raise_error(mocker):
    response_mocked = Mock()
    raise_for_status_mocked = Mock()
    raise_for_status_mocked.side_effect = HTTPError(Mock(status=404), "not found")
    response_mocked.raise_for_status = raise_for_status_mocked
    mocker.patch("requests.get", return_value=response_mocked)

    with pytest.raises(HTTPError):
        url = "https://api.test.com/test"
        request_external_to_json(url)

    assert response_mocked.json.not_called
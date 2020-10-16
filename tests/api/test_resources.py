import pytest
from requests.exceptions import ConnectionError, HTTPError

from app.exceptions import DatabaseUserNotFoundError


@pytest.mark.parametrize(
    "from_local_text, from_local",
    [("", False), ("true", True), ("false", False)],
    ids=["without-from-local", "from-local-true", "from-local-false"],
)
def test_get_repositories_from_user(
    from_local_text, from_local, client, parsed_repositories, username, mocker
):
    get_repositories_mock = mocker.patch(
        "app.resources.get_repositories", return_value=parsed_repositories
    )
    response = client.get(
        f"/repositories?username={username}&from_local={from_local_text}"
    )
    assert 200 == response.status_code
    assert parsed_repositories == response.get_json()
    get_repositories_mock.assert_called_with(from_local=from_local, username=username)


@pytest.mark.parametrize(
    "exc,message_error",
    [
        (ConnectionError, "Falha ao buscar o usuário"),
        (HTTPError, "Falha ao buscar o usuário"),
        (DatabaseUserNotFoundError, "Usuário não encontrado na base de dados"),
    ],
)
def test_get_repositories_from_user_with_error(
    exc, message_error, client, parsed_repositories, username, mocker
):
    get_repositories_mock = mocker.patch(
        "app.resources.get_repositories", return_value=parsed_repositories
    )
    get_repositories_mock.side_effect = exc()
    response = client.get(f"/repositories?username={username}")
    assert 400 == response.status_code
    assert response.get_json() == {"message": message_error}
    assert get_repositories_mock.called


@pytest.mark.parametrize("save_data", [True, False])
def test_get_repository_by_username_and_repository_name(
    save_data, client, parsed_repository, username, repository_name, mocker
):
    get_repository_from_github_mock = mocker.patch(
        "app.resources.get_repository_from_github", return_value=parsed_repository
    )
    response = client.get(
        f"/users/{username}/repositories/{repository_name}/?save_data={save_data}"
    )
    assert 200 == response.status_code
    assert parsed_repository == response.get_json()
    get_repository_from_github_mock.assert_called_with(
        username,
        repository_name,
        save_data=save_data,
    )


@pytest.mark.parametrize(
    "exc,message_error,save_data",
    [
        (ConnectionError, "Falha ao buscar o repositório no github", True),
        (HTTPError, "Falha ao buscar o repositório no github", True),
    ],
)
def test_get_repository_by_username_and_repository_name_with_error(
    exc,
    message_error,
    save_data,
    client,
    parsed_repository,
    username,
    repository_name,
    mocker,
):

    get_repository_from_github_mock = mocker.patch(
        "app.resources.get_repository_from_github", return_value=parsed_repository
    )

    get_repository_from_github_mock.side_effect = exc()
    response = client.get(
        f"/users/{username}/repositories/{repository_name}/?save_data={save_data}"
    )

    assert 400 == response.status_code
    assert response.get_json() == {"message": message_error}
    assert get_repository_from_github_mock.called

from app.use_cases import (
    get_repositories,
    get_repository_from_github,
    get_user_and_repositories_from_github,
    get_user_repositories_from_local,
)


def test_get_repositories_using_local_data(username, mocker):
    get_user_repositories_from_local_mocked = mocker.patch(
        "app.use_cases.get_user_repositories_from_local"
    )

    get_repositories(username, from_local=True)

    assert get_user_repositories_from_local_mocked.called


def test_get_repositories_using_github_data(username, mocker):
    get_user_and_repositories_from_github_mocked = mocker.patch(
        "app.use_cases.get_user_and_repositories_from_github"
    )

    get_repositories(username, from_local=False)

    assert get_user_and_repositories_from_github_mocked.called


def test_get_user_and_repositories_from_github(
    repositories, parsed_repositories, username, user, user_repositories, mocker
):

    get_repositories_by_username_mocked = mocker.patch(
        "app.use_cases.get_repositories_by_username", return_value=repositories
    )
    parse_user_mocked = mocker.patch("app.use_cases.parse_user", return_value=user)
    parse_repositories_mocked = mocker.patch(
        "app.use_cases.parse_repositories", return_value=parsed_repositories
    )
    zip_user_repositories_mocked = mocker.patch(
        "app.use_cases.zip_user_repositories", return_value=user_repositories
    )

    user_and_repositories = get_user_and_repositories_from_github(username)

    get_repositories_by_username_mocked.assert_called_with(username)
    parse_user_mocked.assert_called_with(repositories)
    parse_repositories_mocked.assert_called_with(repositories)
    zip_user_repositories_mocked.assert_called_with(user, parsed_repositories)
    assert user_and_repositories == user_repositories


def test_get_repository_from_github_with_save_data(
    parsed_repository, repository, repository_name, username, mocker
):
    get_repository_by_username_and_name_mocked = mocker.patch(
        "app.use_cases.get_repository_by_username_and_name",
        return_value=repository,
    )

    parse_repository_mocked = mocker.patch(
        "app.use_cases.parse_repository", return_value=parsed_repository
    )

    save_repository_mocked = mocker.patch("app.use_cases.save_repository")

    get_repository_from_github(username, repository_name, save_data=True)

    get_repository_by_username_and_name_mocked.assert_called_with(
        username, repository_name
    )
    parse_repository_mocked.assert_called_with(repository)
    assert save_repository_mocked.called


def test_get_repository_from_github_without_save_data(
    repository, parsed_repository, repository_name, username, mocker
):
    save_data = False
    get_repository_by_username_and_name_mocked = mocker.patch(
        "app.use_cases.get_repository_by_username_and_name",
        return_value=repository,
    )

    parse_repository_mocked = mocker.patch(
        "app.use_cases.parse_repository", return_value=parsed_repository
    )

    save_repository_mocked = mocker.patch("app.use_cases.save_repository")

    get_repository_from_github(username, repository_name, save_data)

    get_repository_by_username_and_name_mocked.assert_called_with(
        username, repository_name
    )
    parse_repository_mocked.assert_called_with(repository)
    assert save_repository_mocked.not_called
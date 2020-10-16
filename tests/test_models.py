from github_api_rest.models import Repository, User


def test_user_repr():
    user = User(username="test")
    assert repr(user) == "<User 'test'>"


def test_repository_repr():
    repository = Repository(name="test repository")
    assert repr(repository) == "<Repository 'test repository'>"


def test_repository_str():
    repository = Repository(name="test repository")
    assert str(repository) == "test repository"


def test_repository_str_without_value():
    repository = Repository()
    assert str(repository) == ""

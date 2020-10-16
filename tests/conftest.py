from pytest import fixture


@fixture
def username():
    return "test123"


@fixture
def user_id():
    return 123


@fixture
def owner(username, user_id):
    return {"id": user_id, "login": username}


@fixture
def repository_name():
    return "test_repository1"


@fixture
def repository(owner, repository_name):
    return {
        "name": repository_name,
        "size": 150,
        "owner": owner,
    }


@fixture
def repository2(owner):
    return {"name": "repo2", "size": 3, "owner": owner}


@fixture
def user(username, user_id):
    {"user_id": user_id, "username": username}


@fixture
def parsed_repository(repository_name):
    return {"name": repository_name, "size": 150}


@fixture
def parsed_repository2():
    return ({"name": "repo2", "size": 3, "owner": owner},)


@fixture
def repositories(repository, repository2):
    return [repository, repository2]


@fixture
def parsed_repositories(parsed_repository, parsed_repository2):
    return [parsed_repository, parsed_repository2]


@fixture
def user_repositories(username, user_id):
    return {
        "username": username,
        "user_id": user_id,
        "repositories": parsed_repositories,
    }
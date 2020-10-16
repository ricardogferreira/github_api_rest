from pytest import fixture


@fixture
def username():
    return "test123"


@fixture
def owner(username):
    return {"id": 123, "login": username}


@fixture
def repository_name():
    return "test_repository_1222"


@fixture
def repository(owner, repository_name):
    return {
        "name": repository_name,
        "size": 150,
        "owner": owner,
    }


@fixture
def user(username):
    {"user_id": 123, "username": username}


@fixture
def parsed_repository():
    return {"name": "test_repository_1222", "size": 150}
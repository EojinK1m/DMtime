from pytest import fixture

url = "/api/v1/me"


@fixture
def get_me(client):
    def _get_me(access_token):
        return client.get(
            url,
            headers={"authorization": "Bearer " + access_token}
        )

    return _get_me


@fixture
def temp_user(create_temp_account):
    return create_temp_account()


def test_get_me_success_response_200(temp_user, get_me):
    rv = get_me(
        temp_user.generate_access_token()
    )

    assert rv.status_code == 200
    assert rv.json


def test_get_me_without_access_token_response_401(get_me):
    rv = get_me(
        ''
    )

    assert rv.status_code == 401

from pytest import fixture

@fixture
def test_user(create_temp_account):
    return create_temp_account()

def login(client, json):
    return client.post(
        '/api/v1/token',
        json = json
    )

def test_login_correctly_response_201_access_token(client, test_user):
    rv = login(
        client,
        {
            'email':test_user.email,
            'password':'test_password_1'
        }
    )

    assert rv.status_code == 201
    assert rv.json['access_token']

def test_login_failed_response_401(client, test_user):
    rv = login(
        client,
        {
            'email':test_user.email,
            'password':'wrong_password1'
        }
    )

    assert rv.status_code == 401


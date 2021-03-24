from pytest import fixture

@fixture
def test_user(create_temp_account):
    test_user = create_temp_account()
    test_user.password = test_user.username.replace('user', 'password')

    return test_user

def get_user_path(user):
    return f'/api/v1/users/{user.username}/account'

def get_access_token(user):
    return user.generate_access_token()

def delete_account(client, user, json, access_token):
    return client.delete(
        get_user_path(user),
        json = json,
        headers = {'authorization':'Bearer ' + access_token}
    )

def test_delete_account_correctly_response_200(client, test_user):
    rv = delete_account(
        client=client,
        user=test_user,
        access_token=get_access_token(test_user)
    )
    assert rv.status_code == 200

def test_account_delete_without_jwt_request_response_422(client, test_user):
    rv = delete_account(
        client=client,
        user=test_user,
        access_token=''
    )

    assert rv.status_code == 422

def test_delete_account_without_permission_response_403(client, test_user):
    rv = delete_account(
        client=client,
        user=test_user,
        access_token=get_access_token(test_user)
    )

    assert rv.status_code == 403

def get_account_information(client, test_user, access_token):
    return client.get(
        get_user_path(test_user),
        headers={'authorization': 'Bearer ' + access_token}
    )

def test_get_account_correctly_response_200(client, test_user):
    rv = get_account_information(client, test_user, get_account_information(test_user))

    assert rv.status_code == 200

    account_info = rv.json['account_info']
    assert account_info
    assert account_info['email'] == test_user.email

def test_get_account_without_permission_response_403(client, test_user):
    test_user.username += 'test'

    rv = get_account_information(
        client,
        test_user,
        get_access_token(test_user)
    )

    assert rv.status_code == 403


def change_password(client, user, password, access_token):
    return client.put(
        get_user_path(user)  + '/password',
        headers={'authorization': 'Bearer ' + access_token},
        json = {'password':password}
    )

def test_change_password_correctly_response_200(client, test_user):
    rv = change_password(
        client,
        test_user,
        'changepass123',
        get_access_token(test_user)
    )

    assert rv.status_code == 200

def test_change_password_without_permission_response_403(client, test_user):
    test_user.username += 'test'

    rv = change_password(
        client,
        test_user,
        'changePass1',
        get_access_token(test_user)
    )

    assert rv.status_code == 403

def test_change_password_forbidden_password_response_400(client, test_user):
    rv = change_password(
        client,
        test_user,
        'changepass',
        get_access_token(test_user)
    )

    assert rv.status_code == 400

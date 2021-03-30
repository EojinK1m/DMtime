from pytest import fixture


@fixture
def test_user(create_temp_account):
    test_user = create_temp_account()
    test_user.password = test_user.username.replace("user", "password")

    return test_user


def get_user_account_path(user):
    return f"/api/v1/users/{user.username}/account"


def get_access_token(user):
    return user.generate_access_token()


def delete_account(client, user, json, access_token):
    return client.delete(
        get_user_account_path(user),
        json=json,
        headers={"authorization": "Bearer " + access_token},
    )


def test_delete_account_correctly_response_200(client, test_user):
    rv = delete_account(
        client=client,
        user=test_user,
        json={"password": test_user.password},
        access_token=get_access_token(test_user),
    )

    assert rv.status_code == 200


def test_delete_account_without_jwt_request_response_422(client, test_user):
    rv = delete_account(
        client=client,
        user=test_user,
        json={"password": test_user.password},
        access_token="",
    )

    assert rv.status_code == 422


def test_delete_account_without_permission_response_403(
    client, test_user, create_temp_account
):
    another_user = create_temp_account()

    rv = delete_account(
        client=client,
        user=test_user,
        json={"password": test_user.password},
        access_token=get_access_token(another_user),
    )

    assert rv.status_code == 403


def test_delete_account_with_wrong_password_response_401(client, test_user):
    rv = delete_account(
        client=client,
        user=test_user,
        json={"password": test_user.password + "wrong"},
        access_token=get_access_token(test_user),
    )

    assert rv.status_code == 401


def test_delete_account_without_password_response_400(client, test_user):
    rv = delete_account(
        client=client, user=test_user, json={}, access_token=get_access_token(test_user)
    )

    assert rv.status_code == 400


def get_account_information(client, test_user, access_token):
    return client.get(
        get_user_account_path(test_user),
        headers={"authorization": "Bearer " + access_token},
    )


def test_get_account_correctly_response_200(client, test_user):
    rv = get_account_information(client, test_user, get_access_token(test_user))

    assert rv.status_code == 200
    assert rv.json["email"] == test_user.email


def test_get_account_without_permission_response_403(
    client, test_user, create_temp_account
):
    another_user = create_temp_account()

    rv = get_account_information(
        client,
        test_user,
        get_access_token(another_user)
    )

    assert rv.status_code == 403


def change_password(client, user, password, new_password, access_token):
    return client.put(
        get_user_account_path(user) + "/password",
        headers={"authorization": "Bearer " + access_token},
        json={"new_password": new_password, "password": password},
    )


def test_change_password_correctly_response_200(client, test_user):
    rv = change_password(
        client,
        test_user,
        test_user.password,
        "changepass123",
        get_access_token(test_user)
    )

    assert rv.status_code == 200


def test_change_password_without_permission_response_403(
    client,
    test_user,
    create_temp_account
):
    another_user = create_temp_account()

    rv = change_password(
        client,
        test_user,
        test_user.password,
        "changePass1",
        get_access_token(another_user)
    )

    assert rv.status_code == 403


def test_change_password_forbidden_password_response_400(client, test_user):
    rv = change_password(
        client,
        test_user,
        test_user.password,
        "changepass",
        get_access_token(test_user)
    )

    assert rv.status_code == 400


def test_change_password_with_wrong_password_response_401(client, test_user):
    rv = change_password(
        client,
        test_user,
        test_user.password+"wrong",
        "changePasss123",
        get_access_token(test_user)
    )

    assert rv.status_code == 401
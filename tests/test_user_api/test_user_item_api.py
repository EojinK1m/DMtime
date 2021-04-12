from pytest import fixture


@fixture
def test_user(create_temp_account, create_temp_image):
    test_image = create_temp_image()
    return create_temp_account(profile_image=test_image)


def get_user_path(user):
    return "/api/v1/users/" + user.username


def get_access_token_of_user(user):
    return user.generate_access_token()


def patch_user(client, user, access_token, json):
    return client.put(
        get_user_path(user),
        headers={"authorization": "Bearer " + access_token},
        json=json,
    )


def test_get_user_information_response_200(client, test_user):
    rv = client.get(get_user_path(test_user))

    assert rv.status_code == 200
    user_info = rv.json
    assert user_info
    assert user_info["username"] == test_user.username
    assert user_info["explain"] == test_user.explain
    assert user_info["profile_image"] == test_user.profile_image.id


def test_put_user(client, test_user):
    change_username = test_user.username + "c"

    rv = patch_user(
        client=client,
        user=test_user,
        access_token=get_access_token_of_user(test_user),
        json={
            "username": change_username,
            "profile_image": test_user.profile_image.id,
            "user_explain": test_user.explain,
        },
    )

    assert rv.status_code == 200
    assert test_user.username == change_username


def test_patch_user_information_with_wrong_data(client, test_user):

    rv = patch_user(
        client=client,
        user=test_user,
        access_token=get_access_token_of_user(test_user),
        json={"wrong_key": "wrong_value"},
    )

    assert rv.status_code == 400


def test_patch_user_information_with_exist_data(client, test_user):
    rv = patch_user(
        client=client,
        user=test_user,
        access_token=get_access_token_of_user(test_user),
        json={
            "username": test_user.username,
            "user_explain": test_user.explain,
            "profile_image": test_user.profile_image.id,
        },
    )

    assert rv.status_code == 409


def test_patch_user_information_without_access_token_response_422(
    client, test_user
):
    rv = patch_user(
        client=client,
        user=test_user,
        access_token="",
        json={
            "username": test_user.username,
            "user_explain": test_user.explain,
            "profile_image_id": test_user.profile_image.id,
        },
    )

    assert rv.status_code == 422


def test_patch_another_user_information_response_403(
    client, test_user, create_temp_account
):
    another_user = create_temp_account()

    rv = patch_user(
        client=client,
        user=another_user,
        access_token=get_access_token_of_user(test_user),
        json={},
    )

    assert rv.status_code == 403

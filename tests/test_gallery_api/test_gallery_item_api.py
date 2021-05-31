from pytest import fixture


url = "/api/v1/board/galleries/"


def test_gallery_delete_correct(
    client, create_temp_account, create_temp_gallery
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery(temp_account)

    rv = client.delete(
        url + f"{temp_gallery.gallery_id}",
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
    )

    assert rv.status_code == 200


def test_gallery_delete_without_authority(
    client, create_temp_account, create_temp_gallery
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()

    rv = client.delete(
        url + f"{temp_gallery.gallery_id}",
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
    )

    assert rv.status_code == 403


def test_gallery_patch_correct(
    client, create_temp_account, create_temp_gallery
):
    admin_account = create_temp_account(is_admin=True)
    temp_gallery = create_temp_gallery()

    changing_gallery_info = {
        "name": "change_gallery_info",
        "explain": "this is explain of changed gallery",
    }
    rv = client.patch(
        url + f"{temp_gallery.gallery_id}",
        headers={
            "authorization": "Bearer " + admin_account.generate_access_token()
        },
        json=changing_gallery_info,
    )

    assert rv.status_code == 200


def test_gallery_patch_with_data_miss(
    client, create_temp_account, create_temp_gallery
):
    admin_account = create_temp_account(is_admin=True)

    temp_gallery = create_temp_gallery()

    changing_gallery_info_explain_missed = {"name": "change_gallery_info"}
    rv = client.patch(
        url + f"{temp_gallery.gallery_id}",
        headers={
            "authorization": "Bearer " + admin_account.generate_access_token()
        },
        json=changing_gallery_info_explain_missed,
    )

    assert rv.status_code == 200

    changing_gallery_info_name_missed = {
        "explain": "this is explain of changed gallery"
    }
    rv_2 = client.patch(
        url + f"{temp_gallery.gallery_id}",
        headers={
            "authorization": "Bearer " + admin_account.generate_access_token()
        },
        json=changing_gallery_info_name_missed,
    )

    assert rv_2.status_code == 200, rv_2.json["msg"]


def test_gallery_patch_to_already_exist_gallery_name(
    client, create_temp_account, create_temp_gallery
):
    temp_account = create_temp_account()
    temp_gallery1, temp_gallery2 = (
        create_temp_gallery(temp_account),
        create_temp_gallery(temp_account),
    )

    rv = client.patch(
        url + f"{temp_gallery1.gallery_id}",
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
        json={"name": temp_gallery2.name},
    )

    assert rv.status_code == 409


@fixture
def get_gallery(client):
    def get_gallery_(gallery_id, access_token):
        return client.get(
            url + str(gallery_id),
            headers={"authorization": "Bearer " + access_token}
        )

    return get_gallery_


def test_get_gallery_success_response_200_and_expected_response(get_gallery, create_temp_account, create_temp_gallery):
    temp_user = create_temp_account()
    another_temp_user = create_temp_account()
    temp_gallery = create_temp_gallery(manager_user=temp_user)

    rv = get_gallery(temp_gallery.id, temp_user.generate_access_token())
    rv2 = get_gallery(temp_gallery.id, another_temp_user.generate_access_token())

    assert rv.status_code == 200
    assert rv.json['is_mine'] is True
    assert rv2.json['is_mine'] is False


def test_get_gallery_without_wrong_access_token_response_422(get_gallery, create_temp_gallery):
    temp_gallery = create_temp_gallery()

    rv = get_gallery(
        gallery_id=temp_gallery.id,
        access_token=''
    )

    assert rv.status_code == 422


def test_get_not_exist_gallery_response_404(get_gallery, create_temp_account):
    temp_user = create_temp_account()

    rv = get_gallery(
        gallery_id="not-exist_gallery-id",
        access_token=temp_user.generate_access_token()
    )

    assert rv.status_code == 404

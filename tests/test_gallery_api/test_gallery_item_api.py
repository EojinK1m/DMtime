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


8


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

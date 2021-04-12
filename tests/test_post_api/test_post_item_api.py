from pytest import fixture


url = "/api/v1/board/posts/"


@fixture
def get_post(client):
    def _get_post(post_id, access_token):
        return client.get(
            url + f"{post_id}",
            headers={"authorization": "Bearer " + access_token},
        )

    return _get_post


def test_post_get_correct(
    client, create_temp_account, create_temp_gallery, create_temp_post, get_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    rv = get_post(
        post_id=temp_post.id,
        access_token=temp_account.generate_access_token()
    )

    assert rv.status_code == 200

    assert rv.json
    expected_keys_of_post = (
        "id",
        "title",
        "posted_gallery",
        "content",
        "posted_datetime",
        "uploader",
        "number_of_likes",
        "number_of_dislikes",
        "views",
        "is_anonymous",
        "my_reaction"
    )
    for expect_key in expected_keys_of_post:
        assert expect_key in rv.json.keys()

    assert rv.json["posted_gallery"]["name"] == temp_gallery.name
    assert rv.json["uploader"]["username"] == temp_account.username
    assert rv.json["my_reaction"] == 'none'


def test_anonymous_post_get_correct(
    client, create_temp_account, create_temp_gallery, create_temp_post, get_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
        is_anonymous=True,
    )

    rv = get_post(
        post_id=temp_post.id,
        access_token=temp_account.generate_access_token()
    )
    assert rv.status_code == 200
    assert rv.json["uploader"]["username"] == "익명의 대마인"


def test_get_post_has_postlike_correctly_response(
    client, create_temp_account, create_temp_gallery, create_temp_post, create_temp_postlike, get_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
        is_anonymous=True,
    )
    create_temp_postlike(
        post_id=temp_post.id,
        liker_id=temp_account.email
    )

    rv = get_post(
        post_id=temp_post.id,
        access_token=temp_account.generate_access_token()
    )

    assert rv.json["number_of_likes"] == 1
    assert rv.json["number_of_dislikes"] == 0
    assert rv.json["my_reaction"] == "like"


def test_post_get_not_exist(client, create_temp_account, get_post):
    temp_account = create_temp_account()

    rv = get_post(
        post_id=1,
        access_token=temp_account.generate_access_token()
    )

    assert rv.status_code == 404


def test_post_delete_correct(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    rv = client.delete(
        url + f"{temp_post.id}",
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
    )

    assert rv.status_code == 200


def test_post_delete_with_admin_account(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    admin_account = create_temp_account(is_admin=True)
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    rv = client.delete(
        url + f"{temp_post.id}",
        headers={
            "authorization": "Bearer " + admin_account.generate_access_token()
        },
    )

    assert rv.status_code == 200


def test_post_delete_with_another_account(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    temp_account = create_temp_account()
    temp_account2 = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    rv = client.delete(
        url + f"{temp_post.id}",
        headers={
            "authorization": "Bearer " + temp_account2.generate_access_token()
        },
    )

    assert rv.status_code == 403


def test_post_patch_correct(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    change_post_info = {
        "title": "Nanana Nanana nana kissing",
        "content": "my name is blurry face and i care what u think",
    }

    rv = client.patch(
        url + f"{temp_post.id}",
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
        json=change_post_info,
    )

    assert rv.status_code == 200


def test_post_patch_with_data_miss(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    change_post_info = {
        "content": "my name is blurry face and i care what u think"
    }

    rv = client.patch(
        url + f"{temp_post.id}",
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
        json=change_post_info,
    )

    assert rv.status_code == 200


def test_post_patch_with_another_account(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    temp_account = create_temp_account()
    temp_account2 = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    change_post_info = {
        "title": "Nanana Nanana nana kissing strangers",
        "content": "my name is blurry face and i care what u think",
    }

    rv = client.patch(
        url + f"{temp_post.id}",
        headers={
            "authorization": "Bearer " + temp_account2.generate_access_token()
        },
        json=change_post_info,
    )

    assert rv.status_code == 403


def test_post_patch_images_correct(
    client,
    create_temp_account,
    create_temp_gallery,
    create_temp_post,
    create_temp_image,
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_image = create_temp_image()
    temp_image_2 = create_temp_image()

    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    rv = client.patch(
        url + f"{temp_post.id}",
        json={"images": [temp_image.id]},
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
    )
    assert rv.status_code == 200

    rv2 = client.patch(
        url + f"{temp_post.id}",
        json={"images": [temp_image.id, temp_image_2.id]},
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
    )
    assert (
        rv2.status_code == 200
    ), "images = [temp_image.id, temp_image_2.id]"

    rv4 = client.patch(
        url + f"{temp_post.id}",
        json={"images": []},
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
    )
    assert rv4.status_code == 200, "images = []"


def test_post_patch_image_id_none(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    rv = client.patch(
        url + f"{temp_post.id}",
        json={"images": None},
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
    )

    assert rv.status_code == 400, "images = None"


def test_post_like_post_correct(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )
    access_token = temp_account.generate_access_token()

    rv = client.post(
        url + f"{temp_post.id}/like",
        headers={"authorization": "Bearer " + access_token},
    )

    assert rv.status_code == 201
    assert rv.json["number_of_likes"] == 1

    rv2 = client.delete(
        url + f"{temp_post.id}/like",
        headers={"authorization": "Bearer " + access_token},
    )

    assert rv2.status_code == 200
    assert rv2.json["number_of_likes"] == 0


def test_post_like_post_without_access_token(
    client, create_temp_account, create_temp_gallery, create_temp_post
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )

    rv = client.post(url + f"{temp_post.id}/like")
    assert rv.status_code == 401


def test_delete_post_have_like(
    client,
    create_temp_account,
    create_temp_gallery,
    create_temp_post,
    create_temp_postlike,
):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email,
        upload_gallery_id=temp_gallery.gallery_id,
    )
    create_temp_postlike(
        liker_id=temp_account.email, post_id=temp_post.id
    )

    rv = client.delete(
        url + f"{temp_post.id}",
        headers={
            "authorization": "Bearer " + temp_account.generate_access_token()
        },
    )

    assert rv.status_code == 200

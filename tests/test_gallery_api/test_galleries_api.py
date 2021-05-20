from pytest import fixture

url = "/api/v1/board/galleries"


@fixture
def post_gallery(client):
    def post_gallery_(
        access_token,
        gallery_id="default-id",
        name="기본갤러리 이름",
        explain="기본 갤러리 설명입니다.",
        gallery_type=2,
    ):
        return client.post(
            url,
            json={
                "gallery_id": gallery_id,
                "name": name,
                "explain": explain,
                "gallery_type": gallery_type,
            },
            headers={"authorization": "Bearer " + access_token},
        )

    return post_gallery_


@fixture
def temp_admin_account(create_temp_account):
    return create_temp_account(is_admin=True)


@fixture
def temp_account(create_temp_account):
    return create_temp_account()


def test_create_gallery_without_name_key_response_400(client, temp_account):

    rv = client.post(
        url,
        json={
            "gallery_id": "galleryid",
            "explain": "explain",
            "gallery_type": 2,
        },
        headers={"authorization": "Bearer " + temp_account.generate_access_token()},
    )

    assert rv.status_code == 400


def test_create_gallery_correct_expect_response_201(
    post_gallery, temp_admin_account
):
    rv = post_gallery(
        gallery_id="testgalleryid1",
        name="테스트 갤러리 이름1",
        explain="이 갤러리는 테스트 갤러리1입니다.",
        gallery_type=1,
        access_token=temp_admin_account.generate_access_token(),
    )

    assert rv.status_code == 201


def test_create_gallery_with_wrong_json_data_response_400(
    client, temp_admin_account
):

    test_gallery_has_overlenth_name = {
        "gallery_id": "testid",
        "name": "테" * 31,
        "explain": "this is explain of test_gallery.",
        "gallery_type": 1,
    }
    test_gallery_has_overlenth_explain = {
        "gallery_id": "testid2",
        "name": "overlenth_explain_gallery",
        "explain": "테" * 256,
        "gallery_type": 1,
    }

    rv = client.post(
        url,
        json=test_gallery_has_overlenth_name,
        headers={
            "authorization": "Bearer "
            + temp_admin_account.generate_access_token()
        },
    )

    rv2 = client.post(
        url,
        json=test_gallery_has_overlenth_explain,
        headers={
            "authorization": "Bearer "
            + temp_admin_account.generate_access_token()
        },
    )

    assert rv.status_code == 400
    assert rv2.status_code == 400


def test_create_gallery_with_not_suport_gallery_type_response_400(
    post_gallery, temp_admin_account
):
    rv = post_gallery(
        gallery_type=44,
        access_token=temp_admin_account.generate_access_token(),
    )

    assert rv.status_code == 400


def test_create_default_gallery_with_normal_user_response_403(
    post_gallery, temp_account
):
    rv = post_gallery(
        gallery_type=1, access_token=temp_account.generate_access_token()
    )
    assert rv.status_code == 403


@fixture
def temp_galleries(create_temp_gallery):
    temp_galleries = [
        create_temp_gallery(gallery_type=1) for i in range(10)
    ] + [create_temp_gallery(gallery_type=2) for i in range(10)]

    return temp_galleries


@fixture
def get_galleries(client):
    def get_galleries_(gallery_type=None):
        return client.get(url, query_string={"gallery-type": gallery_type})

    return get_galleries_


def test_get_all_gallery_list_correct(client, temp_galleries):
    rv = client.get(url)
    galleries_list = rv.json

    assert galleries_list
    assert len(galleries_list) == 20


def test_get_gallery_list_with_filter_type_response_200(
    client, temp_galleries, get_galleries
):
    rv = get_galleries(gallery_type=1)

    galleries = rv.json

    assert rv.status_code == 200
    assert galleries
    for gallery in galleries:
        assert gallery["gallery_type"] == 1

url = "/api/v1/board/galleries"


def test_create_gallery_correct(client, create_temp_account):
    admin_account = create_temp_account(is_admin=True)
    test_gallery_1 = {
        "id": "test",
        "name": "테스트",
        "explain": "테스트를 위한 갤러리1입니다.",
    }

    rv = client.post(
        url,
        json=test_gallery_1,
        headers={
            "authorization": "Bearer " + admin_account.generate_access_token()
        },
    )

    assert rv.status_code == 201


def test_create_gallery_with_wrong_json_data_response_400(client, create_temp_account):
    admin_account = create_temp_account(is_admin=True)
    test_gallery_has_overlenth_name = {
        "name": "테" * 31,
        "explain": "this is explain of test_gallery.",
    }
    test_gallery_has_overlenth_explain = {
        "name": "overlenth_explain_gallery",
        "explain": "테" * 256,
    }

    rv = client.post(
        url,
        json=test_gallery_has_overlenth_name,
        headers={
            "authorization": "Bearer " + admin_account.generate_access_token()
        },
    )

    rv2 = client.post(
        url,
        json=test_gallery_has_overlenth_explain,
        headers={
            "authorization": "Bearer " + admin_account.generate_access_token()
        },
    )

    assert rv.status_code == 400
    assert rv2.status_code == 400



def test_create_gallery_

def test_get_gallery_list_correct(client, create_temp_gallery):
    temp_galleries = [create_temp_gallery() for i in range(10)]

    rv = client.get(url)
    galleries_list = rv.json

    assert galleries_list
    for i in range(10):
        assert temp_galleries[i].name == galleries_list[i]["name"]
        assert temp_galleries[i].id == galleries_list[i]["id"]


def test_get_gallery_list_when_exist_any_gallery(client):
    rv = client.get(url)
    galleries_list = rv.json

    assert galleries_list == []

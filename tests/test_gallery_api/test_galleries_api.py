url = "/api/v1/board/galleries"

@fixture
def post_gallery(client):
    def post_gallery_(gallery_id, name, explain, gallery_type, access_token):
        return client.post(
            url,
            json={
                "gallery_id": gallery_id,
                "name": name,
                "explain": explain,
                "gallery_type": gallery_type,
            },
            header={
                "authorization": "Bearer " + access_token
            }
        )

    return post_gallery_
    
@fixture
def temp_admin_account(create_temp_account):
    return create_temp_account(is_admin=True)

def test_create_gallery_correct_expect_response_201(
        post_gallery,
        temp_admin_account
    ):
    rv = post_gallery(
        gallery_id= "testgalleryid1",
        name= "테스트 갤러리 이름1",
        explain= "이 갤러리는 테스트 갤러리1입니다.",
        gallery_type= 1,
        access_token= temp_account.generate_access_token()
    )

    assert rv.status_code == 201



# def test_create_gallery_correct(client, create_temp_account):
#     admin_account = create_temp_account(is_admin=True)
#     test_gallery_1 = {
#         "gallery_id": "testijbiubiud",
#         "name": "테스트",
#         "explain": "테스트를 위한 갤러리1입니다.",
#     }
#     rv = client.post(
#         url,
#         json=test_gallery_1,
#         headers={
#             "authorization": "Bearer " + admin_account.generate_access_token()
#         },
#     )
#     print(rv.json)


#     assert rv.status_code == 201


def test_create_gallery_with_wrong_json_data_response_400(
        post_gallery,
        temp_admin_account
    ):
    
    test_gallery_has_overlenth_name = {
        "gallery_id": "testid",
        "name": "테" * 31,
        "explain": "this is explain of test_gallery.",
        "gallery_type": 1
    }
    test_gallery_has_overlenth_explain = {
        "gallery_id": "testid2",
        "name": "overlenth_explain_gallery",
        "explain": "테" * 256,
        "gallery_type": 1
    }

    rv = client.post(
        url,
        json=test_gallery_has_overlenth_name,
        headers={
            "authorization": "Bearer " + temp_admin_account.generate_access_token()
        },
    )

    rv2 = client.post(
        url,
        json=test_gallery_has_overlenth_explain,
        headers={
            "authorization": "Bearer " + temp_admin_account.generate_access_token()
        },
    )

    assert rv.status_code == 400
    assert rv2.status_code == 400

def test_create_gallery_with_wrong_gallery_type_response_400(
        post_gallery,
        admin_account
    ):

    rv = post_gallery(
        gallery_id="testid2",
        name="overlenth_explain_gallery",
        explain="this is explain of test_gallery.",
        gallery_type=44,
        access_token=temp_admin_account.generate_access_token()
    )

    assert rv.status_code == 400

@fixture
def temp_galleries(create_temp_gallery):
    temp_galleries =\
        [create_temp_gallery(gallery_type=1) for i in range(10)] +\
        [create_temp_gallery(gallery_type=0) for i in range(10)]
    
    return temp_galleries

@fixture
def get_galleries(client, gallery_type=None):
    return client.get(
        url,
        querystring={
            "gallery_type": gallery_type 
        }
    ) 

def test_get_gallery_list_correct(client, temp_galleries):
    rv = client.get(url)
    galleries_list = rv.json

    assert galleries_list
    for i in range(10):
        assert temp_galleries[i].name == galleries_list[i]["name"]
        assert temp_galleries[i].gallery_id == galleries_list[i]["gallery_id"]


def test_get_gallery_list_with_filter_type(client, create_temp_gallery):
    rv = get_galleries(gallery_type=1)
    
    galleries = rv.json

    assert galleries
    assert galleries[0].gallery_type == 1
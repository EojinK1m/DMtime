from pytest import fixture

def create_postlike_uri(post_id):
    return f'api/v1/board/posts/{post_id}/like'

@fixture
def post_postlike(client):
    
    def _post_postlike(access_token, post_id):
        return client.post(
            create_postlike_uri(post_id),
            headers={"authorization": "Bearer " + access_token},
        )

    return _post_postlike

@fixture
def test_post(create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email, upload_gallery_id=temp_gallery.id
    )
    return temp_post

@fixture
def test_user(create_temp_account):
    user = create_temp_account()
    user.access_token = user.generate_access_token()

    return user

def test_post_postlike_succeess_response_201(
    post_postlike,
    test_post,
    test_user
    ):
    
    rv = post_postlike(
        test_user.access_token,
        test_post.id
    )

    assert rv.status_code == 201
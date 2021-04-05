from pytest import fixture

def create_postlike_uri(post_id):
    return f'api/v1/board/posts/{post_id}/like'

def create_postdislike_uri(post_id):
    return f'api/v1/board/posts/{post_id}/dislike'

@fixture
def post_postlike(client):
    def _post_postlike(access_token, post_id):
        return client.post(
            create_postlike_uri(post_id),
            headers={"authorization": "Bearer " + access_token},
        )

    return _post_postlike

@fixture
def postdislike(client):
    def _post_postdislike(access_token, post_id):
        return client.post(
            create_dislike_uri(post_id),
            headers={"authorization": "Bearer " + access_token}
        )
    
    return _post_postdislike

@fixture 
def delete_postlike(client):
    def _delete_postlike(access_token, post_id):
        return client.delete(
            create_postlike_uri(post_id),
            headers={"authorization": "Bearer " + access_token}
        )
    
    return _delete_postlike

@fixture
def delete_postdislike(client):
    def _delete_postdislike(access_token, post_id):
        return client.delete(
            create_postdislike_uri(post_id),
            headers={"authorization": "Bearer " + access_token}
        )

    return _delete_postdislike

@fixture
def temp_post(create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(
        uploader_id=temp_account.email, upload_gallery_id=temp_gallery.gallery_id
    )
    return temp_post

@fixture
def temp_user(create_temp_account):
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

def test_delete_postlike_when_like_is_not_exist_reponse_404(
    temp_post,
    temp_user
):
    pass

def test_post_postdislike_success_reponse_201(
    temp_post,
    temp_user
):
    pass

def test_post_postdislike_when_already_like_exist_response_409(
    temp_post,
    temp_user
):
    pass

def test_post_postdislike_when_already_postdislike_exist_response_409(
    temp_post,
    temp_user
):
    pass

def test_delete_postdislike_when_postdislike_is_not_exist_response_404(
    temp_post,
    temp_user
):
    pass

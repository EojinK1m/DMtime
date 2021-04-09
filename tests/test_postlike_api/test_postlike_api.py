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
def post_postdislike(client):
    def _post_postdislike(access_token, post_id):
        return client.post(
            create_postdislike_uri(post_id),
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


@fixture
def temp_postlike(create_temp_postlike, temp_post, temp_user):
    postlike = create_temp_postlike(
        liker_id=temp_user.email,
        post_id=temp_post.id
    )

    return {
        "postlike": postlike,
        "user": temp_user,
        "post": temp_post
    }

@fixture
def temp_postdislike(create_temp_postdislike, temp_post, temp_user):
    postdislike = create_temp_postdislike(
        liker_id=temp_user.email,
        post_id=temp_post.id
    )

    return {
        "postdislike": postdislike,
        "user": temp_user,
        "post": temp_post
    }


def test_post_postlike_succeess_response_201(
    post_postlike,
    temp_post,
    temp_user
):    
    rv = post_postlike(
        temp_user.generate_access_token(),
        temp_post.id
    )

    assert rv.status_code == 201


def test_post_postlike_when_already_postlike_exist_response_409(
    post_postlike,
    temp_postlike
):
    rv = post_postlike(
        access_token=temp_postlike['user'].generate_access_token(),
        post_id=temp_postlike['post'].id
    )
    
    assert rv.status_code == 409


def test_post_postlike_when_already_postdislike_exist_response_409(
    temp_postdislike,
    post_postlike
):
    rv = post_postlike(
        access_token=temp_postdislike['user'].generate_access_token(),
        post_id=temp_postdislike['post'].id
    )

    assert rv.status_code == 409

    
def test_delete_postlike_success_response_200(
    temp_postlike,
    delete_postlike
):
    rv = delete_postlike(
        temp_postlike['user'].generate_access_token(),
        temp_postlike['post'].id
    )

    assert rv.status_code == 200


def test_delete_postlike_when_postlike_is_not_exist_reponse_404(
    temp_post,
    temp_user,
    delete_postlike
):
    rv = delete_postlike(
        post_id=temp_post.id,
        access_token=temp_user.generate_access_token()
    )
    assert rv.status_code == 404

###TEST postdislike API


def test_post_postdislike_succeess_response_201(
    post_postdislike,
    temp_post,
    temp_user
):    
    rv = post_postdislike(
        access_token=temp_user.generate_access_token(),
        post_id=temp_post.id
    )

    assert rv.status_code == 201


def test_post_postdislike_when_already_postlike_exist_response_409(
    post_postdislike,
    temp_postlike
):
    rv = post_postdislike(
        access_token=temp_postlike['user'].generate_access_token(),
        post_id=temp_postlike['post'].id
    )
    
    assert rv.status_code == 409

def test_post_postdislike_when_already_postdislike_exist_response_409(
    temp_postdislike,
    post_postdislike
):
    rv = post_postdislike(
        access_token=temp_postdislike['user'].generate_access_token(),
        post_id=temp_postdislike['post'].id
    )

    assert rv.status_code == 409

    
def test_delete_postdislike_success_response_200(
    temp_postdislike,
    delete_postdislike
):
    rv = delete_postdislike(
        temp_postdislike['user'].generate_access_token(),
        temp_postdislike['post'].id
    )

    assert rv.status_code == 200


def test_delete_postdislike_when_postdislike_is_not_exist_reponse_404(
    temp_post,
    temp_user,
    delete_postdislike
):
    rv = delete_postdislike(
        post_id=temp_post.id,
        access_token=temp_user.generate_access_token()
    )
    assert rv.status_code == 404

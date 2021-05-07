from pytest import fixture


@fixture
def get_posts_request_user_wrote_comment(client):

    def get_posts_request_user_wrote_comment_(access_token):
        return client.get(
            f"/api/v1/me/posts-wrote-comment",
            headers={"authorization": "Bearer " + access_token}
        )

    return get_posts_request_user_wrote_comment_


@fixture
def temp_resources(
        create_temp_account,
        create_temp_gallery,
        create_temp_post,
        create_temp_comment
):

    temp_user = create_temp_account()
    temp_gallery = create_temp_gallery(manager_user=temp_user)
    temp_post = create_temp_post(
        uploader_id=temp_user.id,
        upload_gallery_id=temp_gallery.id
    )
    temp_comment = create_temp_comment(
        wrote_user_id=temp_user.email,
        wrote_post_id=temp_post.id
    )

    return {
        'user': temp_user,
        'gallery': temp_gallery,
        'post': temp_post,
        'access_token': temp_user.generate_access_token(),
        'comment': temp_comment
    }


def test_get_posts_request_user_wrote_comment_success_response_200(
        temp_resources,
        get_posts_request_user_wrote_comment,
        create_temp_post,
        create_temp_account
):
    another_temp_user = create_temp_account()
    create_temp_post(
        upload_gallery_id=temp_resources["gallery"].id,
        uploader_id=another_temp_user.email
    )

    rv = get_posts_request_user_wrote_comment(
        temp_resources['access_token']
    )

    assert rv.status_code == 200
    assert len(rv.json) == 1


def test_get_posts_request_user_wrote_comment_without_access_token_response_422(
        get_posts_request_user_wrote_comment,
        temp_resources
):
    rv = get_posts_request_user_wrote_comment(
        access_token=''
    )

    assert rv.status_code == 422

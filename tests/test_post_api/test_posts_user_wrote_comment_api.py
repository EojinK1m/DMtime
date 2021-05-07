from pytest import fixture


@fixture
def get_user_wrote_comment_posts(client):

    def get_user_wrote_comment_posts_(username):
        return client.get(
            f"/api/v1/users/{username}/posts-wrote-comment"
        )

    return get_user_wrote_comment_posts_


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


def test_get_user_wrote_comment_posts_success_response_200(
        temp_resources,
        get_user_wrote_comment_posts,
        create_temp_post,
        create_temp_account
):
    another_temp_user = create_temp_account()
    create_temp_post(
        upload_gallery_id=temp_resources["gallery"].id,
        uploader_id=another_temp_user.email
    )

    rv = get_user_wrote_comment_posts(
        temp_resources['user'].username
    )

    assert rv.status_code == 200
    assert len(rv.json) == 1


def test_get_user_wrote_comment_posts_with_not_exists_username_response_404(
        get_user_wrote_comment_posts,
        temp_resources
):
    rv = get_user_wrote_comment_posts(
        username='없는 유저네임'
    )

    assert rv.status_code == 404
from pytest import fixture


@fixture
def get_user_liked_posts(client):

    def get_user_liked_posts_(username):
        return client.get(
            f"/api/v1/users/{username}/liked-posts"
        )

    return get_user_liked_posts_


@fixture
def temp_resources(
        create_temp_account,
        create_temp_gallery,
        create_temp_post,
        create_temp_postlike
):

    temp_user = create_temp_account()
    temp_gallery = create_temp_gallery(manager_user=temp_user)
    temp_post = create_temp_post(
        uploader_id=temp_user.id,
        upload_gallery_id=temp_gallery.id
    )
    temp_postlike = create_temp_postlike(
        post_id=temp_post.id,
        liker_id=temp_user.email
    )

    return {
        'user': temp_user,
        'gallery': temp_gallery,
        'post': temp_post,
        'access_token': temp_user.generate_access_token()
    }


def test_get_user_liked_posts_success_response_200(
        temp_resources,
        get_user_liked_posts,
        create_temp_post,
        create_temp_account
):
    another_temp_user = create_temp_account()
    create_temp_post(
        upload_gallery_id=temp_resources["gallery"].id,
        uploader_id=another_temp_user.email
    )

    rv = get_user_liked_posts(
        temp_resources['user'].username
    )

    assert rv.status_code == 200
    assert len(rv.json["posts"]) == 1


def test_get_user_liked_posts_with_not_exists_username_response_404(
        get_user_liked_posts,
        temp_resources
):
    rv = get_user_liked_posts(
        username='없는 유저네임'
    )

    assert rv.status_code == 404
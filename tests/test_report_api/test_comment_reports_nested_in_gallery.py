from pytest import fixture


url = "/api/v1/board/galleries/"


@fixture
def temp_resources(
        create_temp_comment_report,
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
        wrote_post_id=temp_post.id,
    )

    return {
        'report': create_temp_comment_report(user=temp_user, comment=temp_comment),
        'user': temp_user,
        'gallery': temp_gallery,
        'post': temp_post,
        'comment': temp_comment,
        'access_token': temp_user.generate_access_token()
    }


@fixture
def get_comment_reports_nested_in_gallery(client):
    def get_comment_reports_nested_in_gallery_(gallery_id, access_token):
        return client.get(
            url + f"{gallery_id}/comment-reports",
            headers={"authorization": "Bearer " + access_token}
        )

    return get_comment_reports_nested_in_gallery_


def test_get_comment_reports_nested_in_gallery_success(
        get_comment_reports_nested_in_gallery,
        temp_resources
):
    rv = get_comment_reports_nested_in_gallery(
        gallery_id=temp_resources['gallery'].id,
        access_token=temp_resources['access_token']
    )
    from pprint import pprint
    pprint(rv.json)
    assert rv.status_code == 200


def test_get_comment_reports_of_gallery_with_not_exist_gallery_id_response_404(
        get_comment_reports_nested_in_gallery,
        temp_resources
):
    rv = get_comment_reports_nested_in_gallery(
        gallery_id="notexistGallery",
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 404


def test_get_comment_reports_of_gallery_without_permission_response_403(
        get_comment_reports_nested_in_gallery,
        temp_resources,
        create_temp_account
):
    admin_user = create_temp_account()

    rv = get_comment_reports_nested_in_gallery(
        gallery_id=temp_resources['gallery'].id,
        access_token=admin_user.generate_access_token()
    )

    assert rv.status_code == 403

from pytest import fixture


url = "/api/v1/comment-reports"


@fixture
def get_comment_report(client):
    def get_comment_report_(report_id, access_token):
        return client.get(
            url + f'/{report_id}',
            headers={"authorization": "Bearer " + access_token},
        )

    return get_comment_report_


@fixture
def delete_comment_report(client):
    def delete_comment_report_(report_id, access_token):
        return client.delete(
            url + f'/{report_id}',
            headers={"authorization": "Bearer " + access_token},
        )

    return delete_comment_report_


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


def test_get_comment_report_success_response_200(get_comment_report, temp_resources):
    rv = get_comment_report(
        report_id=temp_resources['report'].id,
        access_token=temp_resources['user'].generate_access_token()
    )

    assert rv.status_code == 200


def test_get_comment_report_by_admin_response_200(get_comment_report, temp_resources, create_temp_account):
    admin_user = create_temp_account(is_admin=True)

    rv = get_comment_report(
        report_id=temp_resources['report'].id,
        access_token=admin_user.generate_access_token()
    )

    assert rv.status_code == 200


def test_get_comment_report_not_exist_response_404(get_comment_report, temp_resources):
    rv = get_comment_report(
        report_id=3434,
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 404


def test_get_comment_report_by_without_permission_403(get_comment_report, temp_resources, create_temp_account):
    temp_user = create_temp_account()

    rv = get_comment_report(
        report_id=temp_resources['report'].id,
        access_token=temp_user.generate_access_token()
    )

    assert rv.status_code == 403


def test_delete_comment_report_success_200(delete_comment_report, temp_resources):
    rv = delete_comment_report(
        report_id=temp_resources['report'].id,
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 200


def test_delete_comment_report_with_admin_response_200(delete_comment_report, temp_resources, create_temp_account):
    admin = create_temp_account(is_admin=True)

    rv = delete_comment_report(
        report_id=temp_resources['report'].id,
        access_token=admin.generate_access_token()
    )

    assert rv.status_code == 200


def test_delete_comment_report_without_permission_response_403(delete_comment_report, temp_resources, create_temp_account):
    temp_user = create_temp_account()

    rv = delete_comment_report(
        report_id=temp_resources['report'].id,
        access_token=temp_user.generate_access_token()
    )

    assert rv.status_code == 403


def test_delete_comment_report_not_exist_response_404(delete_comment_report, temp_resources):
    rv = delete_comment_report(
        report_id=3434,
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 404

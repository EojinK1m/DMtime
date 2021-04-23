from pytest import fixture

url = "/api/v1/post-reports/"


@fixture
def get_post_report(client):
    def get_post_report_(report_id, access_token):
        return client.get(
            url + f'/{report_id}',
            headers={"authorization": "Bearer " + access_token},
        )

    return get_post_report_


@fixture
def delete_post_report(client):
    def delete_post_report_(report_id, access_token):
        return client.delete(
            url + f'/{report_id}',
            headers={"authorization": "Bearer " + access_token},
        )

    return delete_post_report_


@fixture
def temp_resources(
        create_temp_post_report,
        create_temp_account,
        create_temp_gallery,
        create_temp_post
):
    temp_user = create_temp_account()
    temp_gallery = create_temp_gallery(manager_user=temp_user)
    temp_post = create_temp_post(
        uploader_id=temp_user.id,
        upload_gallery_id=temp_gallery.id
    )

    return {
        'report': create_temp_post_report(user=temp_user, post=temp_post),
        'user': temp_user,
        'gallery': temp_gallery,
        'post': temp_post,
        'access_token': temp_user.generate_access_token()
    }


def test_get_post_report_success_response_200(get_post_report, temp_resources):
    rv = get_post_report(
        report_id=temp_resources['report'],
        access_token=temp_resources['user'].generate_access_token()
    )

    assert rv.status_code == 200


def test_get_post_report_by_admin_success(get_post_report, temp_resources, create_temp_account):
    admin_user = create_temp_account(is_admin=True)

    rv = get_post_report(
        report_id=temp_resources['report'],
        access_token=admin_user.generate_access_token()
    )

    assert rv.status_code == 200


def test_get_post_report_not_exist_response_404(get_post_report, temp_resources):
    rv = get_post_report(
        report_id=3434,
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 404


def test_get_post_report_by_without_permission_403(get_post_report, temp_resources, create_temp_account):
    temp_user = create_temp_account()

    rv = get_post_report(
        report_id=temp_resources['report'].id,
        access_token=temp_user.generate_access_token()
    )

    assert rv.status_code == 403


def test_delete_post_report_success(delete_post_report, temp_resources):
    rv = delete_post_report(
        report_id=temp_resources['report'].id,
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 200


def test_delete_post_report_with_admin_success(delete_post_report, temp_resources, create_temp_account):
    admin = create_temp_account(is_admin=True)

    rv = delete_post_report(
        report_id=temp_resources['report'].id,
        access_token=admin.generate_access_token()
    )

    assert rv.status_code == 200


def test_delete_post_report_without_permission_response_403(delete_post_report, temp_resources, create_temp_account):
    temp_user = create_temp_account()

    rv = delete_post_report(
        report_id=temp_resources['report'].id,
        access_token=temp_user.generate_access_token()
    )

    assert rv.status_code == 403


def test_delete_post_report_not_exist_response_404(delete_post_report, temp_resources):
    rv = delete_post_report(
        report_id=3434,
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 404

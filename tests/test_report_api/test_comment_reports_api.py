from pytest import fixture

url = "/api/v1/comment-reports/"


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
def post_comment_report(client):
    def post_comment_report_(comment_id, access_token, reason, detail_reason):
        return client.post(
            url,
            json={
                "comment_id":comment_id,
                "reason":reason,
                "detail_reason":detail_reason
            },
            headers={"authorization": "Bearer " + access_token}
        )

    return post_comment_report_


@fixture
def get_comment_reports(client):
    def get_comment_reports_(access_token):
        return client.get(
            url,
            headers={"authorization": "Bearer " + access_token}
        )

    return get_comment_reports_


@fixture
def get_comment_reports_included_in_gallery(client):
    def get_comment_reports_included_in_gallery_(access_token,gallery_id):
        return client.get(
            f'/api/v1/board/galleries/{gallery_id}/comment_reports',
            headers={"authorization": "Bearer " + access_token}
        )

    return get_comment_reports_included_in_gallery_


def test_post_comment_report_success_response_201(post_comment_report, temp_resources):
    rv = post_comment_report(
        comment_id=temp_resources['comment'].id,
        access_token=temp_resources['access_token'],
        reason=1,
        detail_reason='응애 쟤가 나쁜말 해요ㅠ'
    )

    assert rv.status_code == 201


def test_post_comment_report_with_not_supported_reason_response_400(post_comment_report, temp_resources):
    rv = post_comment_report(
        comment_id=temp_resources['comment'].id,
        access_token=temp_resources['access_token'],
        reason=132,
        detail_reason='응애 쟤가 나쁜말 해요ㅠ'
    )

    assert rv.status_code == 400


def test_post_comment_report_with_not_exist_post_id_response_404(post_comment_report, temp_resources):
    rv = post_comment_report(
        comment_id=3333,
        access_token=temp_resources['access_token'],
        reason=1,
        detail_reason='응애 쟤가 나쁜말 해요ㅠ'
    )

    assert rv.status_code == 404


def test_get_all_comment_reports_by_admin_success(get_comment_reports, temp_resources, create_temp_account):
    admin_user = create_temp_account(is_admin=True)

    rv = get_comment_reports(admin_user.generate_access_token())

    assert rv.status_code == 200


def test_get_all_comment_reports_by_not_admin_user_response_403(get_comment_reports, temp_resources):
    rv = get_comment_reports(temp_resources['access_token'])

    assert rv.status_code == 403


def test_get_comment_reports_of_gallery_by_manager_success(get_comment_reports_included_in_gallery, temp_resources):
    rv = get_comment_reports_included_in_gallery(
        gallery_id=temp_resources['gallery'],
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 200


def test_get_comment_reports_of_gallery_by_admin_success(
        get_comment_reports_included_in_gallery,
        temp_resources,
        create_temp_account
):
    admin_user = create_temp_account(is_admin=True)

    rv = get_comment_reports_included_in_gallery(
        gallery_id=temp_resources['gallery'],
        access_token=admin_user.generate_access_token()
    )

    assert rv.status_code == 200


def test_get_comment_reports_of_gallery_with_not_exist_gallery_id_response_404(
        get_comment_reports_included_in_gallery,
        temp_resources
):
    rv = get_comment_reports_included_in_gallery(
        gallery_id="notexistGallery",
        access_token=temp_resources['access_token']
    )

    assert rv.status_code == 404


def test_get_comment_reports_of_gallery_without_permission_response_403(
        get_comment_reports_included_in_gallery,
        temp_resources,
        create_temp_account
):
    admin_user = create_temp_account()

    rv = get_comment_reports_included_in_gallery(
        gallery_id=temp_resources['gallery'],
        access_token=admin_user.generate_access_token()
    )

    assert rv.status_code == 403
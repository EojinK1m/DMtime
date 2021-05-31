from pytest import fixture


@fixture
def default_ready(
    create_temp_account,
    create_temp_gallery,
    create_temp_comment,
    create_temp_post,
    create_temp_report,
):
    from app.api.v1.gallery.report.model import Reason, ContentType

    class DefaultReady:
        def __init__(self):
            self.temp_non_manager_account = create_temp_account()
            self.temp_account = create_temp_account()
            self.temp_gallery = create_temp_gallery(
                manager_user=self.temp_account
            )
            self.temp_post = create_temp_post(
                self.temp_account.email, self.temp_gallery.gallery_id
            )
            self.temp_comment = create_temp_comment(
                self.temp_account.email, self.temp_post.id
            )
            self.temp_post_report = create_temp_report(
                self.temp_account.email,
                self.temp_gallery.gallery_id,
                ContentType.POST.value,
                post_id=self.temp_post.id,
            )
            self.temp_comment_report = create_temp_report(
                self.temp_account.email,
                self.temp_gallery.gallery_id,
                ContentType.COMMENT.value,
                comment_id=self.temp_comment.id,
            )
            self.auth_header = {
                "authorization": "Bearer "
                + self.temp_account.generate_access_token()
            }
            self.non_manager_auth_header = {
                "authorization": "Bearer "
                + self.temp_non_manager_account.generate_access_token()
            }
            self.url = f"api/v1/board/galleries/{self.temp_gallery.gallery_id}/reports"
            self.comment_report_uri = (
                self.url + f"/{self.temp_comment_report.id}"
            )
            self.post_report_uri = self.url + f"/{self.temp_post_report.id}"

            self.default_comment_report_json = {
                "reason": Reason.PRONOGRAPHY.value,
                "detail_reason": "This is default detail reason for test",
                "reported_content_type": ContentType.COMMENT.value,
                "post_id": None,
                "comment_id": self.temp_comment.id,
            }
            self.default_post_report_json = {
                "reason": Reason.PRONOGRAPHY.value,
                "detail_reason": "This is default detail reason for test",
                "reported_content_type": ContentType.POST.value,
                "post_id": self.temp_post.id,
                "comment_id": None,
            }

    return DefaultReady()


def test_get_post_report(client, default_ready):
    rv = client.get(
        default_ready.post_report_uri, headers=default_ready.auth_header
    )

    assert rv.status_code == 200
    assert rv.json
    assert rv.json["reported_post"]


def test_get_comment_report(client, default_ready):
    rv = client.get(
        default_ready.comment_report_uri, headers=default_ready.auth_header
    )

    assert rv.status_code == 200
    assert rv.json
    assert rv.json["reported_comment"]


def test_get_report_with_non_manager_account(client, default_ready):
    rv = client.get(
        default_ready.post_report_uri,
        headers=default_ready.non_manager_auth_header,
    )

    assert rv.status_code == 403


def test_get_not_exist_report(client, default_ready):
    rv = client.get(
        default_ready.post_report_uri + "1", headers=default_ready.auth_header
    )

    assert rv.status_code == 404


def test_delete_report(client, default_ready):
    rv = client.delete(
        default_ready.post_report_uri, headers=default_ready.auth_header
    )

    assert rv.status_code == 200


def test_delete_report_with_non_manager_account(client, default_ready):
    comment_report_rv = client.delete(
        default_ready.comment_report_uri,
        headers=default_ready.non_manager_auth_header,
    )

    post_report_rv = client.delete(
        default_ready.post_report_uri,
        headers=default_ready.non_manager_auth_header,
    )

    assert comment_report_rv.status_code == 403
    assert post_report_rv.status_code == 403

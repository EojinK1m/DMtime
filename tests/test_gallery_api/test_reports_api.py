from pytest import fixture

@fixture
def default_ready(
    create_temp_account,
    create_temp_gallery,
    create_temp_comment,
    create_temp_post,
    create_temp_report
    ):
    from app.api.v1.board.gallery.report.model import Reason, ContentType

    class DefaultReady:
        def __init__(self):
            self.temp_non_manager_account = create_temp_account()
            self.temp_account = create_temp_account()
            self.temp_gallery = create_temp_gallery(manager_user=self.temp_account)
            self.temp_post = create_temp_post(self.temp_account.user.id, self.temp_gallery.id)
            self.temp_comment = create_temp_comment(self.temp_account.user.id, self.temp_post.id)
            self.temp_post_report = create_temp_report(
                self.temp_account.user.id,
                self.temp_gallery.id,
                ContentType.POST.value,
                post_id=self.temp_post.id
                )
            self.temp_comment_report = create_temp_report(
                self.temp_account.user.id,
                self.temp_gallery.id,
                ContentType.COMMENT.value,
                comment_id=self.temp_comment.id
            )
            self.auth_header = {'authorization':'Bearer '+self.temp_account.generate_access_token()}
            self.non_manager_auth_header = {'authorization':'Bearer '+self.temp_non_manager_account.generate_access_token()}
            self.url = f'api/v1/board/galleries/{self.temp_gallery.id}/reports'

            self.default_comment_report_json = {
                'reason':Reason.PRONOGRAPHY.value,
                'detail_reason':'This is default detail reason for test',
                'reported_content_type':ContentType.COMMENT.value,
                'comment_id':self.temp_comment.id,
            }
            self.default_post_report_json = {
                'reason':Reason.PRONOGRAPHY.value,
                'detail_reason':'This is default detail reason for test',
                'reported_content_type':ContentType.POST.value,
                'post_id':self.temp_post.id,
            }

    return DefaultReady()


#CREATE TEST


def test_create_comment_report(client, default_ready):
    rv = client.post(
        default_ready.url,
        json=default_ready.default_comment_report_json,
        headers=default_ready.auth_header
    )
    assert rv.status_code == 201


def test_create_post_report(client, default_ready):
    rv = client.post(
        default_ready.url,
        json=default_ready.default_post_report_json,
        headers=default_ready.auth_header
    )

    assert rv.status_code == 201


def test_create_post_report(client, default_ready):
    default_ready.default_comment_report_json['post_id'] = default_ready.temp_post.id

    rv = client.post(
        default_ready.url,
        json=default_ready.default_comment_report_json,
        headers=default_ready.auth_header
    )

    assert rv.status_code == 400

#GET TEST


def test_get_report_list(client, default_ready):
    rv = client.get(
        default_ready.url,
        headers=default_ready.auth_header
    )

    assert rv.status_code == 200
    assert isinstance(rv.json, list)


def test_get_report_list_with_non_manager_account(client, default_ready):
    rv = client.get(
        default_ready.url,
        headers=default_ready.non_manager_auth_header
    )

    assert rv.status_code == 403

from pytest import fixture

from app.api.v1.user.service import UserService

@fixture
def test_registration(create_temp_register_account):
    return create_temp_register_account()

def post_email_verification_code(client, code):
    param = f'?verification-code={code}' if code else ''

    return client.post(
        '/api/v1/email-verification-code' + param
    )

def test_email_verify_success_response_200_and_create_user(client, test_registration):
    rv = post_email_verification_code(client, test_registration['verification_code'])

    assert rv.status_code == 200
    assert UserService.get_user_by_username_or_none(test_registration['user'].username) is not None

def test_post_verification_code_without_parameter_response_400(client):
    rv = post_email_verification_code(client, None)

    assert rv.status_code == 400

def test_post_not_exist_email_verification_code_response_404(client):
    rv = post_email_verification_code(client, 'eeeeeee')

    assert rv.status_code == 404
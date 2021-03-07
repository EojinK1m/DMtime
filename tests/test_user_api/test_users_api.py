from pytest import fixture

url = '/api/v1/users'

@fixture
def default_ready():
    class DefaultReady:
        def __init__(self):
            self.uri = '/api/v1/users'
            self.correct_register_json = {
                'email':'testemail123@dsm.hs.kr',
                'password':'',
                'username':'회원가입test123'
            }

    return DefaultReady


def test_users_post_correctly_response_200(client, default_ready):
    rv = client.post(
        default_ready.uri,
        json=default_ready.correct_register_json
    )

    assert rv.status == 200




pass

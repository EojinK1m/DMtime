from pytest import fixture

url = "/api/v1/users"


@fixture
def default_ready():
    class DefaultReady:
        def __init__(self):
            self.uri = "/api/v1/users"
            self.correct_register_json = {
                "email": "testemail123@dsm.hs.kr",
                "password": "testpassword123",
                "username": "회원가입test123",
            }

    return DefaultReady()


def register(client, user_info):
    return client.post(
        url,
        json={
            "username": user_info["username"],
            "email": user_info["email"],
            "password": user_info["password"],
        },
    )


def test_register_correctly_response_201(client, default_ready):
    rv = register(client, default_ready.correct_register_json)

    assert rv.status_code == 201


def test_register_with_already_using_username_response_409(
    client, default_ready, create_temp_account
):
    temp_account = create_temp_account()
    same_username_account = default_ready.correct_register_json.copy()
    same_username_account["username"] = temp_account.username

    rv = register(client, same_username_account)

    assert rv.status_code == 409


def test_register_with_wrong_username_response_400(client, default_ready):
    # overlength username
    wrong_account_1 = default_ready.correct_register_json.copy()
    wrong_account_1["username"] += "x" * 30

    overlength_username_rv = register(client, wrong_account_1)
    assert overlength_username_rv.status_code == 400


def test_register_with_forbidden_character_username_response_400(
    client, default_ready
):
    wrong_username_account = default_ready.correct_register_json.copy()
    wrong_username_account["username"] += "?"

    forbidden_character_rv = register(client, wrong_username_account)

    assert forbidden_character_rv.status_code == 400


def test_register_with_non_email_response_400(client, default_ready):
    wrong_account_1 = default_ready.correct_register_json.copy()
    wrong_account_1["email"] = "@" * 30

    rv = register(client, wrong_account_1)

    assert rv.status_code == 400


def test_register_with_already_using_email_response_409(
    client, default_ready, create_temp_account
):
    temp_account = create_temp_account()
    using_email_account = default_ready.correct_register_json.copy()
    using_email_account["email"] = temp_account.email

    rv = register(client, using_email_account)

    assert rv.status_code == 409


def test_register_with_non_school_email_response_400(client, default_ready):
    wrong_email_account = default_ready.correct_register_json.copy()
    wrong_email_account["email"] = "vjslzhs6@naver.com"

    rv = register(client, wrong_email_account)

    assert rv.status_code == 400


def test_register_with_belowlength_password_response_400(
    client, default_ready
):
    wrong_password_account = default_ready.correct_register_json.copy()
    wrong_password_account["password"] = "x1"

    rv = register(client, wrong_password_account)

    assert rv.status_code == 400


def test_register_with_overlength_password_response_400(client, default_ready):
    wrong_password_account = default_ready.correct_register_json.copy()
    wrong_password_account["password"] = "q1" * 19

    rv = register(client, wrong_password_account)

    assert rv.status_code == 400


def test_register_with_forbidden_character_password_response_400(
    client, default_ready
):
    wrong_password_account = default_ready.correct_register_json.copy()
    wrong_password_account["password"] = "잉기모링123k3\\"

    rv = register(client, wrong_password_account)

    assert rv.status_code == 400

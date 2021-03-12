from pytest import fixture

email_duplication_url = '/api/v1/users/email-duplication'
username_duplication_url = '/api/v1/users/username-duplication'


@fixture
def test_user(create_temp_account):
    return create_temp_account()


def check_email_duplication(client, email):
    return client.get(email_duplication_url + '?email=' + email)


def test_not_using_email_duplication_check_response_200_and_usable_true(client):
    rv = check_email_duplication(client, 'not-using-email@dsm.hs.kr')

    print(rv.json)
    assert rv.status_code == 200
    assert rv.json['usable'] == True


def test_check_already_using_email_duplication_response_200_and_usable_false(client, test_user):
    rv = check_email_duplication(client, test_user.email)

    assert rv.status_code == 200
    assert rv.json['usable'] == False


def test_email_duplicate_check_without_email_parameter_response_400(client):
    rv = client.get(email_duplication_url)

    assert rv.status_code == 400


def check_username_duplication(client, username):
    return client.get(username_duplication_url + '?username=' + username)


def test_check_not_using_username_duplicate_response_200_and_usable_true(client):
    rv = check_username_duplication(client, 'notusername')

    assert rv.status_code == 200
    assert rv.json['usable'] == True


def test_check_using_username_duplicate_response_200_and_usable_false(client, test_user):
    rv = check_username_duplication(client, test_user.username)

    assert rv.status_code == 200
    assert rv.json['usable'] == False


def test_email_duplicate_check_without_username_parameter(client):
    rv = client.get(username_duplication_url)

    assert rv.status_code == 400

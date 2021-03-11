from pytest import fixture

email_duplication_url = '/api/v1/users/email-duplication'
username_duplication_url = '/api/v1/users/username-duplcation'

@fixture
def test_user(create_temp_account):
    return create_temp_account()

def check_email_duplication(client, email):
    return client.get(email_duplication_url+'email?email='+email)


def test_not_using_email_duplication_check_response_200_and_usable_true(client):
    rv = check_email_duplication(client, 'not_using_email')

    assert rv.status_code == 200
    assert rv.json['usable'] == True

def test_check_already_using_email_duplicaion_response_200_and_usable_false(client, test_user):
    rv = check_email_duplication(client, test_user.email)

    assert rv.status_code == 200
    assert rv.json['usable'] == False

def test_email_duplicate_check_without_email_parameter_response_400(client):
    rv = client.get(email_duplication_url+'email')

    assert rv.status_code == 400


def check_username_duplication(client, username):
    return client.get(email_duplication_url+'username?username='+username)

def test_check_not_using_username_duplicate_response_200_and_usable_true(client):
    rv = check_username_duplication(client, 'not_exist_username')

    assert rv.status_code == 200
    assert rv.json['usable'] == True

def test_check_using_username_duplicate_response_200_and_usable_false(client, test_user):
    rv = check_username_duplication(client, test_user)

    assert rv.status_code == 200
    assert rv.json['usable'] == False

def test_email_duplicate_check_without_username_parameter(client):
    rv = client.get(username_duplication_url+'username')

    assert rv.status_code == 400



url = '/api/user/account/duplicate-check/'

def check_email(client, email):
    return client.get(url+'email?email='+email)

def test_not_exist_email_duplicate_check(client):
    rv = check_email(client, 'not_exist_email')

    assert rv.status_code == 200
    assert rv.json['usable'] == True

def test_exist_email_duplicate_check(client, create_temp_account):
    temp_account = create_temp_account()
    rv = check_email(client, temp_account.email)

    assert rv.status_code == 200
    assert rv.json['usable'] == False

def test_email_duplicate_check_without_email_parameter(client):
    rv = client.get(url+'email')

    assert rv.status_code == 400
    assert 'miss' in rv.json['msg']


def check_username(client, username):
    return client.get(url+'username?username='+username)

def test_not_exist_username_duplicate_check(client):
    rv = check_username(client, 'not_exist_username')

    assert rv.status_code == 200
    assert rv.json['usable'] == True

def test_exist_username_duplicate_check(client, create_temp_account):
    temp_account = create_temp_account()
    rv = check_username(client, temp_account.user.username)

    assert rv.status_code == 200
    assert rv.json['usable'] == False

def test_email_duplicate_check_without_username_parameter(client):
    rv = client.get(url+'username')

    assert rv.status_code == 400
    assert 'miss' in rv.json['msg']


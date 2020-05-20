url = '/api/user/account/auth'

def login(client, login_data):
    return client.post(url, json=login_data)


def test_login_with_correct_data(client, create_temp_account):
    temp_account = create_temp_account()
    rv = login(client, login_data={'email':temp_account.email,
                                   'password':temp_account.user.username.replace('user', 'password')})
    assert rv.status_code == 200
    assert 'refresh_token' in rv.json
    assert 'access_token' in rv.json

def test_login_with_not_exist_account_data(client):
    rv = login(client, login_data={'email':'not_email@email.com',
                                   'password':'kissing_strangers'})
    assert rv.status_code == 401

def test_login_without_password(client, create_temp_account):
    temp_account = create_temp_account()
    rv = login(client, login_data={'email':temp_account.email})

    assert rv.status_code == 400

def test_login2exist_account_with_wrong_password(client, create_temp_account):
    temp_account = create_temp_account()
    rv = login(client, login_data={'email':temp_account.email,
                                   'password':'wrong_password_123'})

    assert rv.status_code == 401

def refresh(client, refresh_token):
    return client.post(url+'/refresh', headers={'authorization':'bearer '+refresh_token})

def test_token_refresh(client, create_temp_account):
    temp_account = create_temp_account()
    refresh_token = temp_account.generate_refresh_token()
    rv = refresh(client, refresh_token)

    assert rv.status_code == 200
    assert rv.json['access_token']

def test_token_refresh_with_expired_refresh_token(client, create_temp_account):
    import datetime

    temp_account = create_temp_account()
    refresh_token = temp_account.generate_refresh_token(expire=datetime.timedelta(0))
    rv = refresh(client, refresh_token)

    assert rv.status_code == 401

url = '/api/user'


def test_get_user_information(client, create_temp_account):
    temp_account = create_temp_account()

    rv = client.get(url+'/'+temp_account.user.username)

    assert rv.status_code == 200
    user_info = rv.json['user_info']
    assert user_info
    assert user_info['username'] == temp_account.user.username
    assert user_info['explain'] == temp_account.user.explain


def test_patch_user_information(client, create_temp_account):
    temp_account = create_temp_account()
    change_username = temp_account.user.username + 'c'

    rv = client.patch(url+'/'+temp_account.user.username,
                      headers={'authorization':'Bearer '+temp_account.generate_access_token()},
                      json={'username':change_username})

    assert rv.status_code == 200
    assert temp_account.user.username == change_username

def test_patch_user_information_with_wrong_data(client, create_temp_account):
    temp_account = create_temp_account()

    rv = client.patch(url+'/'+temp_account.user.username,
                      headers={'authorization':'Bearer '+temp_account.generate_access_token()},
                      json={'wrong_key':'wrong_value'})

    assert rv.status_code == 402


def test_patch_user_information_without_access_token(client, create_temp_account):
    temp_account = create_temp_account()

    rv = client.patch(url+'/'+temp_account.user.username, json={'wrong_key':'wrong_value'})

    assert rv.status_code == 401

def test_patch_other_user_information(client, create_temp_account):
    temp_account, temp_account_2 = create_temp_account(), create_temp_account()

    change_username = temp_account.user.username + 'c'

    rv = client.patch(url+'/'+temp_account.user.username,
                      headers={'authorization':'Bearer '+temp_account_2.generate_access_token()},
                      json={'username':change_username})

    assert rv.status_code == 403

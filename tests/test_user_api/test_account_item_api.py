account_uri = '/api/v1/users/accounts'


def delete_account(client, email, jwt = ''):
    return client.delete(account_uri+'?email='+email,
                       headers={'authorization':'Bearer '+jwt})


def test_account_delete(client, create_temp_account):
    temp_account = create_temp_account()
    rv = delete_account(client, temp_account.email, jwt=temp_account.generate_access_token())
    assert rv.status_code == 200

def test_account_delete_without_jwt_request_return_422(client, create_temp_account):
    temp_account = create_temp_account()
    rv = delete_account(client, temp_account.email)
    assert rv.status_code == 422

def test_get_user_information(client, create_temp_account):
    temp_account = create_temp_account()
    rv = client.get(account_uri,
                    headers={'authorization':f'Bearer {temp_account.generate_access_token()}'})
    assert rv.status_code == 200
    account_info = rv.json['account_info']
    assert account_info
    assert account_info['email'] == temp_account.email

def test_put_account_password(client, create_temp_account):
    temp_account = create_temp_account()
    password = temp_account.user.username.replace('user', 'password')
    new_password = 'this_1s_new_passsword!'

    rv = client.put(account_uri+'/password',
                    json={
                        'password':password,
                        'new_password':new_password
                        },
                    headers={'authorization':f'Bearer {temp_account.generate_access_token()}'})
    
    assert rv.status_code == 200
    assert temp_account.verify_password(new_password)


def test_put_account_incorrect_password(client, create_temp_account):
    temp_account = create_temp_account()
    password = temp_account.user.username.replace('user', 'password')
    new_password = 'this_1s_new_passsword!'

    rv = client.put(account_uri + '/password',
                    json={
                        'password': password+'1',
                        'new_password': new_password
                    },
                    headers={'authorization': f'Bearer {temp_account.generate_access_token()}'})

    assert rv.status_code == 403

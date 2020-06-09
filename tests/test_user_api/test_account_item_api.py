account_uri = '/api/users/accounts'


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

def test_get_account_information(client, create_temp_account):
    temp_account = create_temp_account()
    rv = client.get(account_uri,
                    headers={'authorization':f'Bearer {temp_account.generate_access_token()}'})
    assert rv.status_code == 200
    account_info = rv.json['account_info']
    assert account_info
    assert account_info['email'] == temp_account.email

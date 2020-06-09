account_uri = '/api/users/accounts'

def register(client, new_account):
    return client.post(account_uri, json=new_account)

correct_account_1 = {'username':'test1',
                     'email':'test1@naver.com',
                     'password':'pass1234'}


def test_register_correct_minimum_information(client):
    rv = register(client, correct_account_1)
    assert rv.status_code == 200

def test_register_correct_full_information(client):
    full_information_account = correct_account_1.copy()
    rv = register(client, full_information_account)
    assert rv.status_code == 200


def test_register_same_username(client):
    rv = register(client, correct_account_1)
    assert rv.status_code == 200

    same_username_account = correct_account_1.copy()
    same_username_account['email'] += 'xxxx'
    rv_2 = register(client, correct_account_1)
    assert rv_2.status_code == 400


def test_register_same_email(client):
    rv = register(client, correct_account_1)
    assert rv.status_code == 200

    same_username_account = correct_account_1.copy()
    same_username_account['username'] += 'xxxx'
    rv_2 = register(client, correct_account_1)
    assert rv_2.status_code == 400


def test_register_wrong_username(client):
    #overlenth
    wrong_account_1 = correct_account_1.copy()
    wrong_account_1['username'] += 'x'*30

    rv = register(client, wrong_account_1)
    assert rv.status_code == 400

    #forbidden character
    wrong_account_2 = correct_account_1.copy()
    wrong_account_2['username'] += '?'

    rv2 = register(client, wrong_account_2)
    assert rv2.status_code == 200


def test_register_wrong_email(client):
    wrong_account_1 = correct_account_1.copy()
    wrong_account_1['email'] = 'x'*30
    rv = register(client, wrong_account_1)
    assert rv.status_code == 400



account_uri = '/api/users/accounts'

def register(client, new_account):
    return client.post(account_uri, json=new_account)

correct_account_1 = {'username':'test1',
                     'email':'test1@dsm.hs.kr',
                     'password':'pass1234'}


def test_register_correct_minimum_information(client):
    rv = register(client, correct_account_1)
    assert rv.status_code == 201


# def test_register_correct_full_information(client):
#     full_information_account = correct_account_1.copy()
#     rv = register(client, full_information_account)
#     assert rv.status_code == 200


def test_register_same_username(client, create_temp_account):
    temp_account = create_temp_account()

    same_username_account = correct_account_1.copy()
    same_username_account['username'] = temp_account.user.username
    rv = register(client, same_username_account)
    assert rv.status_code == 409


def test_register_same_email(client, create_temp_account):
    temp_account = create_temp_account()

    same_username_account = correct_account_1.copy()
    same_username_account['email'] = temp_account.email
    rv = register(client, same_username_account)
    assert rv.status_code == 409


def test_register_wrong_username(client):
    #overlength username
    wrong_account_1 = correct_account_1.copy()
    wrong_account_1['username'] += 'x'*30

    rv = register(client, wrong_account_1)
    assert rv.status_code == 400

    #forbidden character
    wrong_account_2 = correct_account_1.copy()
    wrong_account_2['username'] += '?'

    rv2 = register(client, wrong_account_2)
    assert rv2.status_code == 400


def test_register_wrong_email(client):
    wrong_account_1 = correct_account_1.copy()
    wrong_account_1['email'] = '@'*30
    rv = register(client, wrong_account_1)
    assert rv.status_code == 400


def test_register_not_school_email(client):
    wrong_email_account = correct_account_1.copy()
    wrong_email_account['email'] = 'vjslzhs6@naver.com'
    rv = register(client, wrong_email_account)
    assert  rv.status_code == 403
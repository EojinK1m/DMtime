account_uri = '/api/users/accounts'

def register(client, new_account):
    return client.post(account_uri, json=new_account)

correct_account_1 = {'username':'test1',
                     'email':'test1@naver.com',
                     'password':'pass1234'}


def test_register_correct_minimum_information(client):
    rv = register(client, correct_account_1)
    assert rv.status_code == 200

def test_register_correct_full_information(client, create_temp_image):
    temp_image = create_temp_image()
    full_information_account = correct_account_1.copy()
    full_information_account['user_explain'] = 'test_user_explain'
    full_information_account['profile_image_id'] = temp_image.id

    rv = register(client, full_information_account)
    assert rv.status_code == 200


def test_register_with_not_exist_image_id(client):
    not_exist_image_id_account = correct_account_1.copy()
    not_exist_image_id_account['profile_image_id'] = 1
    rv = register(client, not_exist_image_id_account)
    assert rv.status_code == 206


def test_register_same_username(client):
    rv = register(client, correct_account_1)
    assert rv.status_code == 200

    same_username_account = correct_account_1.copy()
    same_username_account['email'] += 'xxxx'
    rv_2 = register(client, correct_account_1)
    assert rv_2.status_code == 403


def test_register_same_email(client):
    rv = register(client, correct_account_1)
    assert rv.status_code == 200

    same_username_account = correct_account_1.copy()
    same_username_account['username'] += 'xxxx'
    rv_2 = register(client, correct_account_1)
    assert rv_2.status_code == 403


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
    assert rv2.status_code == 400


def test_register_wrong_email(client):
    wrong_account_1 = correct_account_1.copy()
    wrong_account_1['email'] = 'x'*30
    rv = register(client, wrong_account_1)
    assert rv.status_code == 400



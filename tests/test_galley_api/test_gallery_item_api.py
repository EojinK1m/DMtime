url = '/api/board/gallery/'


def test_gallery_delete_correct(client, create_temp_account, create_temp_gallery):
    admin_account = create_temp_account(is_admin = True)
    temp_gallery = create_temp_gallery()

    rv = client.delete(url+f'{temp_gallery.id}',
                       headers={'authorization':'Bearer '+admin_account.generate_access_token()})

    assert rv.status_code == 200

def test_gallery_delete_with_not_admin_account(client, create_temp_account, create_temp_gallery):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()

    rv = client.delete(url + f'{temp_gallery.id}',
                       headers={'authorization': 'Bearer ' + temp_account.generate_access_token()})

    assert rv.status_code == 403

def test_gallery_put_correct(client, create_temp_account, create_temp_gallery):
    admin_account = create_temp_account(is_admin = True)
    temp_gallery = create_temp_gallery()

    changing_gallery_info = {'name':'change_gallery_info',
                             'explain':'this is explain of changed gallery'
                            }
    rv = client.delete(url+f'{temp_gallery.id}',
                       headers={'authorization':'Bearer '+admin_account.generate_access_token()},
                       json=changing_gallery_info)

    assert rv.status_code == 200

def test_gallery_put_with_data_miss(client, create_temp_account, create_temp_gallery):
    admin_account = create_temp_account(is_admin = True)

    temp_gallery = create_temp_gallery()

    changing_gallery_info_explain_missed = {'name':'change_gallery_info'}
    rv = client.delete(url+f'{temp_gallery.id}',
                       headers={'authorization':'Bearer '+admin_account.generate_access_token()},
                       json=changing_gallery_info_explain_missed)

    assert rv.status_code == 400

    changing_gallery_info_name_missed= {'explain':'this is explain of changed gallery'}
    rv_2 = client.delete(url + f'{temp_gallery.id}',
                       headers={'authorization': 'Bearer ' + admin_account.generate_access_token()},
                       json=changing_gallery_info_name_missed)

    assert rv_2.status_code == 400

def test_gallery_put_with_not_admin_account(client, create_temp_account, create_temp_gallery):
    temp_account = create_temp_account(is_admin = False)
    temp_gallery = create_temp_gallery()

    changing_gallery_info = {'name':'change_gallery_info',
                             'explain':'this is explain of changed gallery'
                            }
    rv = client.delete(url+f'{temp_gallery.id}',
                       headers={'authorization':'Bearer '+temp_account.generate_access_token()},
                       json=changing_gallery_info)

    assert rv.status_code == 403


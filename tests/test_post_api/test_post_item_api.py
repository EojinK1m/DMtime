url = '/api/board/post/'

def test_post_get_correct(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)

    rv = client.get(url+f'{temp_post.id}')

    assert rv.status_code == 200

    assert rv.json
    expected_keys_of_post = ('id',
                             'title',
                             'posted_gallery',
                             'content',
                             'posted_datetime',
                             'uploader',
                             'likes',
                             'views'
                             )
    for expect_key in expected_keys_of_post:
        assert expect_key in rv.json.keys()

    assert rv.json['posted_gallery']['name'] == temp_gallery.name
    assert rv.json['uploader']['username'] == temp_account.user.username


def test_post_get_not_exist(client):
    rv = client.get(url + '1')
    assert rv.status_code == 404





def test_post_delete_correct(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)

    rv = client.delete(url+f'{temp_post.id}',
                       headers={'authorization':'Bearer '+temp_account.generate_access_token()})

    assert rv.status_code == 200

def test_post_delete_with_admin_account(client, create_temp_account, create_temp_gallery, create_temp_post):
    admin_account = create_temp_account(is_admin = True )
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)

    rv = client.delete(url + f'{temp_post.id}',
                       headers={'authorization': 'Bearer ' + admin_account.generate_access_token()})

    assert rv.status_code == 200

def test_post_delete_with_another_account(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_account2 = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)

    rv = client.delete(url + f'{temp_post.id}',
                       headers={'authorization': 'Bearer ' + temp_account2.generate_access_token()})

    assert rv.status_code == 403


def test_post_put_correct(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)

    change_post_info = {'title':'Nanana Nanana nana kissing strangers',
                        'content':'my name is blurry face and i care what u think'}


    rv = client.put(url+f'{temp_post.id}',
                    headers={'authorization':'Bearer '+temp_account.generate_access_token()},
                    json=change_post_info)

    assert rv.status_code == 200


def test_post_put_with_data_miss(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)

    change_post_info = {'content':'my name is blurry face and i care what u think'}


    rv = client.put(url+f'{temp_post.id}',
                    headers={'authorization':'Bearer '+temp_account.generate_access_token()},
                    json=change_post_info)

    assert rv.status_code == 400


def test_post_put_with_another_account(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_account2 = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id=temp_account.id,
                                 upload_gallery_id=temp_gallery.id)

    change_post_info = {'title':'Nanana Nanana nana kissing strangers',
                        'content':'my name is blurry face and i care what u think'}

    rv = client.put(url + f'{temp_post.id}',
                    headers={'authorization': 'Bearer ' + temp_account2.generate_access_token()},
                    json=change_post_info)

    assert rv.status_code == 403



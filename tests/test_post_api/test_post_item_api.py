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


def test_post_patch_correct(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)

    change_post_info = {'title':'Nanana Nanana nana kissing strangers',
                        'content':'my name is blurry face and i care what u think'}


    rv = client.patch(url+f'{temp_post.id}',
                    headers={'authorization':'Bearer '+temp_account.generate_access_token()},
                    json=change_post_info)

    assert rv.status_code == 200


def test_post_patch_with_data_miss(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)

    change_post_info = {'content':'my name is blurry face and i care what u think'}


    rv = client.patch(url+f'{temp_post.id}',
                    headers={'authorization':'Bearer '+temp_account.generate_access_token()},
                    json=change_post_info)

    assert rv.status_code == 200


def test_post_patch_with_another_account(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_account2 = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id=temp_account.id,
                                 upload_gallery_id=temp_gallery.id)

    change_post_info = {'title':'Nanana Nanana nana kissing strangers',
                        'content':'my name is blurry face and i care what u think'}

    rv = client.patch(url + f'{temp_post.id}',
                    headers={'authorization': 'Bearer ' + temp_account2.generate_access_token()},
                    json=change_post_info)

    assert rv.status_code == 403

def test_post_patch_image_ids_correct(client, create_temp_account, create_temp_gallery, create_temp_post,
                                      create_temp_image):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_image = create_temp_image()
    temp_image_2 = create_temp_image()

    temp_post = create_temp_post(uploader_id=temp_account.id,
                                 upload_gallery_id=temp_gallery.id)

    rv = client.patch(url+f'{temp_post.id}',
                      json = {'image_ids':[temp_image.id]},
                      headers={'authorization': 'Bearer ' + temp_account.generate_access_token()})
    assert rv.status_code == 200

    rv2 = client.patch(url+f'{temp_post.id}',
                      json = {'image_ids':[temp_image.id, temp_image_2.id]},
                      headers={'authorization': 'Bearer ' + temp_account.generate_access_token()})
    assert rv2.status_code == 200

    rv3 = client.patch(url+f'{temp_post.id}',
                      json = {'image_ids':None},
                      headers={'authorization': 'Bearer ' + temp_account.generate_access_token()})

    assert rv3.status_code == 200

    rv4 = client.patch(url+f'{temp_post.id}',
                      json = {'image_ids':[]},
                      headers={'authorization': 'Bearer ' + temp_account.generate_access_token()})
    assert rv4.status_code == 200

def test_post_like_post_correct(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)
    access_token = temp_account.generate_access_token()

    rv = client.post(url+f'{temp_post.id}/like',
                    headers={'authorization':'Bearer '+access_token})

    assert rv.status_code == 200
    assert rv.json['likes'] == 1

    rv2 = client.post(url+f'{temp_post.id}/like',
                    headers={'authorization':'Bearer '+access_token})

    assert rv2.status_code == 200
    assert rv.json['likes'] == 0

def test_post_like_post_without_access_token(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(uploader_id = temp_account.id,
                                 upload_gallery_id = temp_gallery.id)


    rv = client.post(url+f'{temp_post.id}/like')
    assert rv.status_code == 401


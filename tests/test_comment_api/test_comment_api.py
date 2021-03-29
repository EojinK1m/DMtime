url = '/api/v1/board/comments/'

def test_comment_patch_correct(client,
                               create_temp_account,
                               create_temp_gallery,
                               create_temp_post,
                               create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)

    change_comment_info = {
        'content' : 'she played the fiddle in an irish band'
    }

    rv = client.patch(url+f'{temp_comment.id}',
                      json = change_comment_info,
                      headers = {'authorization':'Bearer '+temp_account.generate_access_token()})

    assert rv.status_code == 200

def test_comment_patch_without_content_key(client,
                                           create_temp_account,
                                           create_temp_gallery,
                                           create_temp_post,
                                           create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)

    change_comment_info = {}

    rv = client.patch(url + f'{temp_comment.id}',
                      json=change_comment_info,
                      headers={'authorization': 'Bearer ' + temp_account.generate_access_token()})

    assert rv.status_code == 200
    #assert 'miss' in rv.json['msg']

def test_comment_patch_without_access_token(client,
                                            create_temp_account,
                                            create_temp_gallery,
                                            create_temp_post,
                                            create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)

    change_comment_info = {
        'content' : 'she played the fiddle in an irish band'
    }

    rv = client.patch(url + f'{temp_comment.id}',
                      json=change_comment_info)

    assert rv.status_code == 401

def test_comment_patch_with_another_account(client,
                                            create_temp_account,
                                            create_temp_gallery,
                                            create_temp_post,
                                            create_temp_comment):
    temp_account = create_temp_account()
    temp_account_2 = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)

    change_comment_info = {
        'content' : 'she played the fiddle in an irish band'
    }

    rv = client.patch(url+f'{temp_comment.id}',
                    json = change_comment_info,
                    headers = {'authorization':'Bearer '+temp_account_2.generate_access_token()})

    assert rv.status_code == 403

def test_comment_patch_with_oversize_content(client,
                                             create_temp_account,
                                             create_temp_gallery,
                                             create_temp_post,
                                             create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)

    change_comment_info = {
        'content' : 's'*401
    }

    rv = client.patch(url+f'{temp_comment.id}',
                    json = change_comment_info,
                    headers = {'authorization':'Bearer '+temp_account.generate_access_token()})

    assert rv.status_code == 400
    #assert 'big' in rv.json['msg']

def test_comment_patch_to_not_exist_comment(client,
                                         create_temp_account):
    temp_account = create_temp_account()

    change_comment_info = {
        'content' : 'she played the fiddle in an irish band'
    }

    rv = client.patch(url+f'{1}',
                     json = change_comment_info,
                     headers = {'authorization':'Bearer '+temp_account.generate_access_token()})

    assert rv.status_code == 404


def test_comment_delete_correct(client,
                                create_temp_account,
                                create_temp_gallery,
                                create_temp_post,
                                create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)


    rv = client.delete(url+f'{temp_comment.id}',
                    headers = {'authorization':'Bearer '+temp_account.generate_access_token()})

    assert rv.status_code == 200


def test_comment_delete_with_admin_account(client,
                                            create_temp_account,
                                            create_temp_gallery,
                                            create_temp_post,
                                            create_temp_comment):
    temp_account = create_temp_account()
    admin_account = create_temp_account(is_admin=True)
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)

    rv = client.delete(url + f'{temp_comment.id}',
                    headers={'authorization': 'Bearer ' + admin_account.generate_access_token()})

    assert rv.status_code == 200

def test_comment_delete_with_another_account(client,
                                            create_temp_account,
                                            create_temp_gallery,
                                            create_temp_post,
                                            create_temp_comment):
    temp_account = create_temp_account()
    temp_account_2 = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)

    rv = client.delete(url + f'{temp_comment.id}',
                    headers={'authorization': 'Bearer ' + temp_account_2.generate_access_token()})

    assert rv.status_code == 403

def test_comment_delete_not_exist_comment(client,
                                            create_temp_account):
    temp_account = create_temp_account()

    rv = client.delete(url + f'{1}',
                    headers={'authorization': 'Bearer ' + temp_account.generate_access_token()})

    assert rv.status_code == 404


def test_comment_delete_without_access_token(client,
                                            create_temp_account,
                                            create_temp_gallery,
                                            create_temp_post,
                                            create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.email, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.email, temp_post.id)

    rv = client.delete(url + f'{temp_comment.id}')

    assert rv.status_code == 401
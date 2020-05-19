url = '/api/board/comment/'

def test_comment_put_correct(client,
                             create_temp_account,
                             create_temp_gallery,
                             create_temp_post,
                             create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.id, temp_post.id)

    change_comment_info = {
        'content' : 'she played the fiddle in an irish band'
    }

    rv = client.put(url+f'{temp_comment.id}',
                    json = change_comment_info,
                    headers = {'authorization':'Bearer '+temp_account.generate_access_token()})

    assert rv.status_code == 200

def test_comment_put_without_content_key(client,
                                         create_temp_account,
                                         create_temp_gallery,
                                         create_temp_post,
                                         create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.id, temp_post.id)

    change_comment_info = {}

    rv = client.put(url + f'{temp_comment.id}',
                    json=change_comment_info,
                    headers={'authorization': 'Bearer ' + temp_account.generate_access_token()})

    assert rv.status_code == 400
    assert 'miss' in rv.json['msg']

def test_comment_put_without_access_token(client,
                                          create_temp_account,
                                          create_temp_gallery,
                                          create_temp_post,
                                          create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.id, temp_post.id)

    change_comment_info = {
        'content' : 'she played the fiddle in an irish band'
    }

    rv = client.put(url + f'{temp_comment.id}',
                    json=change_comment_info)

    assert rv.status_code == 401

def test_comment_put_with_another_account(client,
                                         create_temp_account,
                                         create_temp_gallery,
                                         create_temp_post,
                                         create_temp_comment):
    temp_account = create_temp_account()
    temp_account_2 = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.id, temp_post.id)

    change_comment_info = {
        'content' : 'she played the fiddle in an irish band'
    }

    rv = client.put(url+f'{temp_comment.id}',
                    json = change_comment_info,
                    headers = {'authorization':'Bearer '+temp_account_2.generate_access_token()})

    assert rv.status_code == 401

def test_comment_put_with_oversize_content(client,
                                         create_temp_account,
                                         create_temp_gallery,
                                         create_temp_post,
                                         create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comment = create_temp_comment(temp_account.id, temp_post.id)

    change_comment_info = {
        'content' : 's'*401
    }

    rv = client.put(url+f'{temp_comment.id}',
                    json = change_comment_info,
                    headers = {'authorization':'Bearer '+temp_account.generate_access_token()})

    assert rv.status_code == 400
    assert 'big' in rv.json['msg']

def test_comment_put_to_not_exist_comment(client,
                                         create_temp_account):
    temp_account = create_temp_account()

    change_comment_info = {
        'content' : 'she played the fiddle in an irish band'
    }

    rv = client.put(url+f'{1}',
                    json = change_comment_info,
                    headers = {'authorization':'Bearer '+temp_account.generate_access_token()})

    assert rv.status_code == 404

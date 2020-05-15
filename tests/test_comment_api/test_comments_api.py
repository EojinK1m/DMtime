url = '/api/board/comment'


def test_comment_post_correct(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)

    test_comment_info = {'content':'This Is my Test Comment yeah~'}

    rv = client.post(url+f'?post-id={temp_post.id}',
                     headers={'authorization': 'Bearer '+temp_account.generate_access_token()},
                     json = test_comment_info)

    assert rv.status_code == 200

def test_comment_post_without_post_id(client, create_temp_account):
    temp_account = create_temp_account()

    test_comment_info = {'content':'This Is my Test Comment yeah~'}

    rv = client.post(url,
                     headers={'authorization': 'Bearer '+temp_account.generate_access_token()},
                     json = test_comment_info)

    assert rv.status_code == 400
    assert 'miss' in rv.json['msg']

def test_comment_post_with_wrong_post_id(client, create_temp_account):
    temp_account = create_temp_account()

    test_comment_info = {'content':'This Is my Test Comment yeah~'}

    rv = client.post(url+f'?post-id={1}',
                     headers={'authorization': 'Bearer '+temp_account.generate_access_token()},
                     json = test_comment_info)

    assert rv.status_code == 404


def test_comment_post_without_access_token(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)

    test_comment_info = {'content':'This Is my Test Comment yeah~'}

    rv = client.post(url+f'?post-id={temp_post.id}',
                     json = test_comment_info)

    assert rv.status_code == 401

def test_comment_post_over_size(client, create_temp_account, create_temp_gallery, create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)

    test_comment_info = {'content':'t'*401}

    rv = client.post(url+f'?post-id={temp_post.id}',
                     headers={'authorization': 'Bearer '+temp_account.generate_access_token()},
                     json = test_comment_info)

    assert rv.status_code == 400
    assert 'too big' in rv.json['msg']

def test_comment_post_lower_correct(client, create_temp_account, create_temp_gallery, create_temp_post,
                                    create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comment = create_temp_comment(wrote_user_id = temp_account.user.id, wrote_post_id = temp_post.id)

    test_comment_info = {'content':'This Is my Test Comment yeah~',
                         'upper_comment_id':temp_comment}

    rv = client.post(url+f'?post-id={temp_post.id}',
                     headers={'authorization': 'Bearer '+temp_account.generate_access_token()},
                     json = test_comment_info)

    assert rv.status_code == 200

def test_comment_post_lower_with_wrong_upper_comment_id(client,
                                                        create_temp_account,
                                                        create_temp_gallery,
                                                        create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)

    test_comment_info = {'content':'This Is my Test Comment yeah~',
                         'upper_comment_id':1}

    rv = client.post(url+f'?post-id={temp_post.id}',
                     headers={'authorization': 'Bearer '+temp_account.generate_access_token()},
                     json = test_comment_info)

    assert rv.status_code == 404

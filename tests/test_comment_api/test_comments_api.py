url = '/api/board/comments'


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

    test_comment_info = {'content':'t'*101}

    rv = client.post(url+f'?post-id={temp_post.id}',
                     headers={'authorization': 'Bearer '+temp_account.generate_access_token()},
                     json = test_comment_info)

    assert 'shorter than 100' in rv.json['msg']
    assert rv.status_code == 413


def test_comment_post_lower_correct(client, create_temp_account, create_temp_gallery, create_temp_post,
                                    create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comment = create_temp_comment(wrote_user_id = temp_account.user.id, wrote_post_id = temp_post.id)

    test_comment_info = {'content':'This Is my Test Comment yeah~',
                         'upper_comment_id':temp_comment.id}

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




def test_comment_get_on_post_correct(client, create_temp_account, create_temp_gallery, create_temp_post,
                                     create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comments = [create_temp_comment(wrote_user_id = temp_account.user.id,
                                         wrote_post_id = temp_post.id) for i in range(20)]

    rv = client.get(url+f'?post-id={temp_post.id}')

    assert rv.status_code == 200

    comments = rv.json['comments']
    assert comments != None

    expected_keys = (
        'id',
        'content',
        'wrote_datetime',
        'upper_comment_id',
        'writer'
    )
    for expect_key in expected_keys:
        assert expect_key in comments[0].keys()


def test_comment_get_on_user_correct(client, create_temp_account, create_temp_gallery, create_temp_post,
                                     create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comments = [create_temp_comment(wrote_user_id=temp_account.user.id,
                                         wrote_post_id=temp_post.id) for i in range(20)]

    rv = client.get(url + f'?post-id={temp_post.id}')

    assert rv.status_code == 200

    comments = rv.json['comments']
    assert comments != None

    expected_keys = (
        'id',
        'content',
        'wrote_datetime',
        'writer'
    )
    for expect_key in expected_keys:
        assert expect_key in comments[0].keys()


def test_comment_get_with_paging(client, create_temp_account, create_temp_gallery, create_temp_post,
                                 create_temp_comment):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)
    temp_comments = [create_temp_comment(wrote_user_id = temp_account.user.id,
                                         wrote_post_id = temp_post.id) for i in range(20)]

    rv = client.get(url+f'?post-id={temp_post.id}&per-page=5&page=4')

    for i in range(2):
        assert rv.status_code == 200
        assert rv.json['number_of_pages'] == 4

        comments = rv.json['comments']
        assert comments != None


        for i in range(len(comments)):
            assert temp_comments[-i-1].content == comments[-i-1]['content']

        rv = client.get(url+f'?username={temp_account.user.username}&per-page=5&page=4')


def test_comment_get_with_username_post_id_together(client, create_temp_account, create_temp_gallery,
                                                    create_temp_post):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_post = create_temp_post(temp_account.id, temp_gallery.id)

    rv = client.get(url+f'?post-id={temp_post.id}&username='+temp_account.user.username)

    assert rv.status_code == 400

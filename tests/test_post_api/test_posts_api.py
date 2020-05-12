url = '/api/board/post'

def post_post(client, post, gallery_id, access_token=''):
    return client.post(url+f'?gallery-id={gallery_id}',
                  json=post,
                  headers={'authorization':'Bearer '+access_token})

def test_post_post_correct(client, create_temp_account, create_temp_gallery):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()

    test_post_info = {'title': 'this is test post tile_1',
                      'content': 'Why dont you recognize. Im so rare?'}

    rv = post_post(client, test_post_info, temp_gallery.id, temp_account.generate_access_token())

    assert rv.status_code == 200

def test_post_post_without_access_token(client, create_temp_gallery):
    temp_gallery = create_temp_gallery()

    test_post_info = {'title': 'this is test post tile_1',
                      'content': 'Why dont you recognize. Im so rare?'}

    rv = post_post(client, test_post_info, temp_gallery.id)

    rv.status_code == 403

def test_post_post_too_fast(client, create_temp_account, create_temp_gallery):
    raise Exception('NotMakeError', 'We didnt think its detail yet')
    pass

def test_post_post_with_unsuitable_post_data(client, create_temp_account, create_temp_gallery):
    temp_account = create_temp_account()
    access_token_of_temp_account = temp_account.generate_access_token()
    temp_gallery = create_temp_gallery()


    too_long_title_post = {'title':'t'*41,
                           'content':'test test test content yeah~'}
    rv = post_post(client, too_long_title_post, temp_gallery.id, access_token_of_temp_account)
    assert rv.status_code == 400

    empty_title_post = {'title':'',
                        'content':'yeah im gonna take my horse to the old town road'}
    rv2 = post_post(client, empty_title_post, temp_gallery.id, access_token_of_temp_account)
    assert rv2.status_code == 400

    empty_content_post = {'title':'Samba yeah~',
                        'content':''}
    rv3 = post_post(client, empty_content_post, temp_gallery.id, access_token_of_temp_account)
    assert rv3.status_code == 400

    #test over size content


#make GET method test
url = '/api/board/posts'

def post_post(client, post, gallery_id, access_token=''):
    return client.post(url+f'?gallery-id={gallery_id}',
                  json=post,
                  headers={'authorization':'Bearer '+access_token})

def test_post_post_correct(client, create_temp_account, create_temp_gallery):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()


    test_post_info = {'title': 'this is test post tile_1',
                      'content': 'Why dont you recognize. Im so rare?',
                      'image_ids': []}

    rv = post_post(client, test_post_info, temp_gallery.id, temp_account.generate_access_token())

    assert rv.status_code == 200

def test_post_post_correct_with_image(client, create_temp_account, create_temp_gallery, create_temp_image):
    temp_account = create_temp_account()
    temp_gallery = create_temp_gallery()
    temp_image = create_temp_image()

    test_post_info = {'title': 'this is test post tile_1',
                      'content': 'Why dont you recognize. Im so rare?',
                      'image_ids':[temp_image.id]}

    rv = post_post(client, test_post_info, temp_gallery.id, temp_account.generate_access_token())

    assert rv.status_code == 200

def test_post_post_without_access_token(client, create_temp_gallery):
    temp_gallery = create_temp_gallery()

    test_post_info = {'title': 'this is test post tile_1',
                      'content': 'Why dont you recognize. Im so rare?'}

    rv = post_post(client, test_post_info, temp_gallery.id)

    rv.status_code == 403

# def test_post_post_too_fast(client, create_temp_account, create_temp_gallery):
#     raise Exception('NotMakeError', 'We didnt think its detail yet')
#     pass

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



def test_posts_get(client, create_temp_post, create_temp_gallery, create_temp_account):
    temp_gallery = create_temp_gallery()
    temp_account = create_temp_account()
    temp_posts = [create_temp_post(upload_gallery_id = temp_gallery.id, uploader_id=temp_account.id) for i in range(10)]

    rv = client.get(url+f'?gallery-id={temp_gallery.id}')

    assert rv.status_code == 200
    assert rv.json['number_of_pages']
    assert rv.json['posts']
    expected_keys_of_post = ('id',
                             'title',
                             'whether_exist_image',
                             'posted_datetime',
                             'uploader',
                             'likes',
                             'number_of_comments',
                             'views'
                             )
    for expect_key in expected_keys_of_post:
        assert expect_key in rv.json['posts'][0].keys()



def test_posts_get_with_per_page(client, create_temp_post, create_temp_gallery, create_temp_account):
    temp_gallery = create_temp_gallery()
    temp_account = create_temp_account()
    temp_posts = [create_temp_post(upload_gallery_id = temp_gallery.id, uploader_id=temp_account.id) for i in range(10)]

    rv = client.get(url+f'?gallery-id={temp_gallery.id}&per-page={5}')
    assert rv.status_code == 200

    json = rv.json
    assert json
    assert json['number_of_pages'] == 2
    assert json['posts'] != []


def test_posts_get_to_no_posts_gallery(client, create_temp_gallery, create_temp_account):
    temp_gallery = create_temp_gallery()
    temp_account = create_temp_account()

    rv = client.get(url+f'?gallery-id={temp_gallery.id}&per-page{5}')
    assert rv.status_code == 200

    assert rv.json
    assert rv.json['number_of_pages'] == 0
    assert rv.json['posts'] == []

def test_posts_get_whether_exist_value_of_post(client, create_temp_post, create_temp_gallery,\
                                               create_temp_account, create_temp_image):
    temp_gallery = create_temp_gallery()
    temp_account = create_temp_account()
    temp_image = create_temp_image()
    temp_post = create_temp_post(upload_gallery_id = temp_gallery.id, uploader_id=temp_account.id,
                                 included_images = [temp_image])


    rv = client.get(url+f'?gallery-id={temp_gallery.id}')
    assert rv.status_code == 200

    assert rv.json
    post = rv.json['posts'][0]
    assert post['whether_exist_image'] == True

def test_posts_get_without_gallery_id(client, create_temp_post, create_temp_gallery, create_temp_account):
    temp_galleries = [create_temp_gallery() for i in range(3)]
    temp_account = create_temp_account()
    temp_posts = [create_temp_post(upload_gallery_id = temp_gallery.id,
                                   uploader_id=temp_account.id) for temp_gallery in temp_galleries]

    rv = client.get(url)

    assert rv.json
    posts = rv.json['posts']
    assert posts
    assert len(posts) == 3

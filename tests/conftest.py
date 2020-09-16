import pytest

# @pytest.fixture(scope='session')
# def app():
#     from app import create_app
#     from app.config import TestConfig
#     return create_app(TestConfig)
#
# @pytest.fixture(scope='function', autouse=True)
# def db(app):
#     from app import db as _db
#     with app.app_context():
#         _db.create_all()
#
#     yield _db
#
#     with app.app_context():
#         _db.drop_all()
from app import create_app
from app.config import TestConfig
from app import db as _db
from app import redis_client as _redis_client
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    return create_app(TestConfig)


@pytest.fixture(scope="session")
def db(app, request):
    """
    Returns session-wide initialised database.
    """
    with app.app_context():
        _db.drop_all()
        _db.create_all()


@pytest.fixture(scope="function", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                sess.begin_nested()

        _db.session = sess
        yield sess

        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def redis_client():
    _redis_client.flushall()
    yield _redis_client

    _redis_client.flushall()

@pytest.fixture(scope='function')
def image(app, session):
    from app.api.image.model import ImageModel

    temp_image = ImageModel(filename='temp_image_1')

    session.add(temp_image)
    session.commit()

    return temp_image

@pytest.fixture()
def create_temp_image(app, session):
    from app.api.image.model import ImageModel
    import os

    def create_temp_image_():
        create_temp_image_.number += 1
        temp_image = ImageModel(filename=f'fake_filename{create_temp_image_.number}.png')


        temp_file = open(app.config['IMAGE_UPLOADS']+f'/fake_filename{create_temp_image_.number}.png', 'w')
        temp_file.close()

        session.add(temp_image)
        session.commit()

        return temp_image

    create_temp_image_.number = 0
    yield create_temp_image_

    for i in range(create_temp_image_.number):
        try:
            os.remove(os.path.join(app.config['IMAGE_UPLOADS'], f'fake_filename{i+1}.png'))
        except FileNotFoundError:
            continue
        except Exception as e:
            raise e



@pytest.fixture
def create_temp_account(app, session):
    from app.api.user.account.model import AccountModel
    from app.api.user.model import UserModel


    def create_temp_account_(profile_image = None, is_admin = False):
        email = f'test_account_{create_temp_account_.number}@dsm.hs.kr'
        username = f'test_user_{create_temp_account_.number}'
        password = f'test_password_{create_temp_account_.number}'
        user_explain = f'test_users_explain{create_temp_account_.number}'

        if(is_admin):
            if not(create_temp_account_.test_admin_exist):
                create_temp_account_.test_admin_exist = True
                email = 'test_admin'
            else:
                raise Exception('TestAdminOverError', 'Admin account for test cant exist more than one')

        temp_account = AccountModel(email=email,
                                    password_hash=AccountModel.hash_password(password))

        session.add(temp_account)
        session.commit()

        temp_user = UserModel(username=username,
                              explain=user_explain,
                              account_id=temp_account.id)

        session.add(temp_user)
        session.commit()

        if(profile_image):
            profile_image.user_id = temp_user.id

        create_temp_account_.number += 1
        return temp_account

    create_temp_account_.test_admin_exist = False
    create_temp_account_.number = 1
    return create_temp_account_

@pytest.fixture()
def create_temp_gallery(app, session, create_temp_account):
    from app.api.board.gallery.model import GalleryModel

    def create_temp_gallery_(manager_user=None):
        if(manager_user==None):
            manager_user = create_temp_account()

        name = f'test_gallery{create_temp_gallery_.number}_name'
        explain = f'test_gallery{create_temp_gallery_.number}_explain'

        temp_gallery = GalleryModel(name=name, explain=explain, manager_user_id=manager_user.id)

        session.add(temp_gallery)
        session.commit()

        create_temp_gallery_.number += 1

        return temp_gallery

    create_temp_gallery_.number = 0
    return create_temp_gallery_

@pytest.fixture()
def create_temp_post(app, session):
    from app.api.board.post.model import PostModel

    def create_temp_post_(uploader_id, upload_gallery_id, is_anonymous=False, included_images = None):
        title = f'test_post{create_temp_post_.number}_title'
        content = f'test_post{create_temp_post_.number}_content'+'test\n'*10

        temp_post = PostModel(uploader_id = uploader_id, gallery_id = upload_gallery_id,
                              title=title, content=content, is_anonymous=is_anonymous)

        session.add(temp_post)
        session.commit()

        if(included_images):
            for image in included_images:
                image.post_id = temp_post.id

        create_temp_post_.number += 1

        return temp_post

    create_temp_post_.number = 0
    return create_temp_post_

@pytest.fixture()
def create_temp_comment(app, session):
    from app.api.board.comment.model import CommentModel

    def create_temp_comment_(wrote_user_id, wrote_post_id, is_anonymous=False, upper_comment_id=None):
        content = f'test_post{create_temp_comment_.number}_content' + 'test\n' * 5

        import datetime
        temp_comment = CommentModel(content=content,
                                    wrote_user_id=wrote_user_id,
                                    wrote_post_id=wrote_post_id,
                                    upper_comment_id=upper_comment_id,
                                    wrote_datetime=datetime.datetime.now(),
                                    is_anonymous=is_anonymous)

        session.add(temp_comment)
        session.commit()

        create_temp_comment_.number += 1

        return temp_comment

    create_temp_comment_.number = 0
    return create_temp_comment_

@pytest.fixture
def create_temp_postlike(app, session):
    from app.api.board.post.model import PostLikeModel

    def create_temp_postlike_(post_id, liker_id):
        temp_postlike = PostLikeModel(post_id=post_id, liker_id=liker_id)

        session.add(temp_postlike)
        session.commit()

        create_temp_postlike.number += 1

        return temp_postlike

    create_temp_postlike.number = 0
    return create_temp_postlike_

@pytest.fixture
def create_temp_report(app, session):
    from app.api.board.gallery.report.model import ReportModel, ContentType

    def create_temp_report_(
        reported_user_id,
        gallery_id,
        reported_content_type,
        post_id=None,
        comment_id=None,
        reason=1
        ):

        if(reported_content_type == ContentType.COMMENT.value):
            if(post_id is not None or comment_id is None):
                raise Exception()
        elif(reported_content_type == ContentType.POST.value):
            if(post_id is None or comment_id is not None):
                raise Exception()

        detail_reason = f'This is detail reason for temp port {create_temp_report.number}'

        temp_report =\
            ReportModel(
                reason=reason,
                detail_reason=detail_reason,
                reported_user_id=reported_user_id,
                gallery_id=gallery_id,
                reported_content_type=reported_content_type,
                post_id=post_id,
                comment_id=comment_id
            )

        session.add(temp_report)
        session.commit()
        create_temp_report.number += 1

        return temp_report

    create_temp_report.number = 0
    return create_temp_report_


@pytest.fixture
def create_temp_register_account(app, session, redis_client):
    import json
    from app.util import verification_code_generater

    def create_temp_register_account_():
        email = f'test_account_{create_temp_register_account_.number}@dsm.hs.kr'
        username = f'test_user_{create_temp_register_account_.number}'
        password = f'test_password_{create_temp_register_account_.number}'

        verification_code = verification_code_generater.generate_verification_code()
        registry_data = {
            'email':email,
            'username':username,
            'password':password
        }
        redis_client.mset({verification_code:json.dumps(registry_data)})

        registry_data['verification_code']=verification_code

        create_temp_register_account_.number += 1
        return registry_data

    create_temp_register_account_.number = 1
    return create_temp_register_account_


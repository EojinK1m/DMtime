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

    def create_temp_image_():
        temp_image = ImageModel(filename=f'fake_filename{create_temp_image_.number}')
        create_temp_image_.number += 1

        session.add(temp_image)
        session.commit()

        return temp_image

    create_temp_image_.number = 0
    return create_temp_image_


@pytest.fixture
def create_temp_account(app, session):
    from app.api.user.account.model import AccountModel
    from app.api.user.model import UserModel


    def create_temp_account_(profile_image = None):
        email = f'test_account_{create_temp_account_.number}@test.test'
        username = f'test_user_{create_temp_account_.number}'
        password = f'test_password_{create_temp_account_.number}'
        user_explain = f'test_users_explain{create_temp_account_.number}'


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
            image.user_id = temp_user.id

        create_temp_account_.number += 1
        return temp_account

    create_temp_account_.number = 1
    return create_temp_account_

@pytest.fixture()
def create_temp_gallery(app, session):
    from app.api.board.gallery.model import GalleryModel

    def create_temp_gallery_():
        name = f'test_gallery{create_temp_gallery_.number}_name'
        explain = f'test_gallery{create_temp_gallery_.number}_explain'

        temp_gallery = GalleryModel(name=name, explain=explain)

        session.add(temp_gallery)
        session.commit()

        create_temp_gallery_.number += 1

        return temp_gallery

    create_temp_gallery_.number = 0
    return create_temp_gallery_

@pytest.fixture()
def create_temp_post(app, session):
    from app.api.board.post.model import PostModel

    def create_temp_post_(uploader_id, upload_gallery_id):
        title = f'test_post{create_temp_post_.number}_title'
        content = f'test_post{create_temp_post_.number}_content'+'test\n'*10

        temp_post = PostModel(uploader_id = uploader_id, gallery_id = upload_gallery_id,
                              title=title, content=content)

        session.add(temp_post)
        session.commit()

        create_temp_post_.number += 1

        return temp_post

    create_temp_post_.number = 0
    return create_temp_post_

@pytest.fixture()
def create_temp_comment(app, session):
    from app.api.board.comment.model import CommentModel

    def create_temp_comment_(wrote_user_id, wrote_post_id, upper_comment_id=None):
        content = f'test_post{create_temp_comment_.number}_content' + 'test\n' * 5

        temp_comment = CommentModel(content=content,
                                    wrote_user_id=wrote_user_id,
                                    wrote_post_id=wrote_post_id,
                                    upper_comment_id=upper_comment_id)

        session.add(temp_comment)
        session.commit()

        create_temp_comment_.number += 1

        return temp_comment

    create_temp_comment_.number = 0
    return create_temp_comment


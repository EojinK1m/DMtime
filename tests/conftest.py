import pytest

from app import create_app
from config import TestConfig
from app.extensions import db as _db
from app.extensions import redis_client as _redis_client
from sqlalchemy import event


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

        @event.listens_for(sess(), "after_transaction_end")
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
        # This instruction rollback any commit that were executed in the tests.
        txn.rollback()
        conn.close()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def redis_client():
    _redis_client.flushall()
    yield _redis_client

    _redis_client.flushall()


@pytest.fixture(scope="function")
def image(app, session):
    from app.api.v1.image.model import ImageModel

    temp_image = ImageModel(filename="temp_image_1")

    session.add(temp_image)
    session.commit()

    return temp_image


@pytest.fixture()
def create_temp_image(app, session):
    from app.api.v1.image.model import ImageModel
    import os

    def create_temp_image_():
        create_temp_image_.number += 1
        temp_image = ImageModel(
            filename=f"fake_filename{create_temp_image_.number}.png"
        )

        temp_file = open(
            app.config["IMAGE_UPLOADS"]
            + f"/fake_filename{create_temp_image_.number}.png",
            "w",
        )
        temp_file.close()

        session.add(temp_image)
        session.commit()

        return temp_image

    create_temp_image_.number = 0
    yield create_temp_image_

    for i in range(create_temp_image_.number):
        try:
            os.remove(
                os.path.join(
                    app.config["IMAGE_UPLOADS"], f"fake_filename{i+1}.png"
                )
            )
        except FileNotFoundError:
            continue
        except Exception as e:
            raise e


@pytest.fixture
def create_temp_account(app, session):
    from app.api.v1.user.model import UserModel
    from app.extensions import bcrypt

    def create_temp_account_(profile_image=None, is_admin=False):
        email = f"test_account_{create_temp_account_.number}@dsm.hs.kr"
        username = f"test_user_{create_temp_account_.number}"
        password = f"test_password_{create_temp_account_.number}"
        user_explain = f"test_users_explain{create_temp_account_.number}"

        if is_admin:
            if not (create_temp_account_.test_admin_exist):
                create_temp_account_.test_admin_exist = True
                email = "test_admin"
            else:
                raise Exception(
                    "TestAdminOverError",
                    "Admin account for test cant exist more than one",
                )

        temp_user = UserModel(
            email=email,
            username=username,
            password_hash=bcrypt.generate_password_hash(password),
            explain=user_explain,
        )

        session.add(temp_user)
        session.commit()

        if profile_image:
            profile_image.user_id = temp_user.email

        create_temp_account_.number += 1
        return temp_user

    create_temp_account_.test_admin_exist = False
    create_temp_account_.number = 1
    return create_temp_account_


@pytest.fixture()
def create_temp_gallery(app, session, create_temp_account):
    from app.api.v1.gallery.model import GalleryModel

    def create_temp_gallery_(manager_user=None, gallery_type=1):
        if manager_user == None:
            manager_user = create_temp_account()

        name = f"test_gallery{create_temp_gallery_.number}_name"
        explain = f"test_gallery{create_temp_gallery_.number}_explain"
        gallery_id = f"test_gallery{create_temp_gallery_.number}_id"

        temp_gallery = GalleryModel(
            name=name,
            explain=explain,
            gallery_id=gallery_id,
            manager_user_id=manager_user.email,
            gallery_type=gallery_type,
        )

        session.add(temp_gallery)
        session.commit()
        create_temp_gallery_.number += 1

        return temp_gallery

    create_temp_gallery_.number = 0
    return create_temp_gallery_


@pytest.fixture()
def create_temp_post(app, session):
    from app.api.v1.post.model import PostModel

    def create_temp_post_(
        uploader_id,
        upload_gallery_id,
        is_anonymous=False,
        included_images=None,
    ):
        title = f"test_post{create_temp_post_.number}_title"
        content = (
            f"test_post{create_temp_post_.number}_content" + "test\n" * 10
        )

        temp_post = PostModel(
            uploader_id=uploader_id,
            gallery_id=upload_gallery_id,
            title=title,
            content=content,
            is_anonymous=is_anonymous,
        )

        session.add(temp_post)
        session.commit()

        if included_images:
            for image in included_images:
                image.post_id = temp_post.id

        create_temp_post_.number += 1

        return temp_post

    create_temp_post_.number = 0
    return create_temp_post_


@pytest.fixture()
def create_temp_comment(app, session):
    from app.api.v1.comment.model import CommentModel

    def create_temp_comment_(
        wrote_user_id, wrote_post_id, is_anonymous=False, upper_comment_id=None
    ):
        content = (
            f"test_post{create_temp_comment_.number}_content" + "test\n" * 5
        )

        import datetime

        temp_comment = CommentModel(
            content=content,
            wrote_user_id=wrote_user_id,
            wrote_post_id=wrote_post_id,
            upper_comment_id=upper_comment_id,
            wrote_datetime=datetime.datetime.now(),
            is_anonymous=is_anonymous,
        )

        session.add(temp_comment)
        session.commit()

        create_temp_comment_.number += 1

        return temp_comment

    create_temp_comment_.number = 0
    return create_temp_comment_


@pytest.fixture
def create_temp_postlike(app, session):
    from app.api.v1.postlike.model import PostlikeModel

    def create_temp_postlike_(post_id, liker_id):
        temp_postlike = PostlikeModel(post_id=post_id, liker_id=liker_id)

        session.add(temp_postlike)
        session.commit()

        create_temp_postlike.number += 1

        return temp_postlike

    create_temp_postlike.number = 0
    return create_temp_postlike_


@pytest.fixture
def create_temp_postdislike(app, session):
    from app.api.v1.post.model import PostdislikeModel

    def create_temp_postdislike_(post_id, liker_id):
        temp_postdislike = PostdislikeModel(post_id=post_id, liker_id=liker_id)

        session.add(temp_postdislike)
        session.commit()

        create_temp_postdislike.number += 1

        return temp_postdislike

    create_temp_postdislike.number = 0
    return create_temp_postdislike_


@pytest.fixture
def create_temp_report(app, session):
    from app.api.v1.gallery.report.model import ReportModel, ContentType

    def create_temp_report_(
        reported_user_id,
        gallery_id,
        reported_content_type,
        post_id=None,
        comment_id=None,
        reason=1,
    ):

        if reported_content_type == ContentType.COMMENT.value:
            if post_id is not None or comment_id is None:
                raise Exception()
        elif reported_content_type == ContentType.POST.value:
            if post_id is None or comment_id is not None:
                raise Exception()

        detail_reason = (
            f"This is detail reason for temp port {create_temp_report.number}"
        )

        temp_report = ReportModel(
            reason=reason,
            detail_reason=detail_reason,
            reported_user_id=reported_user_id,
            gallery_id=gallery_id,
            reported_content_type=reported_content_type,
            post_id=post_id,
            comment_id=comment_id,
        )

        session.add(temp_report)
        session.commit()
        create_temp_report.number += 1

        return temp_report

    create_temp_report.number = 0
    return create_temp_report_


@pytest.fixture
def create_temp_register_account(app, session, redis_client):
    from app.util import random_string_generator
    from app.api.v1.user.model import UserModel
    from app.api.v1.user.view import Users
    from app.extensions import bcrypt

    def create_temp_register_account_():
        email = (
            f"test_account_{create_temp_register_account_.number}@dsm.hs.kr"
        )
        username = f"test_user_{create_temp_register_account_.number}"
        password = f"test_password_{create_temp_register_account_.number}"
        explain = f"test_user_explain_{create_temp_register_account_.number}"

        temp_user = UserModel(
            email=email,
            username=username,
            password_hash=bcrypt.generate_password_hash(password),
            explain=explain,
        )
        verification_code = (
            random_string_generator.generate_verification_code()
        )

        Users().store_account_data_with_verification_code(
            verification_code, temp_user
        )

        create_temp_register_account_.number += 1
        return {"verification_code": verification_code, "user": temp_user}

    create_temp_register_account_.number = 1
    return create_temp_register_account_


@pytest.fixture
def create_temp_post_report(app, session):
    from app.api.v1.report.model import PostReport

    def create_temp_post_report_(user, post, reason=1, detail_reason='None'):
        if not detail_reason:
            detail_reason = f'test post report detail reason {create_temp_post_report_.number}'

        temp_post_report = PostReport(
            post_id=post.id,
            user_id=user.email,
            reason=reason,
            detail_reason=detail_reason
        )

        session.add(temp_post_report)
        session.commit()

        create_temp_post_report_.number += 1
        return temp_post_report

    create_temp_post_report_.number = 1
    return create_temp_post_report_


@pytest.fixture
def create_temp_comment_report(app, session):
    from app.api.v1.report.model import CommentReport

    def create_temp_comment_report_(user, comment, reason=1, detail_reason='None'):
        if not detail_reason:
            detail_reason = f'test post report detail reason {create_temp_comment_report_.number}'

        temp_comment_report = CommentReport(
            comment_id=comment.id,
            user_id=user.email,
            reason=reason,
            detail_reason=detail_reason
        )

        session.add(temp_comment_report)
        session.commit()

        create_temp_comment_report_.number += 1
        return temp_comment_report

    create_temp_comment_report_.number = 1
    return create_temp_comment_report_

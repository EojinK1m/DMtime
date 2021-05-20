from app.extensions import db


def commit_session_after_request(response):
    db.session.commit()
    return response


def rollback_session_when_error(error=None):
    if error is not None:
        db.session.rollback()

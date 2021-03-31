from app import db


def commit_session_after_request(response):
    db.session.commit()
    return response


def rollback_session_when_error(error=None):
    print(f"rollback_session_when_error is executed \n arg is {error}")

    if error is not None:
        db.session.rollback()
